import requests
import json

# Ollama API endpoint
OLLAMA_API_URL = "http://localhost:11434/api/chat"

class SamChat:
    def __init__(self, model="llama3.2:1b"):
        self.name = "Sam"
        self.system_message_prompt = "You are a randomly generated person simply named 'Sam'. Generate a persona for yourself including your age, race, gender, job description, education level, hobbies, interests, skills, passions, religious beliefs, personal qualities and aspirations."

        self.model = model
        self.conversation_history = []
        self.context = []

    def generate_system_message(self, system_message_prompt):
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [{"role": "system", "content": system_message_prompt}],
            "stream": False
        }
        
        if self.context:
            data["context"] = self.context
        
        try:
            response = requests.post(OLLAMA_API_URL, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            
            result = response.json()
            self.context = result.get('context', [])
            
            system_message = result['message']['content'] 
            
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
            "stream": False
        }
        
        if self.context:
            data["context"] = self.context
        
        try:
            response = requests.post(OLLAMA_API_URL, headers=headers, data=json.dumps(data))
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

    chat.generate_system_message(chat.system_message_prompt)

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

            
