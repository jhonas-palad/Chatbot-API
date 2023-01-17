from . import utils

import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import Dataset as DS, DataLoader

from .model import ChatBot, NeuralNet

from typing import Callable
from enum import Enum


class IntentDataset(DS):
    def __init__(self, intents, filters = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n'):
        self.intents = intents
        self.word_collection = []
        self.tags = []

        self.preprocess(filters)

    def preprocess(self, filters):
        _intents = self.intents
        all_words = []
        tags = []
        xy = []
        def clean_patterns(patterns, tag):
            
            for pattern in patterns:
                tokenized_pattern = utils.tokenize(pattern)
                pattern_words = [utils.stem(w) for w in tokenized_pattern if w not in filters]
                all_words.extend(pattern_words)
                xy.append((pattern_words, tag))

        def split_xy(xy_list):
            x_data = []
            y_data = []
            for (p_tokens, tag) in xy_list:
                x_bag = utils.bag_of_words(p_tokens, self.word_collection_gen())
                
                y_tag = self.tags.index(tag)
                
                x_data.append(x_bag)
                y_data.append(y_tag)


            x_data = np.array(x_data)
            y_data = np.array(y_data)

            return x_data, y_data

        for intent in _intents:
            tag = intent['tag']
            tags.append(tag)
            clean_patterns(intent['patterns'], tag)

        self.word_collection = sorted(set(all_words))
        self.tags = sorted(set(tags))

        self._x_data, self._y_data = split_xy(xy)
    

    def word_collection_gen(self):
        for w in self.word_collection:
            yield  w


    def __getitem__(self, index):
        return self._x_data[index], self._y_data[index]

    def __len__(self):
        if not hasattr(self, 'n_samples'):
            self.n_samples = len(self._x_data)

        return self.n_samples


TrainState = Enum('TrainState', ['STARTING', 'EXECUTING', 'FINISHED'])

class Trainer:

    def __init__(self, chatbot, **kwargs):

        self.chatbot = chatbot

        self.dataset_cls = IntentDataset


        self._device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    @property
    def device(self):
        return self._device
    async def train_model(self, _intents, **kwargs):
        
        dataset = self.dataset_cls(_intents)

        setattr(self.chatbot, 'dataset', dataset)

        hidden_size:int = kwargs.pop('hidden_layer_size', 8)
        output_size = len(dataset.tags)
        input_size = len(dataset.word_collection)
        self.create_dsloader(batch_size = output_size, shuffle=True)

        

        # Create an instance 
        model = self.chatbot.create_nn_ins(input_layer_size= input_size,  \
                                         hidden_layer_size = hidden_size, \
                                         output_layer_size = output_size) \

        send: Callable = kwargs.pop('send', None)

        await send({
            "msg": f"Preparing parameters...",
            "status": TrainState.STARTING.value
        })
        loss = await self._run_epoch(model, send, **kwargs)
        
        return {
            'model_state': model.state_dict(),
            'model_init_params': {
                'input_layer_size': input_size,
                'hidden_layer_size': hidden_size,
                'output_layer_size': output_size
            },
            'word_collection': dataset.word_collection,
            'tags': dataset.tags,
            'loss': loss
        }


    async def _run_epoch(self, model: NeuralNet, send: Callable = None, num_epochs = 1000, learning_rate = 0.001):
        await send({
            "msg": f"Configuration -> number of epochs = {num_epochs}, learning rate = {learning_rate}",
            "status": TrainState.STARTING.value
        })
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr = learning_rate)
        dataloader = self.dataloader_ins
        for epoch in range(num_epochs):
            for x, y in dataloader:

                x = x.to(self.device)
                y = y.to(self.device)

                outputs = model(x) #make forward pass

                loss = criterion(outputs, y)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            if not ((epoch + 1) % 100):
                await send({
                    "msg": f"Epoch {epoch + 1} / {num_epochs}, loss = {loss.item():.4f}",
                    "status": TrainState.EXECUTING.value
                })
            percent_complete = (epoch / num_epochs) * 100
            await send({
                'percent_complete': round(percent_complete),
                'status': TrainState.EXECUTING.value
            })
            
        await send({
            "msg": f"Training finished with final loss of {loss.item():.4f}",
            "status": TrainState.FINISHED.value
        })
        return loss.item()
    def create_dsloader(self, **kwargs):
        if not hasattr(self.chatbot, 'dataset'):
            raise Exception(f"train_model() must be called first, before loading the dataset")

        dataloader = DataLoader(
                    dataset = self.chatbot.dataset,
                    **kwargs
                )

        self.dataloader_ins = dataloader

async def train_from_db(intents,send, **train_params):
    chatbot = ChatBot('MyBot')
    trainer = Trainer(chatbot)
    
    data = await trainer.train_model(intents,send = send, **train_params)
    return data


