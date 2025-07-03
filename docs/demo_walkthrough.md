# TestZeus Hercules MCP Server - Demo Walkthrough

This document provides a step-by-step demonstration of the complete TestZeus Hercules MCP Server workflow, from test creation to execution and results viewing.

## 🎯 Demo Overview

The demo showcases the complete integration between:
- **MCP Server**: Core test management and execution
- **VSCode Extension**: Editor integration for authoring and viewing
- **Hercules Integration**: Actual test execution (with simulation fallback)

## 🚀 Prerequisites Setup

1. **Install the system:**
```bash
git clone <repository-url>
cd hercules-mcp-server
chmod +x install.sh
./install.sh
```

2. **Start the MCP server:**
```bash
python src/main.py
# Server starts on http://localhost:8000
```

3. **Install VSCode extension:**
```bash
code --install-extension vscode-extension/hercules-mcp-extension-1.0.0.vsix
```

## 📝 Part 1: Test Authoring in Editor

### Via VSCode Extension

1. **Open VSCode and access Hercules features:**
   - Open Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
   - Type "Hercules" to see available commands

2. **Create a new test case:**
   - Run command: `Hercules: Create Test Case`
   - Enter test details:
     ```
     Name: Login Flow Test
     Description: Validates user authentication workflow
     Steps: Navigate to login page, Enter credentials, Click login, Verify dashboard
     Expected Outcome: User successfully authenticates and accesses dashboard
     ```

3. **View the created test:**
   - Check the "Hercules Tests" panel in Explorer
   - Test appears under "Test Cases" section
   - Click to open the generated test file

### Via Command Line (Alternative)

```bash
# Create test using VSCode integration script
python vscode_plugin.py create --file sample_test.py
```

## 🔄 Part 2: Triggering Test via MCP

### Method 1: VSCode Extension
1. **Navigate to test tree:**
   - Open "Hercules Tests" panel
   - Find your "Login Flow Test" under Test Cases

2. **Execute the test:**
   - Right-click on test case
   - Select "Run Test"
   - Extension sends MCP request to server

3. **Monitor execution:**
   - Status updates in real-time in test tree
   - Running indicator (🔄) appears during execution

### Method 2: Direct MCP API
```bash
# If using curl to test MCP endpoints directly
curl -X POST http://localhost:8000/tools/run_test \
  -H "Content-Type: application/json" \
  -d '{"arguments": {"test_id": "your-test-id"}}'
```

### Method 3: Demo Script
```bash
# Run the comprehensive demo
python demo_script.py
```

## 📊 Part 3: Live Results in Editor

### VSCode Results Panel

1. **Access results view:**
   - Results automatically appear in "Test Results" webview
   - Or manually open via Command Palette: `Hercules: Show Results`

2. **View detailed results:**
   - **Status Badge**: ✅ Passed / ❌ Failed / 🔄 Running / ⚠️ Error
   - **Execution Details**: Duration, start/end times, test ID
   - **Execution Logs**: Step-by-step execution trace
   - **Error Information**: Detailed error messages if failed

3. **Interactive features:**
   - Click on test results to view details
   - Refresh automatically or manually
   - Filter by status or date

### Example Result Display

```
🧪 Login Flow Test
Status: ✅ PASSED
Duration: 2.34s
Started: 2025-01-15 10:30:45
Completed: 2025-01-15 10:30:47

Execution Logs:
1. Starting test: Login Flow Test
2. Description: Validates user authentication workflow  
3. Step 1: Navigate to login page
4. Step 2: Enter credentials
5. Step 3: Click login
6. Step 4: Verify dashboard
7. Verifying expected outcome: User successfully authenticates
8. ✓ Test passed successfully
```

## 🎬 Complete Demo Flow

### Scenario: E-commerce Site Testing

Let's create and run a comprehensive test for an e-commerce website:

1. **Create Product Search Test:**
```
Name: Product Search and Purchase
Description: Test complete user journey from search to purchase
Steps:
  - Navigate to homepage
  - Search for "laptop"
  - Filter results by price range
  - Select product
  - Add to cart
  - Proceed to checkout
  - Enter shipping information
  - Complete purchase
Expected Outcome: Order confirmation displayed with order number
```

2. **Execute via VSCode:**
   - Test appears in Hercules Tests panel
   - Right-click → "Run Test"
   - Watch real-time status updates

3. **View Results:**
   - Detailed execution log in Results panel
   - Performance metrics (execution time)
   - Screenshots (if Hercules captures them)
   - Error details (if any step fails)

## 🔧 Behind the Scenes

### What Happens During Execution

1. **MCP Server receives request** from VSCode extension
2. **Test file generation** - Python Hercules test class created
3. **Hercules execution** - CLI command runs the test
4. **Result collection** - Logs, status, timing captured
5. **Response formatting** - Structured data returned to extension
6. **UI updates** - VSCode displays real-time results

### Generated Test File Example

```python
"""
Test Case: Product Search and Purchase
Description: Test complete user journey from search to purchase
Generated: 2025-01-15T10:30:45Z
"""

from hercules import HerculesTest

class Product_Search_and_PurchaseTest(HerculesTest):
    def __init__(self):
        super().__init__()
        self.test_name = "Product Search and Purchase"
        self.test_id = "uuid-12345"

    def setup(self):
        self.log("Setting up test environment…")

    def execute(self):
        self.log("Starting test execution…")
        
        self.log("Step 1: Navigate to homepage")
        self.execute_step("Navigate to homepage")
        
        self.log("Step 2: Search for laptop")
        self.execute_step("Search for laptop")
        
        # ... more steps
        
        self.log("Verifying expected outcome…")
        self.verify_outcome("Order confirmation displayed with order number")

    def teardown(self):
        self.log("Cleaning up test environment…")

if __name__ == "__main__":
    Product_Search_and_PurchaseTest().run()
```

## 🎯 Key Demo Points

### For Technical Evaluation

1. **MCP Protocol Compliance**: Standard tool definitions and responses
2. **Editor Integration**: Native VSCode experience with proper UI components
3. **Hercules Integration**: Real CLI execution with fallback simulation
4. **Error Handling**: Graceful handling of various failure scenarios
5. **Real-time Updates**: Live status and result streaming

### For User Experience

1. **Intuitive Workflow**: Natural test authoring → execution → results flow
2. **Visual Feedback**: Clear status indicators and rich result display
3. **Productivity Features**: Command palette, context menus, auto-refresh
4. **Professional UI**: Modern webview with proper styling and layout

## 📈 Extending the Demo

### Advanced Scenarios

1. **Concurrent Testing**: Run multiple tests simultaneously
2. **Test Suites**: Group related tests together
3. **CI Integration**: Trigger tests from GitHub Actions
4. **AI-Powered**: Use Claude/GPT to generate test steps

### Custom Test Types

1. **API Testing**: REST endpoint validation
2. **Performance Testing**: Load and stress testing  
3. **Mobile Testing**: Cross-platform mobile app testing
4. **Accessibility Testing**: WCAG compliance validation

---

**This demo showcases a production-ready MCP server with full editor integration, ready for AI-powered testing workflows.**