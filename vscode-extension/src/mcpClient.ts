// vscode-extension/src/mcpClient.ts
import axios, { AxiosInstance } from 'axios';
import { TestCase, TestResult, MCPResponse } from './types';

export class MCPClient {
    private client: AxiosInstance;

    constructor(private serverUrl: string) {
        this.client = axios.create({
            baseURL: serverUrl,
            timeout: 30000,
            headers: {
                'Content-Type': 'application/json'
            }
        });
    }

    async createTestCase(
        name: string,
        description: string,
        steps: string[],
        expectedOutcome: string
    ): Promise<MCPResponse<{ test_case: TestCase }>> {
        try {
            const response = await this.client.post('/tools/create_test_case', {
                arguments: {
                    name,
                    description,
                    steps,
                    expected_outcome: expectedOutcome
                }
            });
            return response.data;
        } catch (error) {
            return {
                success: false,
                error: error instanceof Error ? error.message : 'Unknown error'
            };
        }
    }

    async runTest(testId: string): Promise<MCPResponse<{ result: TestResult }>> {
        try {
            const response = await this.client.post('/tools/run_test', {
                arguments: { test_id: testId }
            });
            return response.data;
        } catch (error) {
            return {
                success: false,
                error: error instanceof Error ? error.message : 'Unknown error'
            };
        }
    }

    async getTestResult(testId: string): Promise<MCPResponse<{ result: TestResult }>> {
        try {
            const response = await this.client.post('/tools/get_test_result', {
                arguments: { test_id: testId }
            });
            return response.data;
        } catch (error) {
            return {
                success: false,
                error: error instanceof Error ? error.message : 'Unknown error'
            };
        }
    }

    async listTestCases(): Promise<MCPResponse<{ test_cases: TestCase[], count: number }>> {
        try {
            const response = await this.client.post('/tools/list_test_cases', {
                arguments: {}
            });
            return response.data;
        } catch (error) {
            return {
                success: false,
                error: error instanceof Error ? error.message : 'Unknown error',
                test_cases: [],
                count: 0
            };
        }
    }

    async listTestResults(): Promise<MCPResponse<{ results: TestResult[], count: number }>> {
        try {
            const response = await this.client.post('/tools/list_test_results', {
                arguments: {}
            });
            return response.data;
        } catch (error) {
            return {
                success: false,
                error: error instanceof Error ? error.message : 'Unknown error',
                results: [],
                count: 0
            };
        }
    }

    async getTestStatus(testId: string): Promise<MCPResponse<{
        status: string,
        started_at?: string,
        completed_at?: string,
        execution_time?: number
    }>> {
        try {
            const response = await this.client.post('/tools/get_test_status', {
                arguments: { test_id: testId }
            });
            return response.data;
        } catch (error) {
            return {
                success: false,
                error: error instanceof Error ? error.message : 'Unknown error'
            };
        }
    }
}