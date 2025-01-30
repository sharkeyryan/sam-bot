import requests
import json

# Ollama API endpoint
OLLAMA_API_GENERATE_URL = "http://localhost:11434/api/generate"
OLLAMA_API_CHAT_URL = "http://localhost:11434/api/chat"

class SamChat:
    def __init__(self, model="llama3.2:1b"):
        self.name = "Sam"
        self.system_message_prompt = f"You are randomly generated person simply named '{self.name}'. You will aquire a persona for itself including an age, race, gender, job description, education level, hobbies, interests, skills, passions, religious beliefs, personal qualities and aspirations."
        self.model = model
        self.conversation_history = []
        self.context = []
        self.options = {
            "num_keep": 5,
            "seed": 42,
            "num_predict": 100,
            "top_k": 20,
            "top_p": 0.9,
            "min_p": 0.0,
            "typical_p": 0.7,
            "repeat_last_n": 33,
            "temperature": 0.8,
            "repeat_penalty": 1.2,
            "presence_penalty": 1.5,
            "frequency_penalty": 1.0,
            "mirostat": 1,
            "mirostat_tau": 0.8,
            "mirostat_eta": 0.6,
            "penalize_newline": True,
            "stop": ["\n", "user:"],
            "numa": False,
            "num_ctx": 1024,
            "num_batch": 2,
            "num_gpu": 1,
            "main_gpu": 0,
            "low_vram": False,
            "vocab_only": False,
            "use_mmap": True,
            "use_mlock": False,
            "num_thread": 8
        }

    def generate_system_message(self):
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "prompt": self.system_message_prompt,
            "stream": False
        }
        
        if self.context:
            data["context"] = self.context
        
        try:
            response = requests.post(OLLAMA_API_GENERATE_URL, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            
            result = response.json()
            self.context = result.get('context', [])
            
            system_message = result['response'] 
            
            print(f"Generated system message: {system_message}")

            self.conversation_history.append({"role": "system", "content": system_message})
        
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to LLM API: {e}")
            return None
    
    def generate_response(self, prompt):
        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "messages": self.conversation_history + [{"role": "user", "content": prompt}],
            "stream": False,
            "options": self.options
        }
        
        if self.context:
            data["context"] = self.context
        
        try:
            response = requests.post(OLLAMA_API_CHAT_URL, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            
            result = response.json()
            self.context = result.get('context', [])
            
            assistant_message = result['message']['content']
            self.conversation_history.append({"role": "user", "content": prompt})
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            return assistant_message
        
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to LLM API: {e}")
            return None

if __name__ == "__main__":
    chat = SamChat()

    chat.generate_system_message()

    # print("Hi! My name is " + chat.name + ". Nice to meet you.")
    print("\nType 'quit' to exit.")
    print("\n----------------------------------------")
    
    while True:
        user_prompt = input("\nYou: ")
        
        if user_prompt.lower() == 'quit':
            print("Nice to meet you. Have a good day!")
            break
        
        response = chat.generate_response(user_prompt)
        
        if response:
            print("\n----------------------------------------\n")
            print(chat.name + ": " + response)
        else:
            print("Failed to get a response from " + chat.name + ".")
        
        # Add some newlines and underscores to make it easier to read
        print("\n----------------------------------------")

            
