// VSCode extension for Hercules MCP integration
// Main extension entry point

import * as vscode from 'vscode';
import { MCPClient } from './mcpClient';
import { TestTreeProvider } from './testTreeProvider';
import { ResultsWebviewProvider } from './resultsWebviewProvider';

let mcpClient: MCPClient;
let testTreeProvider: TestTreeProvider;
let resultsProvider: ResultsWebviewProvider;

export function activate(context: vscode.ExtensionContext) {
    console.log('Hercules MCP extension activated');

    // Get server URL from config
    const config = vscode.workspace.getConfiguration('hercules');
    const serverUrl = config.get<string>('mcpServerUrl', 'http://localhost:8000');
    
    mcpClient = new MCPClient(serverUrl);
    
    // Setup tree view for tests
    testTreeProvider = new TestTreeProvider(mcpClient);
    vscode.window.registerTreeDataProvider('herculesTests', testTreeProvider);
    
    // Setup results webview
    resultsProvider = new ResultsWebviewProvider(context.extensionUri, mcpClient);
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider('herculesResults', resultsProvider)
    );

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('hercules.createTest', createTestCase),
        vscode.commands.registerCommand('hercules.runTest', runTest),
        vscode.commands.registerCommand('hercules.refreshTests', () => testTreeProvider.refresh()),
        vscode.commands.registerCommand('hercules.showResults', showResults),
        vscode.commands.registerCommand('hercules.openTestFile', openTestFile),
    );

    // Auto-refresh if enabled
    const refreshInterval = config.get<number>('refreshInterval', 5000);
    if (config.get<boolean>('autoRefresh', true)) {
        setInterval(() => testTreeProvider.refresh(), refreshInterval);
    }
}

async function createTestCase() {
    try {
        // Get test details from user
        const name = await vscode.window.showInputBox({
            prompt: 'Test name',
            placeHolder: 'Login Flow Test'
        });
        if (!name) return;

        const description = await vscode.window.showInputBox({
            prompt: 'Test description',
            placeHolder: 'What does this test do?'
        });
        if (!description) return;

        const stepsInput = await vscode.window.showInputBox({
            prompt: 'Test steps (comma-separated)',
            placeHolder: 'Step 1, Step 2, Step 3'
        });
        if (!stepsInput) return;

        const expectedOutcome = await vscode.window.showInputBox({
            prompt: 'Expected outcome',
            placeHolder: 'What should happen?'
        });
        if (!expectedOutcome) return;

        const steps = stepsInput.split(',').map(s => s.trim());

        // Create via MCP
        const result = await mcpClient.createTestCase(name, description, steps, expectedOutcome);
        
        if (result.success) {
            vscode.window.showInformationMessage(`Created test: ${name}`);
            testTreeProvider.refresh();
        } else {
            vscode.window.showErrorMessage(`Failed: ${result.error}`);
        }
    } catch (error) {
        vscode.window.showErrorMessage(`Error: ${error}`);
    }
}

async function runTest(testId?: string) {
    try {
        if (!testId) {
            // Let user pick a test
            const tests = await mcpClient.listTestCases();
            if (!tests.success || tests.test_cases.length === 0) {
                vscode.window.showInformationMessage('No tests available');
                return;
            }

            const selected = await vscode.window.showQuickPick(
                tests.test_cases.map((test: any) => ({
                    label: test.name,
                    description: test.description,
                    testId: test.id
                })),
                { placeHolder: 'Pick test to run' }
            );

            if (!selected) return;
            testId = (selected as any).testId;
        }

        vscode.window.showInformationMessage('Running test...');
        const result = await mcpClient.runTest(testId!);
        
        if (result.success) {
            const status = result.result.status;
            const icon = status === 'passed' ? '✅' : status === 'failed' ? '❌' : '⚠️';
            vscode.window.showInformationMessage(`${icon} Test ${status}`);
            
            testTreeProvider.refresh();
            resultsProvider.updateResults(result.result);
        } else {
            vscode.window.showErrorMessage(`Test failed: ${result.error}`);
        }
    } catch (error) {
        vscode.window.showErrorMessage(`Error: ${error}`);
    }
}

async function showResults(testId?: string) {
    try {
        if (!testId) {
            const results = await mcpClient.listTestResults();
            if (!results.success || results.results.length === 0) {
                vscode.window.showInformationMessage('No results yet');
                return;
            }

            const selected = await vscode.window.showQuickPick(
                results.results.map((result: any) => ({
                    label: result.test_name,
                    description: `${result.status} - ${result.execution_time}s`,
                    testId: result.test_id
                })),
                { placeHolder: 'Pick result to view' }
            );

            if (!selected) return;
            testId = (selected as any).testId;
        }

        const result = await mcpClient.getTestResult(testId!);
        if (result.success) {
            resultsProvider.updateResults(result.result);
            vscode.commands.executeCommand('herculesResults.focus');
        }
    } catch (error) {
        vscode.window.showErrorMessage(`Error: ${error}`);
    }
}

async function openTestFile(filePath: string) {
    try {
        const uri = vscode.Uri.file(filePath);
        const doc = await vscode.workspace.openTextDocument(uri);
        await vscode.window.showTextDocument(doc);
    } catch (error) {
        vscode.window.showErrorMessage(`Can't open file: ${error}`);
    }
}

export function deactivate() {
    // cleanup
}