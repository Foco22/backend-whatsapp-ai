import os
from dotenv import load_dotenv
from datetime import datetime
import uuid
import requests
import json

load_dotenv()

class WhatsappAPI:

    def __init__(self, body):
        self.body = body

    def detect_body(self):

        try:
            if 'entry' in self.body:
                for entry in self.body['entry']:
                    if 'changes' in entry:
                        for change in entry['changes']:
                            if 'value' in change and 'messages' in change['value']:
                                json_ = {}
                                json_= change['value']['messages'][0]
                                json_['metadata'] = change['value']['metadata']
                                json_['status'] = True
                                json_['type'] = change['value']['messages'][0]['type']
                                return json_
        except KeyError: 
            json_ = {}   
            json_['status'] = False
            json_['type'] = False
            json_['metadata'] = False
            return json_
        
        json_ = {}
        json_['status'] = False
        json_['type'] = False
        json_['metadata'] = False
        return json_
    

    def location_message(self, access_token, latitude, longitude, recipient_id, code_phone_from, name, address):
        
        url = 'https://graph.facebook.com/v19.0/{}/messages'.format(code_phone_from)
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "location",
            "location": {
                "latitude": latitude,
                "longitude": longitude,
                "name": name,
                "address": address
            }
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return {
            'status_code': response.status_code,
            'response': response
        }

    def buttom_message(self, access_token, recipient_id, code_phone_from, image_link, text_body, buttons_list):
        
        url = 'https://graph.facebook.com/v19.0/{}/messages'.format(code_phone_from)
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        # Create the payload
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_id,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "header": {
                    "type": "image",
                    "image": {
                        "link": image_link  # Replace with your image URL
                    }
                },
                "body": {
                    "text": text_body
                },
                "action": {
                    "buttons": buttons_list
                }
            }
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return {
            'status_code': response.status_code,
            'response': response
        }
    
    def list_message(self, access_token, recipient_id, code_phone_from, text_type, text_body, text_buttom, text_section, rows_list):
        
        url = 'https://graph.facebook.com/v19.0/{}/messages'.format(code_phone_from)
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        # Create the payload for list message
        payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_id,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
            "type": "text",
            "text": text_type
            },
            "body": {
            "text": text_body
            },
            "action": {
            "button": text_buttom,
            "sections": [
                {
                "title": text_section,
                "rows": rows_list
                }
            ]
            }
        }
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        return {
            'status_code': response.status_code,
            'response': response
        }
    

    def reply_message(self, access_token, recipient_id, code_phone_from, text_body, buttons_list, image_link):
        
        url = 'https://graph.facebook.com/v19.0/{}/messages'.format(code_phone_from)
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        # Create the payload
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_id,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "header": {
                    "type": "image",
                    "image": {
                        "link": image_link  
                    }
                },
                "body": {
                    "text": text_body
                },
                "action": {
                    "buttons":  buttons_list
                }
            }
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return {
            'status_code': response.status_code,
            'response': response
        }


    def text_message(self, access_token, recipient_id, code_phone_from, text_body):
        
        url = 'https://graph.facebook.com/v19.0/{}/messages'.format(code_phone_from)
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "text",
            "text": {
                "body": text_body
            }
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return {
            'status_code': response.status_code,
            'response': response
        }
