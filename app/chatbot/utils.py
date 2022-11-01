import nltk
from nltk.stem.porter import PorterStemmer

import numpy as np

import json
from typing import (
    Any,
    NamedTuple,
)
from collections import namedtuple

stemmer = PorterStemmer()

#Use namedtupple instead, but i'll leave it here
# class ROData:
#     def __init__(self, **data):
#         super().__setattr__('data', data)
#     def __getattr__(self, __key) -> Any:
#         if __key not in self.data:
#             raise AttributeError(f"{__key} is does not exists in data information set.")
#         data = super().__getattribute__('data')
#         return data[__key]
#     def __setattr__(self, __name: str, __value: Any) -> None:
#         raise AttributeError("It is not possible to  modify the values of this instance.")



def tokenize(sentence):
    """
    Yield tokenized words in a sequence using word_tokenize
    """
    
    for token in nltk.word_tokenize(sentence):
        yield token

def stem(word):
    """
    Stem words using PorterStemmer
    """
    lower_w = word.lower()
    return stemmer.stem(lower_w)

def bag_of_words(tokenized_sequence, all_words):
    # bag = [0] * len(all_words)

    # bag = np.zeros(len(all_words), dtype=np.float32)

    bag = []
    for word in all_words:
        bag.append(1.0) if word in tokenized_sequence else bag.append(0.0)
        

    return np.array(bag, dtype=np.float32)

def load_json(filename):
    """
    Used for loading intents
    """
    if not filename.endswith('.json'):
        filename = filename + '.json'
    with open(filename, 'r') as f:
        return json.load(f)

def validate_kwargs(kwargs, keys):

    for key in kwargs:
        if not key in keys:
            raise KeyError(f"{key} is not a valid key argument")

def named_tuple_from_dict(cls_name, **kwargs) -> NamedTuple:
    
    kwargs_keys = kwargs.keys()
    kwargs_values = tuple(kwargs.values())
    namedtuple_cls = namedtuple(cls_name, kwargs_keys)

    return namedtuple_cls(*kwargs_values)


