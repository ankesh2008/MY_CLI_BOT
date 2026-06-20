#  DOST — CLI Chatbot with Memory

A terminal-based AI chatbot powered by **OpenRouter API** that maintains conversation context across multiple turns with intelligent token/memory management and **mood-adaptive responses**.

> Built as Project 1 of my AI/LLM Engineering portfolio — 2nd year B.E. student.

---

##  Demo

<img width="1358" height="719" alt="image" src="https://github.com/user-attachments/assets/72404bc8-b5f6-4644-868c-3ed364d5c535" />


```
════════════════════════════════════════════════════════════
  🤖  DOST — CLI Chatbot with Memory
  Model: openrouter | Max memory: 10 turns
════════════════════════════════════════════════════════════
  Commands:  'quit' or 'exit' → end session
             'clear'           → wipe memory
             'memory'          → show memory stats
             'history'         → show full conversation
════════════════════════════════════════════════════════════

  You → ugh nothing is working i give up

  🤖 DOST:
  Hey, that sounds really frustrating. Let's slow down
  and figure this out together — what's the part that
  isn't working?
```

---

## 🧠 Key Concepts Demonstrated

| Concept | Implementation |
|---|---|
| **LLM API Integration** | OpenRouter API via HTTP POST requests |
| **Multi-turn conversation** | Full `history` list sent on every request |
| **Context window management** | `trim_history()` — oldest turns dropped first |
| **Token estimation** | ~4 chars per token approximation |
| **System prompts** | Mood-adaptive personality via `SYSTEM_PROMPT` |
| **Prompt engineering** | 7-mood detection and response adaptation |
| **Error handling** | Try/catch with history rollback on failed requests |
| **Unicode handling** | UTF-8 reconfiguration for emoji support on Windows |

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/ankesh2008/MY_CLI_BOT.git
cd dost-cli-chatbot
```

### 2. Install dependencies
```bash
pip install -r req.txt
```

Or use the setup script (Mac/Linux):
```bash
bash settingup.sh
```

### 3. Get your free OpenRouter API key
- Go to [openrouter.ai/keys](https://openrouter.ai/keys)
- Sign up for free → click **"Create Key"** → copy it

### 4. Set your API key

**Windows (Command Prompt):**
```bash
set OPENROUTER_API_KEY=your-api-key-here
```

**Windows (PowerShell):**
```bash
$env:OPENROUTER_API_KEY="your-api-key-here"
```

**Mac / Linux:**
```bash
export OPENROUTER_API_KEY="your-api-key-here"
```

### 5. Run the chatbot
```bash
python bot.py
```

---

## 💬 Chat Commands

| Command | What it does |
|---|---|
| `quit` / `exit` | End the session |
| `clear` | Wipe all memory and start fresh |
| `memory` | Show current token usage stats |
| `history` | Display full conversation so far |

---

## 🧩 How Memory Works

```
Turn 1:   [user msg 1] [model reply 1]
Turn 2:   [user msg 1] [model reply 1] [user msg 2] [model reply 2]
Turn 10:  [all 20 messages sent to the model]
Turn 11:  [oldest 2 messages DROPPED → still 20 messages total]
```

Every time you send a message, the **entire conversation history** is sent to the model. This is how LLMs appear to "remember" — they don't have memory built-in; we give them the full context on every call.

When history grows too large, we trim it from the oldest end to stay within the **context window** (token limit).

---

## 🎭 How Mood Adaptation Works

The system prompt instructs DOST to silently detect mood from word choice, punctuation, and tone — then adapt its reply style without ever announcing it.

| Detected Mood | DOST's Response Style |
|---|---|
| Happy / Excited | Enthusiastic, light humor |
| Sad / Down | Warm, gentle, short sentences |
| Frustrated | Calm, direct, solution-focused |
| Confused | Simple words, analogies, step-by-step |
| Curious | Deeper context, examples, follow-ups |
| Stressed / Urgent | Bullet points, no filler |
| Neutral | Concise and balanced |

---

## 📁 Project Structure

```
dost-cli-chatbot/
├── bot.py           # Main application
├── req.txt          # Python dependencies
├── settingup.sh     # One-command setup script (Mac/Linux)
└── README.md        # This file
```

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **OpenRouter API** — unified gateway to multiple LLMs (no vendor lock-in)
- **Requests** library for HTTP calls

---

## 📌 What I Learned

- How LLMs process conversation history as a list of messages
- What tokens are and why they matter for API costs and limits
- How to implement context window management in a real app
- The role of system prompts in shaping model behavior
- Prompt engineering for mood detection and tone adaptation
- Difference between embedding models and chat/generation models
- Error handling patterns for production AI applications
- UTF-8 encoding configuration for cross-platform emoji support

---

## ⚠️ Important: Choosing the Right Model

OpenRouter provides access to many models. Make sure to use a **chat/generation model**, not an embedding model.

✅ Works (chat models):
- `google/gemini-2.0-flash-exp`
- `meta-llama/llama-3.1-8b-instruct:free`
- `mistralai/mistral-7b-instruct:free`

❌ Won't work (embedding models — converts text to vectors, can't chat):
- `google/gemini-embedding-2`

---

## 🔮 Future Improvements

- [ ] Persistent memory across sessions (save/load history to JSON)
- [ ] Streaming responses (print token by token)
- [ ] Conversation export to `.txt` or `.md`
- [ ] Web UI using Flask + HTML/CSS/JS
- [ ] Switch models mid-conversation via command

---

## 📬 Connect with Me

- **LinkedIn:** [https://www.linkedin.com/in/ankesh-singh-9898503a6/]
- **GitHub:** [https://github.com/ankesh2008]
