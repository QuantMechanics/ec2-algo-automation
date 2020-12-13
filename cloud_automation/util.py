from pathlib import Path
import os
import sys
import json
from pathlib import Path
from threading import Thread
import requests


class clUtil():
    @staticmethod
    def get_project_root() -> Path:
        return Path(__file__).parent

    @staticmethod
    def loadJson(filename=""):  # This helps in reading JSON files
        with open(filename, mode="r") as json_file:
            data = json.load(json_file)
            return data
    
    @staticmethod
    def sendMsg(self, msg: str):
        payload = {'chat_id': self.chat_id, 'text': msg,
                'disable_notification': 'false'}
        response = requests.request(
            "POST", self.tel_url, json=payload)
        return (response.text.encode('utf8'))