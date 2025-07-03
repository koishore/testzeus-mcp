#!/bin/bash
# install.sh - Setup script for Hercules MCP Server

set -e

echo "🧪 Setting up Hercules MCP Server..."

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Need Python 3.8+, found: $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python: $PYTHON_VERSION"

# Install Python stuff
echo "📦 Installing Python dependencies..."
python3 -m pip install --upgrade pip
pip install -r requirements.txt

# Dev dependencies if requested
if [ "$1" = "--dev" ]; then
    echo "📦 Installing dev dependencies..."
    pip install pytest pytest-asyncio black isort flake8
fi

# Check for Node.js (for VSCode extension)
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✅ Node.js: $NODE_VERSION"
    
    echo "📦 Installing VSCode extension deps..."
    cd vscode-extension
    npm install
    
    # Install vsce if needed
    if ! command -v vsce &> /dev/null; then
        echo "📦 Installing vsce..."
        npm install -g @vscode/vsce
    fi
    
    echo "🔨 Building extension..."
    npm run compile
    
    echo "📦 Packaging extension..."
    vsce package
    
    cd ..
    
    echo "✅ Extension built: vscode-extension/hercules-mcp-extension-1.0.0.vsix"
else
    echo "⚠️  Node.js not found - skipping VSCode extension"
    echo "   Install Node.js 16+ to build the extension"
fi

# Check for Hercules
if command -v hercules &> /dev/null; then
    HERCULES_VERSION=$(hercules --version 2>/dev/null || echo "unknown")
    echo "✅ Hercules: $HERCULES_VERSION"
else
    echo "⚠️  Hercules not found - will use simulation mode"
    echo "   Get it at: https://github.com/test-zeus-ai/testzeus-hercules"
fi

# Create temp dirs
echo "📁 Creating test directories..."
mkdir -p /tmp/hercules_tests
mkdir -p /tmp/hercules_results

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next:"
echo "1. Start server:      python src/main.py"
echo "2. Install extension: code --install-extension vscode-extension/hercules-mcp-extension-1.0.0.vsix"
echo "3. Try demo:         python demo_script.py"
echo ""
echo "See README.md for more details."