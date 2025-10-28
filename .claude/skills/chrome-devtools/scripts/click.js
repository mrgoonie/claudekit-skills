#!/usr/bin/env node
/**
 * Click an element
 * Usage: node click.js --selector ".button" [--url https://example.com] [--wait-for ".result"]
 */
import { getBrowser, getPage, closeBrowser, parseArgs, outputJSON, outputError } from './lib/browser.js';

async function click() {
  const args = parseArgs(process.argv.slice(2));

  if (!args.selector) {
    outputError(new Error('--selector is required'));
    return;
  }

  try {
    const browser = await getBrowser({
      headless: args.headless !== 'false'
    });

    const page = await getPage(browser);

    // Navigate if URL provided
    if (args.url) {
      await page.goto(args.url, {
        waitUntil: args['wait-until'] || 'networkidle2'
      });
    }

    // Wait for element
    await page.waitForSelector(args.selector, {
      visible: true,
      timeout: parseInt(args.timeout || '5000')
    });

    // Click element
    await page.click(args.selector);

    // Wait for optional selector after click
    if (args['wait-for']) {
      await page.waitForSelector(args['wait-for'], {
        timeout: parseInt(args.timeout || '5000')
      });
    } else {
      // Wait for navigation or timeout
      try {
        await page.waitForNavigation({
          waitUntil: 'networkidle2',
          timeout: 2000
        });
      } catch (e) {
        // Ignore timeout - no navigation occurred
      }
    }

    outputJSON({
      success: true,
      url: page.url(),
      title: await page.title()
    });

    if (args.close !== 'false') {
      await closeBrowser();
    }
  } catch (error) {
    outputError(error);
  }
}

click();
