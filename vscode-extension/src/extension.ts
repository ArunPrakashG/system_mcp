import * as vscode from 'vscode';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

let client: Client | null = null;

async function ensureClient(): Promise<Client> {
  if (client) return client;

  // Spawn the Python MCP server via uv
  const transport = new StdioClientTransport({
    command: process.platform === 'win32' ? 'uv.exe' : 'uv',
    args: ['run', '-m', 'system_mcp.server'],
    env: Object.fromEntries(Object.entries(process.env ?? {}).filter(([k, v]) => typeof v === 'string')) as Record<string, string>,
  });

  const c = new Client({ name: 'vscode-system-mcp', version: '0.1.0' });
  await c.connect(transport);
  client = c;
  return c;
}

export async function activate(context: vscode.ExtensionContext) {
  const disposableConnect = vscode.commands.registerCommand('systemMcp.connect', async () => {
    try {
      await ensureClient();
      vscode.window.showInformationMessage('System MCP connected');
    } catch (err: any) {
      vscode.window.showErrorMessage(`Failed to connect System MCP: ${err?.message ?? err}`);
    }
  });

  const disposableListTools = vscode.commands.registerCommand('systemMcp.tools.list', async () => {
    try {
      const c = await ensureClient();
      const tools = await c.listTools();
      const items = tools.tools.map(t => ({ label: t.name, description: t.description ?? '' }));
      const pick = await vscode.window.showQuickPick(items, { title: 'System MCP Tools' });
      if (pick) {
        vscode.window.showInformationMessage(`Selected: ${pick.label}`);
      }
    } catch (err: any) {
      vscode.window.showErrorMessage(`Failed to list tools: ${err?.message ?? err}`);
    }
  });

  const disposableScreenshot = vscode.commands.registerCommand('systemMcp.tools.screenshot', async () => {
    try {
      const c = await ensureClient();
  const result = await c.callTool({ name: 'take_screenshot', arguments: {} });
  const output: any = (result as any).output ?? {};
  const content = Array.isArray(output.content) ? output.content[0] : undefined;
      if (content && content.type === 'image') {
        const dataUri = content.data.startsWith('data:') ? content.data : `data:image/${content.mimeType ?? 'png'};base64,${content.data}`;
        const panel = vscode.window.createWebviewPanel('systemMcpScreenshot', 'System MCP Screenshot', vscode.ViewColumn.Active, {});
        panel.webview.html = `<!DOCTYPE html><html><body style=\"margin:0\"><img src=\"${dataUri}\" style=\"max-width:100%; max-height:100vh;\" /></body></html>`;
      } else {
        vscode.window.showWarningMessage('Screenshot tool did not return an image');
      }
    } catch (err: any) {
      vscode.window.showErrorMessage(`Failed to take screenshot: ${err?.message ?? err}`);
    }
  });

  context.subscriptions.push(disposableConnect, disposableListTools, disposableScreenshot);
}

export function deactivate() {
  // StdioClientTransport doesn't expose kill here; process exits when VS Code unloads.
  client = null;
}
