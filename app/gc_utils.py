from langchain.schema import HumanMessage
from langchain.chat_models.gigachat import GigaChat
import requests


def get_ans_from_gc(user_prompt):
    with open('../promptique copy 2.txt') as f:
        extended_prompt = f.read()

    giga_key = 'Mzc5NGQ0ODEtNjVmYi00NTM3LWI2MDQtYTIzNjY0YWI2MWU4OjJmNDA5MDIxLTcxMTgtNGQ1OC04N2E0LTM3YzlkMWU1MjI1OA=='

    giga = GigaChat(credentials=giga_key,
                    model="GigaChat", timeout=30, verify_ssl_certs=False)
    giga.verbose = False

    # user_prompt = "Выведи количество клиентов в портфеле ипотек по годам"

    # Classic Prompt
    classic_prompt = extended_prompt.replace('{user_prompt}', user_prompt)

    response = giga.invoke([HumanMessage(content=classic_prompt)])
    return response.content
    # print(f"Model answer:\n{response.content}\n")