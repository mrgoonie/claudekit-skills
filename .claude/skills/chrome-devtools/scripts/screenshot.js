#!/usr/bin/env node
/**
 * Take a screenshot
 * Usage: node screenshot.js --output screenshot.png [--url https://example.com] [--full-page true] [--selector .element]
 */
import { getBrowser, getPage, closeBrowser, parseArgs, outputJSON, outputError } from './lib/browser.js';
import fs from 'fs/promises';
import path from 'path';

async function screenshot() {
  const args = parseArgs(process.argv.slice(2));

  if (!args.output) {
    outputError(new Error('--output is required'));
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

    const screenshotOptions = {
      path: args.output,
      type: args.format || 'png',
      fullPage: args['full-page'] === 'true'
    };

    if (args.quality) {
      screenshotOptions.quality = parseInt(args.quality);
    }

    let buffer;
    if (args.selector) {
      const element = await page.$(args.selector);
      if (!element) {
        throw new Error(`Element not found: ${args.selector}`);
      }
      buffer = await element.screenshot(screenshotOptions);
    } else {
      buffer = await page.screenshot(screenshotOptions);
    }

    const result = {
      success: true,
      output: path.resolve(args.output),
      size: buffer.length,
      url: page.url()
    };

    outputJSON(result);

    if (args.close !== 'false') {
      await closeBrowser();
    }
  } catch (error) {
    outputError(error);
  }
}

screenshot();
