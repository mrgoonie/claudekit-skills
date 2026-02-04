#!/usr/bin/env node
/**
 * Download design images from Dribbble search results
 * Usage: node download-dribbble.js --query "financial dashboard dark ui" --output ./downloads [--count 12] [--quality hd] [--no-compress]
 * 
 * Options:
 *   --query <string>      : Search query (required)
 *   --output <path>       : Output directory (default: ./dribbble-downloads)
 *   --count <number>      : Number of images to download (default: 12)
 *   --quality <quality>   : Image quality - "regular" or "hd" (default: hd)
 *   --delay <ms>          : Delay between downloads in ms (default: 1000)
 *   --max-size <mb>       : Max image size in MB before compression (default: 10)
 *   --no-compress         : Don't compress images
 */
import { getBrowser, getPage, closeBrowser, parseArgs, outputJSON, outputError } from './lib/browser.js';
import fs from 'fs/promises';
import path from 'path';
import { execSync } from 'child_process';
import { createWriteStream } from 'fs';
import { pipeline } from 'stream/promises';

/**
 * Compress image using ImageMagick if it exceeds max size
 */
async function compressImageIfNeeded(filePath, maxSizeMB = 10) {
  const stats = await fs.stat(filePath);
  const originalSize = stats.size;
  const maxSizeBytes = maxSizeMB * 1024 * 1024;

  if (originalSize <= maxSizeBytes) {
    return { compressed: false, originalSize, finalSize: originalSize };
  }

  try {
    execSync('magick -version', { stdio: 'pipe' });
  } catch {
    try {
      execSync('convert -version', { stdio: 'pipe' });
    } catch {
      console.warn('Warning: ImageMagick not found. Skipping compression.');
      return { compressed: false, originalSize, finalSize: originalSize };
    }
  }

  try {
    const ext = path.extname(filePath).toLowerCase();
    const tempPath = filePath.replace(ext, `.temp${ext}`);

    // Progressive compression for JPEG
    const compressionCmd = `magick "${filePath}" -strip -quality 75 -interlace Plane "${tempPath}"`;
    execSync(compressionCmd, { stdio: 'pipe' });

    const compressedStats = await fs.stat(tempPath);
    const compressedSize = compressedStats.size;

    if (compressedSize > maxSizeBytes) {
      const finalPath = filePath.replace(ext, `.final${ext}`);
      const aggressiveCmd = `magick "${tempPath}" -strip -quality 60 -resize 85% "${finalPath}"`;
      execSync(aggressiveCmd, { stdio: 'pipe' });
      await fs.unlink(tempPath);
      await fs.rename(finalPath, filePath);
    } else {
      await fs.rename(tempPath, filePath);
    }

    const finalStats = await fs.stat(filePath);
    return { compressed: true, originalSize, finalSize: finalStats.size };
  } catch (error) {
    console.warn(`Compression warning for ${filePath}:`, error.message);
    return { compressed: false, originalSize, finalSize: originalSize };
  }
}

/**
 * Extract image URL from a Dribbble shot page
 */
async function extractImageFromShotPage(page, shotUrl) {
  try {
    await page.goto(shotUrl, { waitUntil: 'networkidle2', timeout: 30000 });
    
    // Get the main image/shot content
    const imageUrl = await page.evaluate(() => {
      // Try multiple strategies to find the image
      let img = null;
      
      // Strategy 1: Look for og:image meta tag (highest quality)
      const ogImage = document.querySelector('meta[property="og:image"]');
      if (ogImage?.content) {
        return ogImage.content;
      }
      
      // Strategy 2: Look for shot image in main container
      img = document.querySelector('img[alt*="shot"], img[alt*="design"], img.shot-image');
      if (img?.src) {
        return img.src;
      }
      
      // Strategy 3: Look for largest image on page
      const allImages = Array.from(document.querySelectorAll('img'));
      const largeImages = allImages.filter(i => {
        const width = i.naturalWidth || i.width;
        const height = i.naturalHeight || i.height;
        return width > 400 || height > 400;
      });
      
      if (largeImages.length > 0) {
        // Return the first large image's src or srcset
        const img = largeImages[0];
        if (img.srcset) {
          const urls = img.srcset.split(',').map(s => s.trim());
          return urls[urls.length - 1].split(' ')[0];
        }
        return img.src;
      }
      
      return null;
    });
    
    return imageUrl;
  } catch (error) {
    console.error(`Error extracting from ${shotUrl}:`, error.message);
    return null;
  }
}

/**
 * Download image from URL with retry logic
 */
async function downloadImage(url, filePath, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch(url, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
          'Referer': 'https://dribbble.com/'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      // Check content type - be more lenient
      const contentType = response.headers.get('content-type') || '';
      if (!contentType.includes('image') && !url.includes('.jpg') && !url.includes('.png')) {
        throw new Error(`Invalid content type: ${contentType}`);
      }

      await pipeline(response.body, createWriteStream(filePath));
      return true;
    } catch (error) {
      if (i === retries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
    }
  }
}

async function downloadDribbble() {
  const args = parseArgs(process.argv.slice(2));

  if (!args.query) {
    outputError(new Error('--query is required'));
    return;
  }

  const query = encodeURIComponent(args.query);
  const outputDir = args.output || './dribbble-downloads';
  const count = parseInt(args.count) || 12;
  const quality = args.quality || 'hd';
  const delay = parseInt(args.delay) || 1000;
  const maxSize = parseFloat(args['max-size']) || 10;
  const noCompress = args['no-compress'] === 'true';

  try {
    // Create output directory
    await fs.mkdir(outputDir, { recursive: true });

    const browser = await getBrowser({ headless: args.headless !== 'false' });
    const page = await getPage(browser);

    // Navigate to Dribbble search
    const searchUrl = `https://dribbble.com/search/shots/popular?q=${query}`;
    console.log(`Navigating to: ${searchUrl}`);

    await page.goto(searchUrl, { waitUntil: 'networkidle2', timeout: 60000 });

    // Wait for images to load - with longer timeout for heavy pages
    await new Promise(resolve => setTimeout(resolve, 5000));

    // Extract image URLs from the page
    const images = await page.evaluate(() => {
      const results = [];
      const seenUrls = new Set();
      
      // Strategy: Get all shot links directly - they follow the pattern /shots/XXXXX-title
      const shotLinks = document.querySelectorAll('a[href*="/shots/"]');
      console.log(`Found ${shotLinks.length} potential shot links`);
      
      shotLinks.forEach((link, index) => {
        try {
          const href = link.href;
          
          // Filter to only actual shot links (format: /shots/NUMBER-TITLE)
          // Avoid navigation links like /shots/popular, /shots/recent, etc.
          if (!href.includes('/shots/') || !href.match(/\/shots\/\d+/)) {
            return;
          }
          
          // Skip if we've already seen this URL
          if (seenUrls.has(href)) {
            return;
          }
          seenUrls.add(href);
          
          // Get shot title from the link or its parent
          let title = 'untitled';
          
          // Try to get title from link text or nearby elements
          let titleText = link.textContent?.trim();
          if (!titleText) {
            // Try parent container
            const parent = link.closest('[data-test="shot"], li, article, div[class*="shot"]');
            const titleEl = parent?.querySelector('h3, h2, [data-test="shot-title"]');
            titleText = titleEl?.textContent?.trim();
          }
          
          if (titleText) {
            title = titleText;
          }
          
          results.push({
            title: title.replace(/[^a-z0-9-]/gi, '-').toLowerCase().substring(0, 50),
            shotUrl: href
          });
        } catch (e) {
          console.error(`Error processing shot at index ${index}:`, e.message);
        }
      });

      console.log(`Extracted ${results.length} unique shot URLs`);
      return results;
    });

    if (images.length === 0) {
      // Debug: show page structure
      const pageInfo = await page.evaluate(() => {
        return {
          title: document.title,
          shotElements: document.querySelectorAll('[data-test="shot"]').length,
          allLinks: document.querySelectorAll('a').length,
          shotLinks: document.querySelectorAll('a[href*="/shots/"]').length,
          images: document.querySelectorAll('img').length
        };
      });
      
      const errorMsg = `No images found on the page. Page info: ${JSON.stringify(pageInfo)}. Try adding --headless false to debug visually.`;
      outputError(new Error(errorMsg));
      await closeBrowser();
      return;
    }

    console.log(`Found ${images.length} images. Downloading ${Math.min(count, images.length)}...`);

    const downloadResults = [];
    const downloadedCount = Math.min(count, images.length);

    for (let i = 0; i < downloadedCount; i++) {
      const shot = images[i];
      const fileName = `${String(i + 1).padStart(3, '0')}-${shot.title}.jpg`;
      const filePath = path.join(outputDir, fileName);

      try {
        process.stdout.write(`[${i + 1}/${downloadedCount}] ${shot.title}... `);

        // Step 1: Visit the shot page to get the actual image URL
        process.stdout.write('(loading) ');
        const imageUrl = await extractImageFromShotPage(page, shot.shotUrl);
        
        if (!imageUrl) {
          throw new Error('Could not extract image URL from shot page');
        }

        // Debug: show the extracted image URL
        if (process.env.DEBUG) {
          console.log(`\n  Shot URL: ${shot.shotUrl}`);
          console.log(`  Image URL: ${imageUrl}`);
        }

        // Step 2: Download the image
        process.stdout.write('(downloading) ');
        await downloadImage(imageUrl, filePath);

        // Get file size
        const stats = await fs.stat(filePath);
        let result = {
          success: true,
          index: i + 1,
          filename: fileName,
          path: path.resolve(filePath),
          originalSize: stats.size,
          size: stats.size,
          url: imageUrl,
          shotUrl: shot.shotUrl
        };

        // Compress if needed
        if (!noCompress) {
          const compressionResult = await compressImageIfNeeded(filePath, maxSize);
          if (compressionResult.compressed) {
            result.compressed = true;
            result.compressionRatio = (
              (1 - compressionResult.finalSize / compressionResult.originalSize) * 100
            ).toFixed(2) + '%';
            result.size = compressionResult.finalSize;
          }
        }

        downloadResults.push(result);
        console.log('✓');

        // Add delay between downloads
        if (i < downloadedCount - 1) {
          await new Promise(resolve => setTimeout(resolve, delay));
        }
      } catch (error) {
        console.log(`✗ (${error.message})`);
        downloadResults.push({
          success: false,
          index: i + 1,
          filename: fileName,
          error: error.message,
          shotUrl: shot.shotUrl
        });
      }
    }

    // Summary
    const successful = downloadResults.filter(r => r.success).length;
    const summary = {
      success: true,
      query: args.query,
      outputDir: path.resolve(outputDir),
      totalRequested: downloadedCount,
      totalDownloaded: successful,
      totalFailed: downloadedCount - successful,
      downloads: downloadResults
    };

    console.log(`\n✓ Download complete: ${successful}/${downloadedCount} successful`);
    outputJSON(summary);

    await closeBrowser();
  } catch (error) {
    outputError(error);
    process.exit(1);
  }
}

downloadDribbble();
