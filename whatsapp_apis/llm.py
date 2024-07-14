import os
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class GroqModel:

    def __init__(self, history):
        self.history = history
        self.api_groq = os.getenv('API_KEY_GROQ')
        self.model_groq = 'llama3-8b-8192'
        self.max_history = 10

    def main(self):
        
        try:
            self.history = self.history[-self.max_history:]
            history  = []
            for entry in self.history:
                json_ = {
                    'role': entry['role'],
                    'content': entry['content']
                }
                history.append(json_)
            
            client = Groq(
                api_key= self.api_groq,
            )       
            history_system = [{"role": "system", "content": "You are a useful assistant. You always answer in Spanish. Be kind and respectful."}]
            chat_completion = client.chat.completions.create(
                messages=history_system + history,
                model=self.model_groq,
            )
            return {
                'message': chat_completion.choices[0].message.content
            }
        except Exception as e:
            return {
                'message': 'Disculpa, no puedo responder a eso en este momento.'
            }
