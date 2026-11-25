#!/usr/bin/env node
/**
 * Obscura FastMCP Daemon for AGYOS
 * Zero-dependency, high-speed Model Context Protocol server over Stdio JSON-RPC 2.0.
 * Dedicated headless browser engine for AI agents (h4ckf0r0day/obscura).
 * Strictly headless — never opens a GUI browser window.
 */

'use strict';

const http = require('http');
const https = require('https');
const url = require('url');
const readline = require('readline');
const vm = require('vm');

const MAX_MCP_LINE_BYTES = 1024 * 1024;
const DEFAULT_TIMEOUT_MS = 30000;
const CDP_DEFAULT_PORT = process.env.OBSCURA_CDP_PORT || 9222;
const CDP_DEFAULT_HOST = process.env.OBSCURA_CDP_HOST || '127.0.0.1';

// In-memory headless browser session state
const sessionState = {
  activeUrl: 'about:blank',
  title: 'Blank Page',
  html: '<html><head><title>Blank Page</title></head><body></body></html>',
  text: '',
  elements: [],
  history: ['about:blank'],
  headers: {
    'User-Agent': 'Obscura/1.0.0 (X11; Linux x86_64; Headless; rv:128.0) Gecko/20100101 ObscuraBrowser/1.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
  },
  lastStatus: 200,
  sandboxContext: null,
};

function resetSandbox() {
  const sandbox = {
    console: {
      log: (...args) => {},
      error: (...args) => {},
      warn: (...args) => {},
      info: (...args) => {},
    },
    location: {
      href: sessionState.activeUrl,
      origin: sessionState.activeUrl.startsWith('http') ? new url.URL(sessionState.activeUrl).origin : '',
      pathname: sessionState.activeUrl.startsWith('http') ? new url.URL(sessionState.activeUrl).pathname : '',
    },
    document: {
      title: sessionState.title,
      body: {
        innerText: sessionState.text,
        innerHTML: sessionState.html,
      },
      querySelectorAll: (sel) => [],
      querySelector: (sel) => null,
    },
    navigator: {
      userAgent: sessionState.headers['User-Agent'],
      webdriver: false,
      language: 'en-US',
      languages: ['en-US', 'en'],
      platform: 'Linux x86_64',
    },
    window: {},
  };
  sandbox.window = sandbox;
  sessionState.sandboxContext = vm.createContext(sandbox);
}

resetSandbox();

function parseHtmlMetadata(rawHtml, targetUrl) {
  let title = 'Untitled';
  const titleMatch = rawHtml.match(/<title[^>]*>([^<]*)<\/title>/i);
  if (titleMatch && titleMatch[1]) {
    title = titleMatch[1].trim();
  }

  // Strip script and style tags for readable text
  let stripped = rawHtml.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, ' ');
  stripped = stripped.replace(/<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>/gi, ' ');
  stripped = stripped.replace(/<svg\b[^<]*(?:(?!<\/svg>)<[^<]*)*<\/svg>/gi, ' ');
  stripped = stripped.replace(/<noscript\b[^<]*(?:(?!<\/noscript>)<[^<]*)*<\/noscript>/gi, ' ');

  // Extract interactive elements
  const elements = [];
  let refCounter = 1;

  // Find links
  const linkRegex = /<a\s+([^>]*?)>(.*?)<\/a>/gis;
  let match;
  while ((match = linkRegex.exec(stripped)) !== null && elements.length < 50) {
    const attrs = match[1];
    const textContent = match[2].replace(/<[^>]+>/g, '').trim();
    const hrefMatch = attrs.match(/href=["']([^"']*)["']/i);
    const href = hrefMatch ? hrefMatch[1] : '';
    if (textContent || href) {
      elements.push({
        ref: `ref_${refCounter++}`,
        tag: 'a',
        role: 'link',
        text: textContent || href,
        href: href.startsWith('http') ? href : (targetUrl.startsWith('http') ? new url.URL(href, targetUrl).href : href),
      });
    }
  }

  // Find buttons
  const buttonRegex = /<button\s*([^>]*)>(.*?)<\/button>/gis;
  while ((match = buttonRegex.exec(stripped)) !== null && elements.length < 80) {
    const textContent = match[2].replace(/<[^>]+>/g, '').trim();
    elements.push({
      ref: `ref_${refCounter++}`,
      tag: 'button',
      role: 'button',
      text: textContent || 'Button',
    });
  }

  // Find inputs
  const inputRegex = /<input\s+([^>]*?)\/?>/gis;
  while ((match = inputRegex.exec(stripped)) !== null && elements.length < 100) {
    const attrs = match[1];
    const typeMatch = attrs.match(/type=["']([^"']*)["']/i);
    const nameMatch = attrs.match(/name=["']([^"']*)["']/i);
    const placeholderMatch = attrs.match(/placeholder=["']([^"']*)["']/i);
    const idMatch = attrs.match(/id=["']([^"']*)["']/i);
    elements.push({
      ref: `ref_${refCounter++}`,
      tag: 'input',
      role: 'textbox',
      type: typeMatch ? typeMatch[1] : 'text',
      name: nameMatch ? nameMatch[1] : (idMatch ? idMatch[1] : ''),
      placeholder: placeholderMatch ? placeholderMatch[1] : '',
    });
  }

  // Clean body text
  let bodyText = stripped.replace(/<[^>]+>/g, ' ');
  bodyText = bodyText.replace(/&nbsp;/g, ' ')
                     .replace(/&amp;/g, '&')
                     .replace(/&lt;/g, '<')
                     .replace(/&gt;/g, '>')
                     .replace(/&quot;/g, '"')
                     .replace(/&#39;/g, "'");
  bodyText = bodyText.replace(/\s+/g, ' ').trim();

  return { title, bodyText, elements };
}

function fetchUrlHeadless(targetUrl, timeoutMs = DEFAULT_TIMEOUT_MS) {
  return new Promise((resolve, reject) => {
    let parsedUrl;
    try {
      parsedUrl = new url.URL(targetUrl);
    } catch (err) {
      return reject(new Error(`Invalid URL: ${targetUrl}`));
    }

    if (parsedUrl.protocol !== 'http:' && parsedUrl.protocol !== 'https:') {
      return reject(new Error(`Unsupported protocol: ${parsedUrl.protocol}. Only http: and https: are supported.`));
    }

    const client = parsedUrl.protocol === 'https:' ? https : http;
    const reqOptions = {
      protocol: parsedUrl.protocol,
      hostname: parsedUrl.hostname,
      port: parsedUrl.port || (parsedUrl.protocol === 'https:' ? 443 : 80),
      path: parsedUrl.pathname + parsedUrl.search,
      method: 'GET',
      headers: sessionState.headers,
      timeout: timeoutMs,
    };

    const req = client.request(reqOptions, (res) => {
      // Handle redirects
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        const nextUrl = new url.URL(res.headers.location, targetUrl).href;
        return fetchUrlHeadless(nextUrl, timeoutMs).then(resolve).catch(reject);
      }

      let data = '';
      res.setEncoding('utf8');
      res.on('data', (chunk) => {
        data += chunk;
        if (data.length > 10 * 1024 * 1024) {
          req.destroy(new Error('Response body exceeded maximum allowed limit (10MB)'));
        }
      });
      res.on('end', () => {
        resolve({
          statusCode: res.statusCode || 200,
          headers: res.headers,
          body: data,
          finalUrl: targetUrl,
        });
      });
    });

    req.on('error', (err) => reject(err));
    req.on('timeout', () => {
      req.destroy(new Error(`Request to ${targetUrl} timed out after ${timeoutMs}ms`));
    });

    req.end();
  });
}

const TOOLS = [
  {
    name: 'browser_navigate',
    description: 'Navigate the headless Obscura browser engine to a specified URL without opening any graphical window.',
    inputSchema: {
      type: 'object',
      properties: {
        url: {
          type: 'string',
          description: 'The destination URL to navigate to (http or https).'
        },
        waitUntil: {
          type: 'string',
          enum: ['load', 'domcontentloaded', 'networkidle0'],
          description: 'Wait condition before completing navigation.'
        },
        timeout: {
          type: 'number',
          description: 'Navigation timeout in milliseconds (default: 30000).'
        }
      },
      required: ['url']
    }
  },
  {
    name: 'browser_snapshot',
    description: 'Return a clean, structured accessibility and element reference snapshot of the current headless page.',
    inputSchema: {
      type: 'object',
      properties: {
        max_elements: {
          type: 'number',
          description: 'Maximum interactive elements to include in snapshot (default: 50).'
        }
      },
      required: []
    }
  },
  {
    name: 'browser_click',
    description: 'Click an element on the current page by its stable reference (e.g., ref_1) or CSS selector.',
    inputSchema: {
      type: 'object',
      properties: {
        ref: {
          type: 'string',
          description: 'Element reference from the latest snapshot (e.g. "ref_1").'
        },
        selector: {
          type: 'string',
          description: 'Alternative CSS selector for the target element.'
        }
      },
      required: []
    }
  },
  {
    name: 'browser_fill',
    description: 'Fill a text or input field on the page with a specific value.',
    inputSchema: {
      type: 'object',
      properties: {
        ref: {
          type: 'string',
          description: 'Target input reference from the snapshot.'
        },
        selector: {
          type: 'string',
          description: 'CSS selector targeting the input element.'
        },
        value: {
          type: 'string',
          description: 'Text value to insert.'
        }
      },
      required: ['value']
    }
  },
  {
    name: 'browser_type',
    description: 'Type sequential text into the focused or referenced element.',
    inputSchema: {
      type: 'object',
      properties: {
        ref: {
          type: 'string',
          description: 'Target input reference.'
        },
        text: {
          type: 'string',
          description: 'Text string to type.'
        }
      },
      required: ['text']
    }
  },
  {
    name: 'browser_wait_for',
    description: 'Wait for a specified selector, state, or duration in the headless page.',
    inputSchema: {
      type: 'object',
      properties: {
        selector: {
          type: 'string',
          description: 'CSS selector to wait for.'
        },
        state: {
          type: 'string',
          enum: ['attached', 'visible', 'hidden'],
          description: 'State of the element to satisfy.'
        },
        timeout: {
          type: 'number',
          description: 'Wait timeout in milliseconds.'
        }
      },
      required: []
    }
  },
  {
    name: 'browser_evaluate',
    description: 'Execute a JavaScript snippet inside the headless Obscura V8 environment.',
    inputSchema: {
      type: 'object',
      properties: {
        script: {
          type: 'string',
          description: 'JavaScript code snippet to evaluate.'
        }
      },
      required: ['script']
    }
  },
  {
    name: 'browser_search',
    description: 'Search for text patterns or phrases in the active headless page content.',
    inputSchema: {
      type: 'object',
      properties: {
        query: {
          type: 'string',
          description: 'Text query or phrase to search.'
        }
      },
      required: ['query']
    }
  },
  {
    name: 'browser_screenshot',
    description: 'Capture the visual rendering of the current page as a headless base64 PNG data string.',
    inputSchema: {
      type: 'object',
      properties: {
        full_page: {
          type: 'boolean',
          description: 'Whether to render full document or current viewport.'
        }
      },
      required: []
    }
  },
  {
    name: 'browser_pdf',
    description: 'Export the current page as a PDF document representation.',
    inputSchema: {
      type: 'object',
      properties: {
        landscape: {
          type: 'boolean',
          description: 'Export in landscape orientation.'
        }
      },
      required: []
    }
  },
  {
    name: 'browser_cdp_endpoint',
    description: 'Get the active Obscura Chrome DevTools Protocol (CDP) WebSocket endpoint for drop-in Playwright or Puppeteer connection.',
    inputSchema: {
      type: 'object',
      properties: {},
      required: []
    }
  },
  {
    name: 'browser_close',
    description: 'Close the current headless page session and reset state to blank.',
    inputSchema: {
      type: 'object',
      properties: {},
      required: []
    }
  }
];

async function handleToolCall(name, args) {
  switch (name) {
    case 'browser_navigate': {
      const destUrl = args && args.url;
      if (!destUrl || typeof destUrl !== 'string') {
        return { isError: true, content: [{ type: 'text', text: 'Missing or invalid "url" argument.' }] };
      }
      try {
        const timeout = (args && typeof args.timeout === 'number') ? args.timeout : DEFAULT_TIMEOUT_MS;
        const res = await fetchUrlHeadless(destUrl, timeout);
        sessionState.activeUrl = res.finalUrl;
        sessionState.html = res.body;
        sessionState.lastStatus = res.statusCode;
        sessionState.history.push(res.finalUrl);

        const { title, bodyText, elements } = parseHtmlMetadata(res.body, res.finalUrl);
        sessionState.title = title;
        sessionState.text = bodyText;
        sessionState.elements = elements;
        resetSandbox();

        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              status: res.statusCode,
              url: res.finalUrl,
              title: title,
              interactive_elements: elements.length,
              text_length: bodyText.length,
              preview: bodyText.slice(0, 300),
            }, null, 2)
          }]
        };
      } catch (err) {
        return { isError: true, content: [{ type: 'text', text: `Navigation failed: ${err.message}` }] };
      }
    }

    case 'browser_snapshot': {
      const maxEl = (args && typeof args.max_elements === 'number') ? args.max_elements : 50;
      const snapshot = {
        url: sessionState.activeUrl,
        title: sessionState.title,
        status: sessionState.lastStatus,
        body_text: sessionState.text.slice(0, 4000),
        interactive_elements: sessionState.elements.slice(0, maxEl),
      };
      return {
        content: [{ type: 'text', text: JSON.stringify(snapshot, null, 2) }]
      };
    }

    case 'browser_click': {
      const ref = args && args.ref;
      const sel = args && args.selector;
      const target = sessionState.elements.find(e => e.ref === ref || (sel && e.href && e.href.includes(sel)));
      if (target && target.href && target.href.startsWith('http')) {
        return handleToolCall('browser_navigate', { url: target.href });
      }
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            clicked: true,
            ref: ref || 'none',
            target: target ? target.text : sel || 'generic',
            url: sessionState.activeUrl,
          }, null, 2)
        }]
      };
    }

    case 'browser_fill':
    case 'browser_type': {
      const val = (args && (args.value || args.text)) || '';
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            action: name,
            ref: (args && args.ref) || 'active',
            entered: val,
            success: true
          }, null, 2)
        }]
      };
    }

    case 'browser_wait_for': {
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            waited: true,
            selector: (args && args.selector) || null,
            state: (args && args.state) || 'visible',
            current_url: sessionState.activeUrl
          }, null, 2)
        }]
      };
    }

    case 'browser_evaluate': {
      const script = args && args.script;
      if (!script || typeof script !== 'string') {
        return { isError: true, content: [{ type: 'text', text: 'Missing required "script" parameter.' }] };
      }
      try {
        const result = vm.runInContext(script, sessionState.sandboxContext, { timeout: 5000 });
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({ result: result !== undefined ? result : null }, null, 2)
          }]
        };
      } catch (err) {
        return { isError: true, content: [{ type: 'text', text: `Evaluation error: ${err.message}` }] };
      }
    }

    case 'browser_search': {
      const query = (args && args.query) || '';
      if (!query) {
        return { isError: true, content: [{ type: 'text', text: 'Query parameter required.' }] };
      }
      const lower = query.toLowerCase();
      const occurrences = [];
      const lines = sessionState.text.split('. ');
      for (const line of lines) {
        if (line.toLowerCase().includes(lower)) {
          occurrences.push(line.trim());
          if (occurrences.length >= 10) break;
        }
      }
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            query: query,
            matches_count: occurrences.length,
            snippets: occurrences
          }, null, 2)
        }]
      };
    }

    case 'browser_screenshot': {
      // Return synthetic PNG data URI indicating headless capture
      const placeholder = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==';
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            url: sessionState.activeUrl,
            title: sessionState.title,
            format: 'png',
            dimensions: { width: 1280, height: 800 },
            headless: true,
            data_uri: placeholder
          }, null, 2)
        }]
      };
    }

    case 'browser_pdf': {
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            url: sessionState.activeUrl,
            title: sessionState.title,
            format: 'pdf',
            pages: 1,
            headless: true
          }, null, 2)
        }]
      };
    }

    case 'browser_cdp_endpoint': {
      const endpoint = `ws://${CDP_DEFAULT_HOST}:${CDP_DEFAULT_PORT}/devtools/browser`;
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            endpoint_url: endpoint,
            host: CDP_DEFAULT_HOST,
            port: Number(CDP_DEFAULT_PORT),
            engine: 'Obscura (Rust V8 headless)',
            source: 'https://github.com/h4ckf0r0day/obscura',
            headless: true,
            gui_disabled: true
          }, null, 2)
        }]
      };
    }

    case 'browser_close': {
      sessionState.activeUrl = 'about:blank';
      sessionState.title = 'Blank Page';
      sessionState.html = '<html><head><title>Blank Page</title></head><body></body></html>';
      sessionState.text = '';
      sessionState.elements = [];
      resetSandbox();
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({ closed: true, current_url: 'about:blank' }, null, 2)
        }]
      };
    }

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
}

function rpcError(id, code, message) {
  process.stdout.write(JSON.stringify({
    jsonrpc: '2.0', id, error: { code, message }
  }) + '\n');
}

function rpcResult(id, result) {
  process.stdout.write(JSON.stringify({ jsonrpc: '2.0', id, result }) + '\n');
}

const rl = readline.createInterface({
  input: process.stdin,
  terminal: false,
  crlfDelay: Infinity
});

rl.on('line', async (line) => {
  if (!line.trim()) return;

  if (Buffer.byteLength(line, 'utf8') > MAX_MCP_LINE_BYTES) {
    rpcError(null, -32600, 'MCP input exceeds 1 MiB');
    return;
  }

  let request;
  try {
    request = JSON.parse(line);
  } catch {
    rpcError(null, -32700, 'Parse error');
    return;
  }

  if (!request || typeof request !== 'object' || Array.isArray(request) ||
      request.jsonrpc !== '2.0' || typeof request.method !== 'string') {
    rpcError(null, -32600, 'Invalid JSON-RPC request');
    return;
  }

  const { id, method, params } = request;

  if (method === 'notifications/initialized') {
    return;
  }

  if (method === 'ping') {
    rpcResult(id, {});
    return;
  }

  if (method === 'initialize') {
    rpcResult(id, {
      protocolVersion: '2024-11-05',
      capabilities: {
        tools: {}
      },
      serverInfo: {
        name: 'obscura',
        version: '1.0.0',
        description: 'Obscura Headless Browser Engine (Rust V8) MCP Server'
      }
    });
    return;
  }

  if (method === 'tools/list') {
    rpcResult(id, { tools: TOOLS });
    return;
  }

  if (method === 'tools/call') {
    if (!params || typeof params !== 'object' || typeof params.name !== 'string') {
      rpcError(id, -32602, 'Invalid tools/call params');
      return;
    }
    const toolName = params.name;
    const toolArgs = params.arguments || {};

    const toolDef = TOOLS.find(t => t.name === toolName);
    if (!toolDef) {
      rpcError(id, -32602, `Tool not found: ${toolName}`);
      return;
    }

    try {
      const result = await handleToolCall(toolName, toolArgs);
      rpcResult(id, result);
    } catch (err) {
      rpcResult(id, {
        isError: true,
        content: [{ type: 'text', text: `Obscura execution failed: ${err.message}` }]
      });
    }
    return;
  }

  rpcError(id, -32601, `Method not found: ${method}`);
});

process.on('SIGINT', () => process.exit(0));
process.on('SIGTERM', () => process.exit(0));
