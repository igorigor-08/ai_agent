from langchain.schema import HumanMessage
from langchain.chat_models.gigachat import GigaChat
import requests

def get_ans_from_gc(conversation, message_type = "query", query_dict = {}):

    extended_prompt_file = '../promptique copy 2.txt'
    query_evaluator_prompt_file = '../evaluator_prompt.txt'
    message_history_file = '../evaluator_user.txt'
    ask_for_clarification_if_needed_file = '../initial_request_plug.txt'

    if message_type == 'query':
        with open(extended_prompt_file) as f:
            extended_prompt = f.read()
        with open(ask_for_clarification_if_needed_file) as f:
            asking_for_clarification = f.read()
        classic_prompt = extended_prompt.replace('{user_prompt}', query_dict.get("user_prompt", ""))
        classic_prompt = classic_prompt.replace('{plug_if_initial_query}', asking_for_clarification)

    elif message_type == 'error':
        with open(query_evaluator_prompt_file) as f:
            extended_prompt = f.read()
        classic_prompt = extended_prompt.replace('{sql_query}', query_dict.get("sql_query", ""))
        classic_prompt = classic_prompt.replace('{error}', query_dict.get("error", ""))
        classic_prompt = classic_prompt.replace('{database_structure}', query_dict.get("database_structure", ""))
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
        
    response = conversation.run(classic_prompt)
    print(response)
    return response
    # print(f"Model answer:\n{response.content}\n")