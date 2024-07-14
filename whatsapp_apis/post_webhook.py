import os
from dotenv import load_dotenv
from datetime import datetime
import uuid
import requests
import json
from azure.cosmos.exceptions import CosmosResourceNotFoundError
from datetime import datetime, timedelta
from whatsapp_apis.whatsapp import WhatsappAPI
from whatsapp_apis.llm import GroqModel
from whatsapp_apis.cosmos_database import CosmoDataBase
from pytz import timezone
import pytz
from datetime import datetime, timedelta
import logging

load_dotenv()

class PostWebhook:

    def __init__(self, body):
        self.body = body
        self.db_container_user = os.getenv('COSMOS_DB_CONTAINER_USER')
        self.db_container_chat_history = os.getenv('COSMOS_DB_CONTAINER_CHAT_HISTORY')
        self.access_token = os.getenv('PERMANENT_TOKEN_FACEBOOK')
        self.code_phone_from = os.getenv('CODE_PHONE_FROM')
        self.cosmos_db = CosmoDataBase() 
        
    def main(self):
        
        # Paso 1 - Detectar si el mensaje es un evento de WhatsApp (texto)
        detect_body_response = WhatsappAPI(self.body).detect_body()
        logging.info(f"detect_body_response: {detect_body_response}")
        if detect_body_response['status'] == True:

            recipient_id = detect_body_response['from']
            message_id_ = detect_body_response['id']
            timestamp_ = detect_body_response['timestamp']
            text_ = detect_body_response['text']['body']
            type_ = detect_body_response['type']
            metadata_ = detect_body_response['metadata']
            json_response = {'from': recipient_id, 'message_id': message_id_, 'timestamp': timestamp_, 'text': text_, 'type': type_, 'metadata': metadata_, 'typeuser': 'user'}
            
            # Paso 2 - Detectar si existe una conversacion anterior en Cosmos DB, sino  crearla.    
            response_detection_cosmo = self.cosmos_db.get_save_cosmos_db_history_chat(self.db_container_chat_history, json_response)
            history_ = response_detection_cosmo['history']

            # Paso 3 - Genearar una respuesta del modelo LLM.   
            response_llm_modelo = GroqModel(history_).main()['message']
            current_timestamp = datetime.utcnow().isoformat()
            json_response_assistant = {'from': recipient_id, 'message_id': message_id_, 'timestamp': current_timestamp, 'text': response_llm_modelo, 'type': type_, 'metadata': {}, 'typeuser': 'assistant'}
            response_db_assitante = self.cosmos_db.get_save_cosmos_db_history_chat(self.db_container_chat_history, json_response_assistant)
            if response_db_assitante['replacted'] == False:
               
                # Paso 4 - Enviar respuesta al usuario.  
                response_send_message = WhatsappAPI(self.body).text_message(self.access_token, recipient_id, self.code_phone_from, response_llm_modelo)
                return json.dumps({'status_code': 200, 'response': 'Message sent'})
            else:
                return json.dumps({'status_code': 200, 'response': 'Message already sent'})
        
        return json.dumps({'status_code': 200, 'response': 'Event saved'}, ensure_ascii=False)

