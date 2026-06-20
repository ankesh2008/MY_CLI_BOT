#!/bin/bash
# setup.sh — One-command project setup

echo ""
echo "🤖 Setting up DOST CLI Chatbot..."
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python version: $python_version"

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r req.txt -q

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next step: Set your OpenRouter API key:"
echo "  export OPENROUTER_API_KEY='your-key-here'"
echo ""
echo "Then run:"
echo "  python bot.py"
echo ""