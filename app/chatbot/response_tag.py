from typing import List
from .utils import load_json

import random
import sys

class Response(dict):
    def __init__(self, intents_path:str)-> None:
        intents = self.load_intents(intents_path)

        for intent in intents:
            self[intent['tag']] = {'responses': intent['responses'], 'follow_up_responses': intent['follow_up_responses']}
    def load_intents(self, intents_path):

        return load_json(intents_path)
    def get_response_for_tag(self, tag_name) -> str:
        if tag_name not in self:
            raise KeyError("Tag name was not found")
        responses = self[tag_name]
        return {'response': random.choice(responses['responses']), 'follow_up_responses': responses['follow_up_responses']}

try:
    argvs = sys.argv[:]
    for index, value in enumerate(argvs):
        if value == '--train':
            filename_index = index + 1

    filename = argvs[filename_index] #may subscript error
    response = Response(filename)
except:
    #fallback
    response = Response('chatbot/intents.json')