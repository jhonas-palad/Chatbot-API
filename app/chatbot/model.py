import torch
import torch.nn as nn

import numpy as np

from utils import stem, tokenize, bag_of_words, named_tuple_from_dict
from response_tag import response

import os

import logging
logging.basicConfig(level=logging.DEBUG)

class NeuralNet(nn.Module):

    def __init__(self,*,input_layer_size, hidden_layer_size, output_layer_size):
        
        super().__init__()
        
        if not isinstance(input_layer_size, int):
            raise ValueError(f"{self.__class__.__name__}.__init__ argument input_layer_size " \
                             f"expected to be instance of type {int.__name__}, got instance of {input_layer_size.__class__.__name__}.")

        if not isinstance(hidden_layer_size, int):
            raise ValueError(f"{self.__class__.__name__}.__init__ argument hidden_layer_size " \
                             f"expected to be instance of type {int.__name__}, got instance of {hidden_layer_size.__class__.__name__}.")
        
        if not isinstance(output_layer_size, int):
            raise ValueError(f"{self.__class__.__name__}.__init__ argument output_layer_size " \
                             f"expected to be instance of type {int.__name__}, got instance of {output_layer_size.__class__.__name__}.")


        self.input_layer_size = input_layer_size
        self.hidden_layer_size = hidden_layer_size
        self.output_layer_size = output_layer_size

        self.Z1 = nn.Linear(input_layer_size, hidden_layer_size)
        self.Z2 = nn.Linear(hidden_layer_size, hidden_layer_size)
        self.Z3 = nn.Linear(hidden_layer_size, output_layer_size)
        

        self.activation = nn.ReLU()


    def forward(self, x):
        out = self.Z1(x)
        out = self.activation(out)
        out = self.Z2(out)
        out = self.activation(out)
        out = self.Z3(out)

        return out
    def predict(self, x):
        output = self.forward(x)
        #apply softmax activation function
        probabilities = torch.softmax(output, dim = 1)
        #get the maximum value' index in the ouput
        probability, index = torch.max(probabilities, dim = 1)

        return index.item(), probability.item()


class ChatBot:
    def __init__(self, name = 'Bot', nn_model_cls = NeuralNet):
        self.name = name

        if not issubclass(nn_model_cls, nn.Module):
            raise ChatbotExc(
                f"nn_model_cls argument expected {nn.Module.__name__} instance, "
                f"but got {type(nn_model_cls).__name__} instance"
            )

        self.nn_model_cls = nn_model_cls

    def create_nn_ins(self, **hyperparams):
        nn_instance = self.nn_model_cls(**hyperparams)
        self.nn_model = nn_instance
        return nn_instance

    def save_instance(self, filename):
        data = {
            'name': self.name,
            'state': self.nn_model.state_dict(),
            'Z1_units': self.nn_model.input_layer_size,
            'Z2_units': self.nn_model.hidden_layer_size,
            'Z3_units': self.nn_model.output_layer_size,
            'word_collection': self.dataset.word_collection,
            'tags': self.dataset.tags,
        }

        torch.save(data, filename)
    def load_instance(self, filename):
        trained_data: dict = torch.load(filename)
        if not isinstance(trained_data, dict):
            raise ChatbotExc("Trained dataset must be saved as form of mapping.")
        return named_tuple_from_dict('TrainedData', **trained_data)
         
    @classmethod
    def start_bot(cls, FILE = 'chatbot/model.pth'):
        self = cls()

        logging.debug(f"{os.getcwd()}, {cls.start_bot} param FILE = {FILE}")
        trained_ds = self.load_instance(FILE)

        
        setattr(self, 'name', trained_ds.name)
        #Cache these objects, to be used in get_response
        setattr(self, 'word_collection', trained_ds.word_collection)
        setattr(self, 'tags', trained_ds.tags)

        nn_instance = self.create_nn_ins( input_layer_size = trained_ds.Z1_units, \
                                        hidden_layer_size = trained_ds.Z2_units, \
                                        output_layer_size = trained_ds.Z3_units)

        nn_instance.load_state_dict(trained_ds.state)
        nn_instance.eval()
        return self

    def clean_query(self, query: str) -> str:
        gen_query = tokenize(query)
        tok_query = [stem(word) for word in gen_query]
        result = bag_of_words(tok_query, self.word_collection)
        return result.reshape(1, result.shape[0])

    def get_response(self, query, threshold = .75):
        cleaned_query = self.clean_query(query)
        tensor_query = torch.from_numpy(cleaned_query)
        return self.generate_response(tensor_query, threshold)


    def generate_response(self, output, threshold):
        tag_index, probability = self.nn_model.predict(output)
        tag = self.tags[tag_index]
        if probability < threshold:
            return "I'm sorry didn't understand that"
        return response.get_response_for_tag(tag)

class ChatbotExc(Exception):
    pass




