#!/bin/bash  # Shebang line: Yeh operating system ko batata hai ki is script ko execute karne ke liye Bash interpreter ka use karna hai.

# setup.sh — One-command project setup

echo ""  # Terminal par ek khali (blank) line print karta hai taaki output saaf aur organized dikhe.
echo " Setting up DOST CLI Chatbot..."  # User ko batane ke liye welcome message print karta hai ki setup shuru ho chuka hai.
echo ""  # Visual spacing ke liye ek aur khali line.

# Check Python version
# 'python3 --version' run karke uska output leta hai, aur 'cut' command se sirf main version number (jaise 3.10) nikal kar variable me save karta hai.
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python version: $python_version"  # Screen par screen par detected Python version dikhata hai taaki confirm ho sake ki Python installed hai.

# Install dependencies
echo "📦 Installing dependencies..."  # User ko status batata hai ki external packages/libraries install ho rahi hain.
pip install -r req.txt -q  # 'req.txt' me likhi dependencies ko install karta hai. '-q' (quiet) flag se faltu ka faltu logs terminal par nahi dikhta.

echo ""  # Visual spacing.
echo "✅ Setup complete!"  # Success milestone message jo batata hai ki setup bina kisi error ke poora ho gaya.
echo ""  # Visual spacing.
echo "Next step: Set your OpenRouter API key:"  # User ko agla step guide karne ke liye instruction text.
echo "  export OPENROUTER_API_KEY='your-key-here'"  # Terminal par exact command print karta hai jisse user environment variable me API key set kar sake.
echo ""  # Visual spacing.
echo "Then run:"  # Bot chalane ki instruction ka header.
echo "  python bot.py"  # Batata hai ki is command ko type karke chatbot ko start kiya ja sakta hai.
echo ""  # Final output ko clean rakhne ke liye aakhiri blank line.
