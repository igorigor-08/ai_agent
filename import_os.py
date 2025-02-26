import os
import getpass
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
# from langchain_anthropic import ChatAnthropic
from langchain.chat_models.gigachat import GigaChat
from langgraph.types import interrupt

giga_key = 'Mzc5NGQ0ODEtNjVmYi00NTM3LWI2MDQtYTIzNjY0YWI2MWU4OjJmNDA5MDIxLTcxMTgtNGQ1OC04N2E0LTM3YzlkMWU1MjI1OA=='
giga = GigaChat(credentials=giga_key,
                model="GigaChat", timeout=30, verify_ssl_certs=False)
giga.verbose = False
llm = giga # declare l8r

class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str

with open('promptique copy 2.txt') as f:
    extended_prompt = f.read()

graph_builder = StateGraph(State)

def ask_user_prompt(state: State):
    user_prompt = "Выведи количество клиентов в портфеле ипотек по годам" #interrupt("Задайте свой вопрос.")
    return {"user_prompt": user_prompt}

def ask_llm(state: State):
    user_prompt = state.get("user_input")
    llm_output = llm.invoke(extended_prompt.replace("{user_prompt}",user_prompt))
    return {"messages" : llm_output}

def readability_validation(state: State):
    pass

# The first argument is the unique node name
# The second argument is the function or object that will be called whenever the node is used.
graph_builder.add_node("ask_llm", ask_llm)
graph_builder.add_edge(START, "ask_llm")
graph_builder.add_edge("ask_llm", END)
graph = graph_builder.compile()

def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        stream_graph_updates(user_input)
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break