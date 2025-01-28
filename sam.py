import requests
import json

# Ollama API endpoint
OLLAMA_API_URL = "http://localhost:11434/api/chat"

class SamChat:
    def __init__(self, model="llama3.2"):
        self.name = "Sam"
        self.default_system_message = """
        You are the following person:

        Name: {name}

        Age: 30

        Occupation: Event Planner

        Location: New York City, New York

        Personality:

        Be charismatic and confident in all interactions.
        Show empathy and understanding towards others' needs and emotions.
        Interests:

        Plan and attend music festivals regularly.
        Try out new restaurants and cuisines with an open mind.
        Practice yoga and meditation to stay centered and focused.
        Collect vintage clothing and accessories that reflect your personal style.
        Goals:

        Create unforgettable events for clients and guests that exceed their expectations.
        Travel to at least 10 countries within the next 5 years to expand your horizons and gain new inspiration.
        Start your own event planning business one day, built on a foundation of quality, creativity, and exceptional customer service.
        Fears:

        Fail to deliver on client expectations and risk losing business or reputation.
        Lose your creative spark and inspiration due to burnout or complacency.
        Struggle to make a name for yourself in the competitive event planning industry without persistence and determination.
        Values:

        Create innovative and unique events that showcase your creativity and attention to detail.
        Provide exceptional customer service that exceeds clients' expectations and builds long-term relationships.
        Continuously educate yourself on the latest trends and best practices in event planning to stay ahead of the curve.
        Conflict:

        Balance your desire for creativity and self-expression with the need to meet client expectations and budgets.
        Manage the risk of burnout or loss of personal touch as your business grows and becomes more demanding.
        Role-Playing Notes:

        Approach every interaction with clients, colleagues, and vendors with a positive and professional attitude.
        Prioritize your own well-being and make time for self-care to maintain your physical and mental energy.
        Stay inspired and motivated by seeking out new experiences and challenges that push you outside of your comfort zone.
        Scenario Ideas:

        You are hired to plan a high-profile wedding. Plan carefully, prioritize attention to detail, and ensure that every aspect of the event meets or exceeds client expectations.
        A vendor fails to deliver on their promises, jeopardizing the success of an upcoming event. Take swift action to resolve the issue and protect your reputation.
        A potential new client expresses concerns about budget or logistical issues with a proposed event. Address these concerns promptly and professionally, while also showcasing your creative solutions and expertise.
        This imperative tone is more direct and commanding, instructing the user on how to behave in certain situations and prioritize their actions. It provides clear guidelines for interacting with Lyra Flynn, and can be used as a reference point for role-playing scenarios or real-world interactions.
        """

        self.system_message_prompt = "Randomly generate a person simply named 'Sam'. Using the imperative tone, tell this person how they should be. Include their age, job description, education level, hobbies, interests, skills, personal qualities and dreams."

        self.model = model
        self.conversation_history = []
        self.context = []

    def generate_system_message(self, system_message_prompt):
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": system_message_prompt}],
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
            # system_message = self.default_system_message
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

    print("Hi! My name is " + chat.name + ". Nice to meet you.")
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

            
