import os #used to set environment to use openrouter's API key
import sys #system specific commands aur function ko control karne ke liye
import requests #used to get response from Openrouter API from http post
from datetime import datetime #for timestamps 
#Emoji printing ke time Unicode error na aa jaye
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8') #output -> UTF-8 taaki emoji crash na kare
        sys.stderr.reconfigure(encoding='utf-8') #error -> UTF-8
    except Exception: #if terminal can't support reconfigure
        pass
#get OPenRouter API key from env. and if can't find then use a placeholder value
API_KEY = os.getenv("OPENROUTER_API_KEY", "PASTE_YOUR_OpenRouter_API_KEY_Here")
MAX_HISTORY_TURNS = 10 #conversation ko max. 10 turns tak rakhta hai
MODEL_NAME  = "openai/gpt-4o-mini" #uses to call specific model
#prompt which tells system how  to respond in front of user
SYSTEM_PROMPT = """You are DOST, an emotionally intelligent AI assistant.
 
MOOD DETECTION & ADAPTATION:
- Detect the user's mood from their words, punctuation, and tone in every message.
- Silently adapt your reply style based on what you detect. Never say "I can tell you're sad" — just respond accordingly.
 
Mood → How to respond:
- Happy / excited  → Match their energy. Be enthusiastic, use light humor, keep it fun.
- Sad / down       → Be warm and gentle. Shorter sentences. Acknowledge feelings before giving info.
- Frustrated       → Stay calm and patient. Don't over-explain. Be direct and solution-focused.
- Confused         → Slow down. Use simple words, analogies, and step-by-step structure.
- Curious          → Go deeper. Give interesting context, examples, and invite follow-up questions.
- Stressed / urgent → Be quick and clear. Bullet points over paragraphs. No filler words.
- Neutral          → Be helpful and concise. Balanced tone.
 
ALWAYS:
- Remember everything said earlier in the conversation and reference it naturally.
- Never say "As an AI..." or announce that you are adapting your tone.
- If you don't know something, say so honestly.
- Keep replies focused — don't ramble."""
def setup_model(): #ek functional hai to setup + initialise kaene mein kaam aayega
    if not API_KEY: #agar api key khali milti hai
        print("\n ERROR: OPENROUTER_API_KEY not found. Set it and retry.")
        print("Export it as OPENROUTER_API_KEY in your environment.")
        exit(1) #status code if 1 then exit

    class OpenRouterModel: #openrouter api key ke saath ineract karne ke liye ek blueprint hai 
        def __init__(self, api_key, model_name, system_instruction=None):
            self.api_key = api_key
            self.model_name = model_name
            self.system_instruction = system_instruction
            self.endpoint = "https://openrouter.ai/api/v1/chat/completions" #chat api of openrouter where the request should be send


        def generate_content(self, history: list): #take context from history 
            messages = []
            # convert internal history to chat messages
            for msg in history:
                role = "user" if msg.get("role") == "user" else "assistant"
                content = msg.get("parts", [""])[0]
                messages.append({"role": role, "content": content})

            # ensure system instruction is first message if provided
            if self.system_instruction: #list mein index 0 par system prompt lagata hai 
                messages.insert(0, {"role": "system", "content": self.system_instruction})

            payload = {"model": self.model_name, "messages": messages} #requested body taiyaar karta hai json format mein
            headers = {
                "Authorization": f"Bearer {self.api_key}", #API key ko autorisation header mein pass karta hai 
                "Content-Type": "application/json" #tells the server that the format is in json format 
            }

            #Timeout limmit ke saath OpenROuter endpoint par HTTP PoST request karta hhai


            resp = requests.post(self.endpoint, headers=headers, json=payload, timeout=30)
            resp.raise_for_status() #handles the HTTP error
            data = resp.json() #converts the response in json format

            # to store AI generated text
            text = ""
            try: #extract results from OPenrouter's standard structure 2
                text = data["choices"][0]["message"]["content"]
            except Exception:
                try:
                    text = data["choices"][0].get("text", "") #to fetch text from other common format 
                except Exception:
                    text = str(data) #Agar kuch na mile toh poore raw response data ko string bana deta hai

            class Resp:  #response object jaisa structure mimic karne ke liye ek khali class
                pass

            r = Resp() #class ka ek instance banata hai
            r.text = text #Uss instance ke (.text) attribute me extracted reply daal deta hai
            return r #Taiyar kiya hua fake response object return karta hai
#setup_model func.  end mein initialised class instance main return karta hai
    return OpenRouterModel(API_KEY, MODEL_NAME, system_instruction=SYSTEM_PROMPT) 
def trim_history(history: list, max_turns: int) -> list: #token limit ko manage karne ke liye old memory ko delete kar deta hai yeh func.
    """Keeps the conversation history within token limits.
    Each 'turn' = 1 user message + 1 model message = 2 items.
 
    This is the KEY concept: LLMs have a context window (token limit).
    Old messages must be dropped when history grows too large."""
    max_messages = max_turns * 2 #1 turn = 1 user msg + 1 model msg, toh max_messages total items count hoga
    if len(history) > max_messages: #Agar current history limit se zyada ho gayi ho
        trimmed = history[-max_messages:] #toh sirf sabse aakhiri ke relevant messages ko slice karke rakh leta hai
        print(f"\n [Memory] Trimmed history to last {max_turns} turns to manage tokens.\n") #User ko memory trim hone ka info message deta ha
        return trimmed
    return history #if not just return history 
def format_history_to_display(history:list) ->str: #Memory usage statistics ko acche format me screen par dikhane ke liye
    """Returns a readable summary of current memory usage"""
    turns = len(history)//2 #Total messages ko 2 se divide karke total turns calculate karta hai
    total_chars = sum( #claculate the total length of characters in prompt or msg
        len(msg["parts"][0]) if isinstance(msg["parts"][0], str) else 0
        for msg in history
    )
    approx_tokens = total_chars //4 #4 chr = 1 token
    return f"memory:{turns} turn(s) | ~{approx_tokens} tokens used" #returns a readable status string 
def chat(model, history: list, user_input: str) -> tuple[str, list]: #AI se chat karne aur history manage karne ka core function
    """
    Will send a message to Gemini with full conversation history.
    Returns (assistant_reply, updated_history).
    """
    
    history.append({ #Naye user input ko internal history list me format karke add karta hai
        "role": "user",
        "parts": [user_input]
    })
    try:
        # Send FULL history to model so it has context
        response = model.generate_content(history) #Poori updated history model ko bhejta hai context maintain rakhne ke liye.
        assistant_reply = response.text #Response se bot ka reply string nikalta hai    
 
        history.append({ #Bot ke reply ko internal history list me save karta hai agle turn ke liye
            "role": "model",
            "parts": [assistant_reply]
        })
 
        # Trim history to stay within token limits
        history = trim_history(history, MAX_HISTORY_TURNS)
 
        return assistant_reply, history
 
    except Exception as e: #Agar API call fail ho jaye ya internet down ho
        # Remove the user message we just added since request failed
        history.pop() #jo user message abhi append kiya tha use delete kar deta hai taaki history out-of-sync na ho
        raise e
 
def print_banner():
    """Prints the welcome banner."""
    print("\n" + "═" * 60)
    print("  🤖  DOST — CLI Chatbot with Memory")
    print(f"  Model: {MODEL_NAME} | Max memory: {MAX_HISTORY_TURNS} turns")
    print("═" * 60)
    print("  Commands:  'quit' or 'exit' → end session")
    print("             'clear'           → wipe memory")
    print("             'memory'          → show memory stats")
    print("             'history'         → show full conversation")
    print("═" * 60 + "\n")
def print_message(role: str, content: str, timestamp: str): #Chat messages ko formats aur word-wrap ke sath screen par sajane ke liye
    """Pretty-prints a chat message."""
    if role == "You":
        print(f"\n  [{timestamp}] 🧑 You:")
        print(f"  {content}")
    else:
        print(f"\n  [{timestamp}] 🤖 DOST:")
        # Word-wrap long responses for readability
        words = content.split() #Text ko individual words me todta hai
        line, lines = "", [] 
        for word in words:
            if len(line) + len(word) + 1 > 70: #Agar naya word jodne par line 70 characters se lambi ho rahi hai
                lines.append("  " + line)
                line = word # Nayi line naye word se shuru karta hai.
            else:
                line = (line + " " + word).strip()
        if line:
            lines.append("  " + line)
        print("\n".join(lines))
def main(): # Program ka main entry point jahan se execute shuru hota hai.
    print_banner() # Sabse pehle user ko welcome banner dikhata hai
    model = setup_model() # API validation ke baad OpenRouter model class ka instance store karta hai.
    history = [] # Chat start hote hi empty list banti hai memory hold karne ke liye.
 
    print("  DOST is ready! Start chatting.\n")
 
    while True: # Infinite loop jab tak user khud exit na kare.
        try:
            user_input = input("  You → ").strip() # User se input leta hai aur aage-piche ke extra spaces remove karta hai.
        except (KeyboardInterrupt, EOFError):
            print("\n\n  Goodbye! 👋\n")
            break
 
        if not user_input: # Agar user ne kuch nahi likha aur khali enter maar diya
            continue  #toh baaki loop skip karke seedha agle input par chala jata hai.
 
        timestamp = datetime.now().strftime("%H:%M:%S")
 
        # ── Handle special commands ──
        if user_input.lower() in ("quit", "exit"):
            print("\n  Goodbye! 👋\n")
            break
 
        elif user_input.lower() == "clear": # Agar user memory fresh karna chahta hai
            history = [] # History list ko fir se empty reset kar deta hai
            print("\n  ✅ Memory cleared. Starting fresh!\n")
            continue # Agle input turn par jump kar jata hai
 
        elif user_input.lower() == "memory":
            print(f"\n  📊 {format_history_to_display(history)}\n") # formatting function ka result print karta hai
            continue # Request complete wapas loop ke shuru me jata hai
 
        elif user_input.lower() == "history": # Agar poori lambi conversation dekhni ho
            if not history: # Check karta hai agar memory me abhi tak koi chat hi nahi hui
                print("\n  No conversation history yet.\n")
            else:
                print("\n  ── Conversation History ──")
                for msg in history: # Memory ke saare puraane messages par iterate karta hai.
                    role = "You" if msg["role"] == "user" else "DOST"
                    # Har message ke sirf starting 200 characters hi preview dikhata hai taaki terminal screen flood na ho
                    content = msg["parts"][0]
                    print(f"\n  {role}: {content[:200]}{'...' if len(content) > 200 else ''}")
                print()
            continue
 
        # ── Send message to Gemini ──
        print_message("You", user_input, timestamp) # User ka type kiya message terminal par standard format me print karta hai
        print("\n  DOST is thinking...", end="\r")
 
        try:
            reply, history = chat(model, history, user_input) # Chat function ke zariye API response aur updated memory mangwata hai.
            reply_time = datetime.now().strftime("%H:%M:%S") # Reply aate hi uska fresh timestamp note karta hai
            print(" " * 30, end="\r")   # Clear "thinking" text
            print_message("DOST", reply, reply_time)
 
        except Exception as e: # Agar request ke time network flatline ho jaye ya key glitched ho error print karta hai debugging ke liye
            print(f"\n  ❌ Error: {e}\n") # Yeh ensure karta hai ki script tabhi chale jab ise directly run kiya jaye (na ki dusri file me import karke
            print("  Check your API key and internet connection.\n")
 
 
if __name__ == "__main__":
    main()
