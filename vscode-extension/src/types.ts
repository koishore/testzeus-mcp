// vscode-extension/src/types.ts
import * as vscode from 'vscode';

export interface TestCase {
    id: string;
    name: string;
    description: string;
    steps: string[];
    expected_outcome: string;
    created_at: string;
    file_path?: string;
}

export interface TestResult {
    test_id: string;
    test_name: string;
    status: 'running' | 'passed' | 'failed' | 'error';
    logs: string[];
    screenshots: string[];
    error_message?: string;
    execution_time?: number;
    started_at?: string;
    completed_at?: string;
}

export interface MCPResponse<T = any> {
    success: boolean;
    error?: string;
    message?: string;
}

export interface MCPResponse<T> extends Record<string, any> {
    success: boolean;
    error?: string;
    message?: string;
}

export interface TestCaseItem extends vscode.TreeItem {
    testCase: TestCase;
}

export interface TestResultItem extends vscode.TreeItem {
    testResult: TestResult;
}