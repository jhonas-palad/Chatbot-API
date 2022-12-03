from .model import ChatBot

def cmd_main():
    chatbot = ChatBot.start_bot()
    while True:
        query = input(f'{chatbot.name}: ')

        if query == 'q':
            break;

        response = chatbot.get_response(query)
        print(response)
def init_bot(model_state, all_intents):
    return ChatBot.start_bot(model_state, all_intents)