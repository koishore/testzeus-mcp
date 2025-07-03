// vscode-extension/src/testTreeProvider.ts
import * as vscode from 'vscode';
import * as path from 'path';
import { MCPClient } from './mcpClient';
import { TestCase, TestResult } from './types';

export class TestTreeProvider implements vscode.TreeDataProvider<TestTreeItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<TestTreeItem | undefined | null | void> = new vscode.EventEmitter<TestTreeItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<TestTreeItem | undefined | null | void> = this._onDidChangeTreeData.event;

    constructor(private mcpClient: MCPClient) {}

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: TestTreeItem): vscode.TreeItem {
        return element;
    }

    async getChildren(element?: TestTreeItem): Promise<TestTreeItem[]> {
        if (!element) {
            // Root level - show test categories
            return [
                new TestTreeItem('Test Cases', vscode.TreeItemCollapsibleState.Expanded, 'testCases'),
                new TestTreeItem('Test Results', vscode.TreeItemCollapsibleState.Expanded, 'testResults')
            ];
        }

        if (element.contextValue === 'testCases') {
            return this.getTestCases();
        }

        if (element.contextValue === 'testResults') {
            return this.getTestResults();
        }

        return [];
    }

    private async getTestCases(): Promise<TestTreeItem[]> {
        try {
            const response = await this.mcpClient.listTestCases();
            if (!response.success) {
                return [new TestTreeItem('Failed to load test cases', vscode.TreeItemCollapsibleState.None, 'error')];
            }

            return response.test_cases.map(testCase => {
                const item = new TestTreeItem(
                    testCase.name,
                    vscode.TreeItemCollapsibleState.None,
                    'testCase'
                );
                item.description = testCase.description;
                item.tooltip = `Steps: ${testCase.steps.length}\nCreated: ${testCase.created_at}`;
                item.iconPath = new vscode.ThemeIcon('beaker');
                item.command = {
                    command: 'hercules.openTestFile',
                    title: 'Open Test File',
                    arguments: [testCase.file_path]
                };
                item.testCase = testCase;
                return item;
            });
        } catch (error) {
            return [new TestTreeItem('Error loading test cases', vscode.TreeItemCollapsibleState.None, 'error')];
        }
    }

    private async getTestResults(): Promise<TestTreeItem[]> {
        try {
            const response = await this.mcpClient.listTestResults();
            if (!response.success) {
                return [new TestTreeItem('Failed to load test results', vscode.TreeItemCollapsibleState.None, 'error')];
            }

            return response.results.map(result => {
                const item = new TestTreeItem(
                    result.test_name,
                    vscode.TreeItemCollapsibleState.None,
                    'testResult'
                );
                
                const statusIcon = this.getStatusIcon(result.status);
                item.iconPath = new vscode.ThemeIcon(statusIcon);
                item.description = `${result.status} (${result.execution_time?.toFixed(2)}s)`;
                item.tooltip = `Status: ${result.status}\nExecution Time: ${result.execution_time?.toFixed(2)}s\nStarted: ${result.started_at}`;
                
                item.command = {
                    command: 'hercules.showResults',
                    title: 'Show Results',
                    arguments: [result.test_id]
                };
                item.testResult = result;
                return item;
            });
        } catch (error) {
            return [new TestTreeItem('Error loading test results', vscode.TreeItemCollapsibleState.None, 'error')];
        }
    }

    private getStatusIcon(status: string): string {
        switch (status) {
            case 'passed': return 'check';
            case 'failed': return 'x';
            case 'running': return 'sync';
            case 'error': return 'warning';
            default: return 'question';
        }
    }
}

class TestTreeItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState,
        public readonly contextValue: string
    ) {
        super(label, collapsibleState);
    }

    testCase?: TestCase;
    testResult?: TestResult;
}