#!/usr/bin/env node
/**
 * Puppeteer Fetcher with Stealth Plugin
 * Fetches content from URLs that may have CAPTCHA or anti-bot protection
 *
 * Usage: node puppeteer_fetch.js <URL> [--timeout N] [--wait N] [--json]
 *
 * Requirements:
 *   npm install puppeteer puppeteer-extra puppeteer-extra-plugin-stealth
 */

const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");

// Use stealth plugin to avoid detection
puppeteer.use(StealthPlugin());

// Helper function for delay (replaces deprecated page.waitForTimeout)
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// Parse arguments
const args = process.argv.slice(2);
let url = null;
let timeout = 30000;
let waitTime = 2000;
let outputJson = false;

for (let i = 0; i < args.length; i++) {
  if (args[i] === "--timeout") {
    timeout = parseInt(args[++i]) * 1000;
  } else if (args[i] === "--wait") {
    waitTime = parseInt(args[++i]) * 1000;
  } else if (args[i] === "--json") {
    outputJson = true;
  } else if (!args[i].startsWith("--")) {
    url = args[i];
  }
}

if (!url) {
  console.error(
    "Usage: node puppeteer_fetch.js <URL> [--timeout N] [--wait N] [--json]",
  );
  process.exit(1);
}

async function fetchWithPuppeteer() {
  let browser = null;

  try {
    browser = await puppeteer.launch({
      headless: "new",
      args: [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
        "--disable-accelerated-2d-canvas",
        "--disable-gpu",
        "--window-size=1920,1080",
      ],
    });

    const page = await browser.newPage();

    // Set viewport and user agent
    await page.setViewport({ width: 1920, height: 1080 });
    await page.setUserAgent(
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    );

    // Set extra headers
    await page.setExtraHTTPHeaders({
      "Accept-Language": "en-US,en;q=0.9",
      Accept:
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    });

    // Navigate to URL
    const response = await page.goto(url, {
      waitUntil: "networkidle2",
      timeout: timeout,
    });

    // Wait for dynamic content to load
    await delay(waitTime);

    // Check for CAPTCHA indicators
    const captchaDetected = await page.evaluate(() => {
      const bodyText = document.body.innerText.toLowerCase();
      const html = document.documentElement.outerHTML.toLowerCase();

      return (
        bodyText.includes("captcha") ||
        bodyText.includes("verify you are human") ||
        bodyText.includes("please verify") ||
        bodyText.includes("are you a robot") ||
        html.includes("g-recaptcha") ||
        html.includes("h-captcha") ||
        html.includes("cf-turnstile") ||
        document.querySelector('iframe[src*="captcha"]') !== null ||
        document.querySelector('iframe[src*="challenge"]') !== null
      );
    });

    // Extract content
    const result = await page.evaluate(() => {
      // Get title
      const title = document.title || "";

      // Get meta description
      const metaDesc = document.querySelector('meta[name="description"]');
      const description = metaDesc ? metaDesc.getAttribute("content") : "";

      // Get meta author
      const metaAuthor = document.querySelector('meta[name="author"]');
      const author = metaAuthor ? metaAuthor.getAttribute("content") : "";

      // Get publish date
      const metaDate =
        document.querySelector('meta[property="article:published_time"]') ||
        document.querySelector('meta[name="publish-date"]') ||
        document.querySelector('meta[name="date"]');
      const publishDate = metaDate ? metaDate.getAttribute("content") : "";

      // Get main content - try various selectors
      let mainContent = "";
      const contentSelectors = [
        "article",
        '[role="main"]',
        "main",
        ".post-content",
        ".article-content",
        ".entry-content",
        ".content",
        "#content",
        ".post",
        ".article",
        "body",
      ];

      for (const selector of contentSelectors) {
        const el = document.querySelector(selector);
        if (el) {
          const text = el.innerText.trim();
          if (text.length > mainContent.length) {
            mainContent = text;
          }
        }
      }

      // Clean up content
      mainContent = mainContent
        .replace(/\s+/g, " ")
        .replace(/\n\s*\n/g, "\n\n")
        .trim();

      // Get all links
      const links = Array.from(document.querySelectorAll("a[href]"))
        .slice(0, 50)
        .map((a) => ({
          text: a.innerText.trim().slice(0, 100),
          href: a.href,
        }))
        .filter((l) => l.text && l.href);

      return {
        title,
        description,
        author,
        publishDate,
        content: mainContent,
        links,
      };
    });

    // Get final URL (after redirects)
    const finalUrl = page.url();

    await browser.close();

    const output = {
      url: url,
      final_url: finalUrl,
      fetched_at: new Date().toISOString(),
      success: true,
      title: result.title,
      content: result.content,
      content_format: "text",
      metadata: {
        description: result.description,
        author: result.author,
        publish_date: result.publishDate,
        links: result.links,
      },
      quality: {
        word_count: result.content.split(/\s+/).length,
        reading_time_minutes: Math.max(
          1,
          Math.round(result.content.split(/\s+/).length / 200),
        ),
        has_substantial_content: result.content.split(/\s+/).length > 100,
      },
      captcha_detected: captchaDetected,
      method: "puppeteer-stealth",
      error: null,
    };

    if (outputJson) {
      console.log(JSON.stringify(output, null, 2));
    } else {
      console.log(`URL: ${output.url}`);
      console.log(`Title: ${output.title}`);
      console.log(`Word Count: ${output.quality.word_count}`);
      console.log(`CAPTCHA Detected: ${output.captcha_detected}`);
      console.log("\n--- CONTENT ---\n");
      console.log(output.content);
    }
  } catch (error) {
    if (browser) {
      await browser.close();
    }

    const output = {
      url: url,
      fetched_at: new Date().toISOString(),
      success: false,
      error: error.message,
      method: "puppeteer-stealth",
    };

    if (outputJson) {
      console.log(JSON.stringify(output, null, 2));
    } else {
      console.error(`Error: ${error.message}`);
    }

    process.exit(1);
  }
}

fetchWithPuppeteer();
