from langchain.schema import HumanMessage
from langchain.chat_models.gigachat import GigaChat
import requests


def get_ans_from_gc(conversation, message_type = "query", query_dict = {}):

    if message_type == 'query':
        with open('../promptique copy 2.txt') as f:
            extended_prompt = f.read()
        classic_prompt = extended_prompt.replace('{user_prompt}', query_dict.get("user_prompt", ""))
    elif message_type == 'error':
        with open('../evaluator_prompt.txt') as f:
            extended_prompt = f.read()
        classic_prompt = extended_prompt.replace('{sql_query}', query_dict.get("sql_query", ""))
        classic_prompt = classic_prompt.replace('{error}', query_dict.get("error", ""))
        classic_prompt = classic_prompt.replace('{database_structure}', query_dict.get("database_structure", ""))
        classic_prompt = classic_prompt.replace('{user_prompt}', query_dict.get("user_prompt", ""))
        
    response = conversation.run(classic_prompt)
    print(response)
    return response
    # print(f"Model answer:\n{response.content}\n")