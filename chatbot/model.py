import torch
import torch.nn as nn

from .utils import stem, tokenize, bag_of_words
import random


class NeuralNet(nn.Module):

    def __init__(self,*,input_layer_size, hidden_layer_size, output_layer_size):
        
        super().__init__()
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


UNKNOWN_RESPONSES = [
    "Sorry, I didn't get that.",
    "I applogize, I can't understand the query",
    "I'm having hard time to understand your question"
]

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

    def prepare_intents(self, intents: list):
        intent_dict = {}

        for intent in intents:
            responses = intent['responses']
            entities = intent['entities']
            intent_dict[intent['tag']] = {
                'responses': responses,
                'entities': { 
                    entity['title']:
                    dict(text=entity['text'])  for entity in entities
                } or {}
            }
        self.intents = intent_dict
    @classmethod
    def start_bot(cls,model_state, all_intents):
        self = cls()
        
        intent_list = [intent.dict() for intent in all_intents]
        self.prepare_intents(intent_list)
        self.word_collection = model_state['word_collection']
        self.tags = model_state['tags']
        nn_instance = self.create_nn_ins( 
            **model_state['model_init_params']
        )

        nn_instance.load_state_dict(model_state['model_state'])
        nn_instance.eval()
        return self

    def clean_query(self, query: str) -> str:
        
        gen_query = tokenize(query)
        tok_query = [stem(word) for word in gen_query]
        result = bag_of_words(tok_query, self.word_collection)
        print(f'query: {query} gen_query={gen_query} tok_query={tok_query} res {result}')
        return result.reshape(1, result.shape[0])

    def get_response(self, query, threshold = .75):

        cleaned_query = self.clean_query(query)
        tensor_query = torch.from_numpy(cleaned_query)
        return self.generate_response(tensor_query, query, threshold)


    def generate_response(self, output, orig_query, threshold):
        tag_index, probability = self.nn_model.predict(output)
        tag = self.tags[tag_index]
        lower_orig_query = orig_query.lower()
        print(tag_index, probability, tag)
        found_entity = []
        entities = self.intents[tag]['entities']
        unknown_flag = False
        if probability < threshold:
            responses = UNKNOWN_RESPONSES
            unknown_flag = True
        else:
            
            entity_keys = list(entities.keys())
            
            for entity in entity_keys:
                found = True if lower_orig_query.find(entity.lower()) >= 0 else False
                if found :
                    found_entity.append(entity)
                print(entity)
            responses = self.intents[tag]['responses']

        if unknown_flag:
            response = {
                'text': [random.choice(responses)]
            }
        elif not found_entity:
            response = {
                'text': [random.choice(responses)],
                'options': entities or {}
            }
        else :
            text = []
            for entry in found_entity:
                text.append(entities[entry]['text'])
            response = {
                'text': text
            }


        return response

class ChatbotExc(Exception):
    pass




