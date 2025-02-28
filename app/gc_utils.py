from langchain.schema import HumanMessage
from langchain.chat_models.gigachat import GigaChat
import requests
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory

class MemorySetter():
    def __init__(self):
        self.memory_chain = {}

    def set_memory_for_user(self, id):
        giga_key = 'Mzc5NGQ0ODEtNjVmYi00NTM3LWI2MDQtYTIzNjY0YWI2MWU4OjJmNDA5MDIxLTcxMTgtNGQ1OC04N2E0LTM3YzlkMWU1MjI1OA=='

        giga = GigaChat(credentials=giga_key,
                        model="GigaChat", 
                        timeout=30, 
                        verify_ssl_certs=False)
        giga.verbose = False

        memory = ConversationBufferWindowMemory(k=100)
        conversation = ConversationChain(llm=giga, memory=memory)
        self.memory_chain[id] = conversation

    def get_memory_for_user(self, id):
        return self.memory_chain[id]

def get_ans_from_gc(conversation, message_type = "query", query_dict = {}):

    extended_prompt_file = '../promptique copy 2.txt'
    query_evaluator_prompt_file = '../evaluator_prompt.txt'
    message_history_file = '../evaluator_user.txt'
    ask_for_clarification_if_needed_file = '../initial_request_plug.txt'
    database_structure_file = '../db_structure.txt'

    with open(database_structure_file) as f:
        database_structure = f.read()


    if message_type == 'query':
        with open(extended_prompt_file) as f:
            extended_prompt = f.read()
        with open(ask_for_clarification_if_needed_file) as f:
            asking_for_clarification = f.read()
        
        classic_prompt = extended_prompt.replace('{user_prompt}', query_dict.get("user_prompt", ""))
        classic_prompt = classic_prompt.replace('{plug_if_initial_query}', asking_for_clarification.replace('{user_prompt}', query_dict.get("user_prompt","")))

        classic_prompt = classic_prompt.replace('{database_structure}', database_structure)
    elif message_type == 'error':
        with open(query_evaluator_prompt_file) as f:
            extended_prompt = f.read()
        classic_prompt = extended_prompt.replace('{sql_query}', query_dict.get("sql_query", ""))
        classic_prompt = classic_prompt.replace('{error}', query_dict.get("error", ""))
        classic_prompt = classic_prompt.replace('{database_structure}', database_structure)
        classic_prompt = classic_prompt.replace('{user_prompt}', query_dict.get("user_prompt", ""))

    elif message_type == 'clarification':
        with open(message_history_file) as f:
            message_history = f.read()
        with open(extended_prompt_file) as f:
            extended_prompt = f.read()
        message_history = message_history.replace('{user_prompt}', query_dict.get("user_prompt",""))
        message_history = message_history.replace('{clarifying_question}', query_dict.get("gc_first_response",""))
        message_history = message_history.replace('{clarification}', query_dict.get("user_clarification",""))
        classic_prompt = extended_prompt.replace('{user_prompt}',message_history)
        classic_prompt = classic_prompt.replace('{database_structure}',database_structure)
        classic_prompt = classic_prompt.replace('{plug_if_initial_query}',"")


    print(classic_prompt)
    response = conversation.run(classic_prompt)
    print(response)
    return response
    # print(f"Model answer:\n{response.content}\n")