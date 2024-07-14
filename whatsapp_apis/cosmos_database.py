import os
from dotenv import load_dotenv
from datetime import datetime
import uuid
import requests
import json
import azure.cosmos.cosmos_client as cosmos_client

load_dotenv()

class CosmoDataBase():

    def __init__(self):
        self.cosmo_db_url = os.getenv('COSMOS_DB_URL')
        self.cosmo_db_key = os.getenv('COSMOS_DB_KEY')
        self.cosmo_db_name = os.getenv('COSMOS_DB_NAME')

    def get_cosmos_db_user(self, db_container, display_phone_number):

        client = cosmos_client.CosmosClient(self.cosmo_db_url, credential=self.cosmo_db_key, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
        db = client.get_database_client(self.cosmo_db_name)
        container = db.get_container_client(db_container)
        # Define the query to filter by display_phone_number
        query = f"SELECT * FROM c WHERE c.display_phone_number = '{display_phone_number}'"
        # Execute the query
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        
        if items:
            return {
                'status': True,
                'items': items
            
            }
        else:
            return {
                'status': False,
                'items': []
            }
        
    def get_save_cosmos_db_history_chat(self, db_container, body_response):

        client = cosmos_client.CosmosClient(self.cosmo_db_url, credential=self.cosmo_db_key, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
        db = client.get_database_client(self.cosmo_db_name)
        container = db.get_container_client(db_container)

        from_ = body_response['from']
        timestamp_str = body_response['timestamp']
        text_ = body_response['text']
        typeuser_ = body_response['typeuser']
        message_id_= body_response['message_id']
        type_= body_response['type']

        # Ensure timestamp_str is a string
        if not isinstance(timestamp_str, str):
            timestamp_str = str(timestamp_str)
            
        # Convert timestamp string to datetime object
        try:
            timestamp_ = datetime.fromisoformat(timestamp_str)
        except ValueError:
            timestamp_ = datetime.utcnow()

        query = f"SELECT * FROM c WHERE c['from'] = '{from_}'"
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        if items:
            # Conversation exists, update it
            item = items[0]
            for entry in item['history']:
                if entry['message_id_'] == message_id_ and entry['role'] == 'assistant': 
                    return {
                        'created': False,
                        'updated': False,
                        'history': item['history'],
                        'replacted': True
                    }
            history_entry = {
                'role': typeuser_,
                'content': text_,
                'timestamp': timestamp_.isoformat(),
                'message_id_' : message_id_
            }
            item['history'].append(history_entry)
            container.replace_item(item=item, body=item)
            return {
                'created': False,
                'updated': True,
                'history': item['history'],
                'replacted': False
                }
        else:
            new_conversation = {
                'id': str(uuid.uuid4()),
                'session': str(uuid.uuid4()),
                'from': from_,
                'created_at': datetime.utcnow().isoformat(),
                'history': [{
                    'role': typeuser_,
                    'content': text_,
                    'timestamp': timestamp_.isoformat(),
                    'message_id_' : message_id_,
                    'type': type_
                }]
            }
            container.create_item(body=new_conversation)
            return {
                'created': True,
                'updated': False,
                'history': new_conversation['history'],
                'replacted': False
            }
