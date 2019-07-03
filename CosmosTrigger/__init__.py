import logging
import os
import simplecrypt
import json
from base64 import b64encode

import azure.functions as func


def main(documents: func.DocumentList, outputDocument: func.Out[func.Document]) -> str:
        if documents:
                logging.info('Document id: %s', documents[0].data['id'])
        
        # get the encryption key
        encryption_key = os.environ.get('ENCRYPT_KEY', 'some-default-key')

        # encrypt the body
        encrypted_body = simplecrypt.encrypt(encryption_key, documents[0].data['body'])

        base64_bytes = b64encode(encrypted_body)
        base64_string = base64_bytes.decode('utf-8')


        outputDocument.set(func.Document.from_dict({ 
                "id": documents[0].data['id'],
                "encryptedBody": base64_string}))