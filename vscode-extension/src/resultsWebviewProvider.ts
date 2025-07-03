// vscode-extension/src/resultsWebviewProvider.ts
import * as vscode from 'vscode';
import { MCPClient } from './mcpClient';
import { TestResult } from './types';

export class ResultsWebviewProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = 'herculesResults';
    private _view?: vscode.WebviewView;

    constructor(
        private readonly _extensionUri: vscode.Uri,
        private mcpClient: MCPClient
    ) {}

    public resolveWebviewView(
        webviewView: vscode.WebviewView,
        context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken,
    ) {
        this._view = webviewView;

        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this._extensionUri]
        };

        webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);

        webviewView.webview.onDidReceiveMessage(async data => {
            switch (data.type) {
                case 'refreshResults':
                    // Refresh results view
                    break;
            }
        });
    }

    public updateResults(result: TestResult) {
        if (this._view) {
            this._view.webview.postMessage({
                type: 'updateResults',
                result: result
            });
        }
    }

    private _getHtmlForWebview(webview: vscode.Webview) {
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Results</title>
    <style>
        body {
            font-family: var(--vscode-font-family);
            font-size: var(--vscode-font-size);
            color: var(--vscode-foreground);
            background-color: var(--vscode-editor-background);
            padding: 16px;
            margin: 0;
        }

        .result-container {
            border: 1px solid var(--vscode-panel-border);
            border-radius: 4px;
            padding: 16px;
            margin-bottom: 16px;
        }

        .result-header {
            display: flex;
            align-items: center;
            margin-bottom: 12px;
        }

        .status-badge {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            margin-right: 8px;
        }

        .status-passed {
            background-color: var(--vscode-testing-iconPassed);
            color: white;
        }

        .status-failed {
            background-color: var(--vscode-testing-iconFailed);
            color: white;
        }

        .status-running {
            background-color: var(--vscode-testing-iconRunning);
            color: white;
        }

        .status-error {
            background-color: var(--vscode-testing-iconErrored);
            color: white;
        }

        .result-info {
            display: grid;
            grid-template-columns: auto 1fr;
            gap: 8px;
            margin-bottom: 16px;
            font-size: 12px;
        }

        .info-label {
            font-weight: bold;
            color: var(--vscode-descriptionForeground);
        }

        .logs-container {
            background-color: var(--vscode-terminal-background);
            border: 1px solid var(--vscode-panel-border);
            border-radius: 4px;
            padding: 12px;
            font-family: var(--vscode-editor-font-family);
            font-size: 12px;
            max-height: 300px;
            overflow-y: auto;
        }

        .log-entry {
            margin-bottom: 4px;
            white-space: pre-wrap;
        }

        .error-message {
            background-color: var(--vscode-inputValidation-errorBackground);
            border: 1px solid var(--vscode-inputValidation-errorBorder);
            border-radius: 4px;
            padding: 8px;
            margin-bottom: 12px;
            color: var(--vscode-inputValidation-errorForeground);
        }

        .no-results {
            text-align: center;
            color: var(--vscode-descriptionForeground);
            padding: 32px;
        }
    </style>
</head>
<body>
    <div id="results-content">
        <div class="no-results">
            No test results to display.<br>
            Run a test to see results here.
        </div>
    </div>

    <script>
        const vscode = acquireVsCodeApi();
        
        window.addEventListener('message', event => {
            const message = event.data;
            
            switch (message.type) {
                case 'updateResults':
                    displayResult(message.result);
                    break;
            }
        });

        function displayResult(result) {
            const container = document.getElementById('results-content');
            
            const statusClass = 'status-' + result.status;
            const duration = result.execution_time ? result.execution_time.toFixed(2) + 's' : 'N/A';
            const startedAt = result.started_at ? new Date(result.started_at).toLocaleString() : 'N/A';
            const completedAt = result.completed_at ? new Date(result.completed_at).toLocaleString() : 'N/A';
            
            container.innerHTML = \`
                <div class="result-container">
                    <div class="result-header">
                        <span class="status-badge \${statusClass}">\${result.status.toUpperCase()}</span>
                        <strong>\${result.test_name}</strong>
                    </div>
                    
                    <div class="result-info">
                        <span class="info-label">Duration:</span>
                        <span>\${duration}</span>
                        <span class="info-label">Started:</span>
                        <span>\${startedAt}</span>
                        <span class="info-label">Completed:</span>
                        <span>\${completedAt}</span>
                        <span class="info-label">Test ID:</span>
                        <span>\${result.test_id}</span>
                    </div>

                    \${result.error_message ? \`
                        <div class="error-message">
                            <strong>Error:</strong> \${result.error_message}
                        </div>
                    \` : ''}

                    <div>
                        <strong>Execution Logs:</strong>
                        <div class="logs-container">
                            \${result.logs.map(log => \`<div class="log-entry">\${log}</div>\`).join('')}
                        </div>
                    </div>
                </div>
            \`;
        }
    </script>
</body>
</html>`;
    }
}