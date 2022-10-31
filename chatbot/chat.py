from .model import ChatBot

chatbot = ChatBot.start_bot()


def cmd_main():
    while True:
        query = input(f'{chatbot.name}: ')

        if query == 'q':
            break;

        response = chatbot.get_response(query)
        print(response)