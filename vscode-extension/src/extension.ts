import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { SSEClientTransport } from '@modelcontextprotocol/sdk/client/sse.js';
import { StreamableHTTPClientTransport } from '@modelcontextprotocol/sdk/client/streamableHttp.js';
import * as vscode from 'vscode';

let client: Client | null = null;
let toolsProvider: ToolsProvider | null = null;

async function ensureClient(): Promise<Client> {
    if (client) return client;

    const cfg = vscode.workspace.getConfiguration('systemMcp');
    const transportKind = cfg.get<string>('transport', 'stdio');
    const serverUrl = cfg.get<string>('server.url', 'http://127.0.0.1:3000');
    const c = new Client({ name: 'vscode-system-mcp', version: '0.1.0' });

    if (transportKind === 'sse') {
        const transport = new SSEClientTransport(new URL(serverUrl));
        await c.connect(transport);
    } else if (transportKind === 'streamable-http') {
        const transport = new StreamableHTTPClientTransport(new URL(serverUrl));
        await c.connect(transport);
    } else {
        // stdio: Spawn the Python MCP server via configured command/args
        const command = cfg.get<string>('server.command', process.platform === 'win32' ? 'uv.exe' : 'uv');
        const args = cfg.get<string[]>('server.args', ['run', '-m', 'system_mcp.server']);
        const env = Object.fromEntries(Object.entries(process.env ?? {}).filter(([, v]) => typeof v === 'string')) as Record<string, string>;
        const transport = new StdioClientTransport({ command, args, env });
        await c.connect(transport);
    }

    client = c;
    return c;
}

export async function activate(context: vscode.ExtensionContext) {
    toolsProvider = new ToolsProvider(async () => {
        const c = await ensureClient();
        const res = await c.listTools();
        return res.tools;
    }, async (toolName: string) => {
        const c = await ensureClient();
        const result = await c.callTool({ name: toolName, arguments: {} });
        showToolResult(toolName, result);
    });
    vscode.window.registerTreeDataProvider('systemMcp.toolsView', toolsProvider);
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

    const disposableRefresh = vscode.commands.registerCommand('systemMcp.tools.refresh', async () => {
        await toolsProvider?.refresh();
    });

    const disposableRun = vscode.commands.registerCommand('systemMcp.tools.run', async (item?: ToolItem) => {
        if (!toolsProvider) return;
        const name = item?.tool?.name ?? await vscode.window.showInputBox({ prompt: 'Tool name to run' });
        if (!name) return;
        try {
            await toolsProvider.runTool(name);
        } catch (err: any) {
            vscode.window.showErrorMessage(`Tool failed: ${err?.message ?? err}`);
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
                    panel.webview.html = `<!DOCTYPE html><html><body style="margin:0"><img src="${dataUri}" style="max-width:100%; max-height:100vh;" /></body></html>`;
            } else {
                vscode.window.showWarningMessage('Screenshot tool did not return an image');
            }
        } catch (err: any) {
            vscode.window.showErrorMessage(`Failed to take screenshot: ${err?.message ?? err}`);
        }
    });

    context.subscriptions.push(disposableConnect, disposableListTools, disposableScreenshot, disposableRefresh, disposableRun);
}

export function deactivate() {
    // StdioClientTransport doesn't expose kill here; process exits when VS Code unloads.
    client = null;
}

type Tool = { name: string; description?: string };

class ToolItem extends vscode.TreeItem {
    constructor(public tool: Tool) {
        super(tool.name, vscode.TreeItemCollapsibleState.None);
        this.description = tool.description;
        this.contextValue = 'systemMcpTool';
        this.command = {
            title: 'Run Tool',
            command: 'systemMcp.tools.run',
            arguments: [this],
        };
        this.iconPath = new vscode.ThemeIcon('tools');
    }
}

class ToolsProvider implements vscode.TreeDataProvider<ToolItem> {
    private _onDidChangeTreeData = new vscode.EventEmitter<void>();
    readonly onDidChangeTreeData = this._onDidChangeTreeData.event;
    constructor(private loader: () => Promise<Tool[]>, private runner: (toolName: string) => Promise<void>) {}
    async refresh() { this._onDidChangeTreeData.fire(); }
    getTreeItem(element: ToolItem): vscode.TreeItem { return element; }
    async getChildren(): Promise<ToolItem[]> {
        try {
            const tools = await this.loader();
            return tools.map(t => new ToolItem(t));
        } catch (e: any) {
            vscode.window.showErrorMessage(`Failed to load tools: ${e?.message ?? e}`);
            return [];
        }
    }
    async runTool(name: string) {
        await this.runner(name);
    }
}

function showToolResult(title: string, result: any) {
    const output: any = (result as any).output ?? {};
    const content = Array.isArray(output.content) ? output.content[0] : undefined;
    if (content?.type === 'image') {
        const dataUri = content.data?.startsWith('data:') ? content.data : `data:image/${content.mimeType ?? 'png'};base64,${content.data}`;
        const panel = vscode.window.createWebviewPanel('systemMcpResult', `Tool: ${title}`, vscode.ViewColumn.Active, {});
            panel.webview.html = `<!DOCTYPE html><html><body style="margin:0"><img src="${dataUri}" style="max-width:100%; max-height:100vh;" /></body></html>`;
    } else if (content?.type === 'text') {
        vscode.window.showInformationMessage(`${title}: ${content.text?.slice(0, 500)}`);
    } else {
        const outputChannel = vscode.window.createOutputChannel('System MCP');
        outputChannel.appendLine(JSON.stringify(result, null, 2));
        outputChannel.show(true);
    }
}
