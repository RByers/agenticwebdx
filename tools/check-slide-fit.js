#!/usr/bin/env node
// Fail if any slide in the deck overflows the fixed slide size.
//
// Usage: node tools/check-slide-fit.js [path/to/deck.html]
// Uses the same check the deck runs on load (web/slide-fit.js) and exits
// non-zero listing each overflowing slide. Run it after editing slides.
const path = require('path');
const {chromium} = require('playwright');

(async () => {
  const deck = path.resolve(process.argv[2] || path.join(__dirname, '..', 'web', 'index.html'));
  const browser = await chromium.launch();
  let failed = false;
  try {
    // Check a couple of viewport sizes in case rounding differs.
    for (const viewport of [{width: 1280, height: 720}, {width: 1920, height: 1080}]) {
      const page = await browser.newPage({viewport});
      await page.goto('file://' + deck, {waitUntil: 'load'});
      await page.evaluate(() => document.fonts.ready);
      const problems = await page.evaluate(() => {
        if (typeof window.findOverflowingSlides !== 'function')
          throw new Error('Deck does not load slide-fit.js');
        return window.findOverflowingSlides();
      });
      for (const p of problems) {
        failed = true;
        console.error(`${viewport.width}x${viewport.height}: slide ${p.index} (#${p.id}): ${p.reasons.join('; ')}`);
      }
      await page.close();
    }
  } finally {
    await browser.close();
  }
  if (failed) process.exit(1);
  console.log('All slides fit.');
})().catch(e => { console.error(e); process.exit(2); });
