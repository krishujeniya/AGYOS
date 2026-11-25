import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const execFileAsync = promisify(execFile);

function resolveToken() {
  if (process.env.OP_SERVICE_ACCOUNT_TOKEN) {
    return process.env.OP_SERVICE_ACCOUNT_TOKEN.trim();
  }
  const tokenPath = path.join(os.homedir(), ".config", "1password-mcp", "token");
  if (fs.existsSync(tokenPath)) {
    return fs.readFileSync(tokenPath, "utf8").trim();
  }
  return null;
}

async function runOp(args, envOverrides = {}) {
  const token = resolveToken();
  const env = { ...process.env, ...envOverrides };
  if (token) {
    env.OP_SERVICE_ACCOUNT_TOKEN = token;
  }
  try {
    const { stdout, stderr } = await execFileAsync("op", args, { env });
    return { stdout, stderr };
  } catch (error) {
    throw new Error(error.stderr || error.message);
  }
}

const server = new Server(
  {
    name: "1password-mcp",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "op_whoami",
        description: "Check 1Password authentication status and active service account/user profile.",
        inputSchema: {
          type: "object",
          properties: {},
          additionalProperties: false,
        },
      },
      {
        name: "op_list_vaults",
        description: "List all 1Password vaults accessible by the current account.",
        inputSchema: {
          type: "object",
          properties: {},
          additionalProperties: false,
        },
      },
      {
        name: "op_list_items",
        description: "List items inside a specific vault or across accessible vaults (returns titles, IDs, categories).",
        inputSchema: {
          type: "object",
          properties: {
            vault: {
              type: "string",
              description: "Vault name or ID to list items from (recommended for service accounts).",
            },
            categories: {
              type: "string",
              description: "Optional category filter (e.g. Login, Password, Secure Note, API Credential).",
            },
          },
          additionalProperties: false,
        },
      },
      {
        name: "op_get_item",
        description: "Fetch item metadata and field layout from a 1Password vault by item title or ID.",
        inputSchema: {
          type: "object",
          properties: {
            item: {
              type: "string",
              description: "Item name, ID, or title.",
            },
            vault: {
              type: "string",
              description: "Vault name or ID where the item resides.",
            },
          },
          required: ["item"],
          additionalProperties: false,
        },
      },
      {
        name: "op_read_reference",
        description: "Resolve an op:// secret reference URI (e.g., 'op://Vault/Item/field'). Note: Treat secrets with extreme care.",
        inputSchema: {
          type: "object",
          properties: {
            reference: {
              type: "string",
              description: "Secret reference in op:// format (e.g., op://Production/Stripe/api-key).",
            },
          },
          required: ["reference"],
          additionalProperties: false,
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    if (name === "op_whoami") {
      const { stdout } = await runOp(["whoami", "--format=json"]);
      return { content: [{ type: "text", text: stdout }] };
    }

    if (name === "op_list_vaults") {
      const { stdout } = await runOp(["vault", "list", "--format=json"]);
      return { content: [{ type: "text", text: stdout }] };
    }

    if (name === "op_list_items") {
      const cliArgs = ["item", "list", "--format=json"];
      if (args?.vault) {
        cliArgs.push(`--vault=${args.vault}`);
      }
      if (args?.categories) {
        cliArgs.push(`--categories=${args.categories}`);
      }
      const { stdout } = await runOp(cliArgs);
      return { content: [{ type: "text", text: stdout }] };
    }

    if (name === "op_get_item") {
      const cliArgs = ["item", "get", args.item, "--format=json"];
      if (args?.vault) {
        cliArgs.push(`--vault=${args.vault}`);
      }
      const { stdout } = await runOp(cliArgs);
      return { content: [{ type: "text", text: stdout }] };
    }

    if (name === "op_read_reference") {
      const { stdout } = await runOp(["read", args.reference]);
      return { content: [{ type: "text", text: stdout.trim() }] };
    }

    throw new Error(`Unknown tool: ${name}`);
  } catch (error) {
    return {
      content: [{ type: "text", text: `Error: ${error.message}` }],
      isError: true,
    };
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((err) => {
  console.error("1Password MCP Fatal:", err);
  process.exit(1);
});
