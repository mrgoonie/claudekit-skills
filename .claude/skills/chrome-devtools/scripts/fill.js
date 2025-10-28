#!/usr/bin/env node
/**
 * Fill form fields
 * Usage: node fill.js --selector "#input" --value "text" [--url https://example.com]
 */
import { getBrowser, getPage, closeBrowser, parseArgs, outputJSON, outputError } from './lib/browser.js';

async function fill() {
  const args = parseArgs(process.argv.slice(2));

  if (!args.selector) {
    outputError(new Error('--selector is required'));
    return;
  }

  if (!args.value) {
    outputError(new Error('--value is required'));
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

    // Clear existing value if specified
    if (args.clear === 'true') {
      await page.$eval(args.selector, el => el.value = '');
    }

    // Type into element
    await page.type(args.selector, args.value, {
      delay: parseInt(args.delay || '0')
    });

    outputJSON({
      success: true,
      selector: args.selector,
      value: args.value,
      url: page.url()
    });

    if (args.close !== 'false') {
      await closeBrowser();
    }
  } catch (error) {
    outputError(error);
  }
}

fill();
