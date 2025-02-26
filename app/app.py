from flask import Flask, render_template, request, jsonify, send_from_directory, session
import os
import json
import ast
import uuid
import time
from database_utils import safe_query_to_dataframe
from plot_table import AutoVisualizer
from gc_utils import get_ans_from_gc
from langchain.schema import HumanMessage
from langchain.chat_models.gigachat import GigaChat
import requests
from flask_session import Session
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory

app = Flask(__name__)
app.secret_key = 'afd'

giga_key = 'Mzc5NGQ0ODEtNjVmYi00NTM3LWI2MDQtYTIzNjY0YWI2MWU4OjJmNDA5MDIxLTcxMTgtNGQ1OC04N2E0LTM3YzlkMWU1MjI1OA=='

giga = GigaChat(credentials=giga_key,
                model="GigaChat", 
                timeout=30, 
                verify_ssl_certs=False)
giga.verbose = False

memory = ConversationBufferWindowMemory(k=100)
conversation = ConversationChain(llm=giga, memory=memory)

UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    session['chat_history'] = session.get('chat_history', [])
    return render_template('index.html', chat_history=session['chat_history'])

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())

    user_message = request.form['message']
    with open('../db_structure.txt') as f:
        database_structure = f.read()
    # Логика формирования ответа
    answer_json = get_ans_from_gc(conversation, message_type = "query", query_dict = {"user_prompt":user_message})
    print(answer_json)
    answer_json = ast.literal_eval(answer_json)

    result = safe_query_to_dataframe(answer_json['SQL'])
    if len(result["errors"]) > 0:
        answer_json = get_ans_from_gc(conversation, message_type = "error", query_dict = {
            "sql_query":answer_json['SQL'],
            "error":" ".join(result["errors"]),
            "database_structure":database_structure,
            "user_prompt":user_message,
        })
        answer_json = ast.literal_eval(answer_json)
        result = safe_query_to_dataframe(answer_json['SQL'])

    df = result['data']
    
    # Инициализация ответа
    bot_response = {"text": None, "image": None}
    filename = None
    
    # Текстовый ответ
    if 'comment' in answer_json:
        bot_response['text'] = answer_json['comment']
    
    # Генерация изображения
    try:
        timestamp = int(time.time())
        filename = f"{session['user_id']}_{timestamp}.png"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        df_new, fig = AutoVisualizer(df, file_path).visualize()
        
        if fig:
            bot_response['image'] = filename
        else:
            if df.shape == (1, 1):
                print(df_new.values[0])
                bot_response['text'] += f"\nОтвет: {round(df_new.values[0][0], 3)}"
            else:
                bot_response['text'] += f"\nОтвет: {df_new}"

    except Exception as e:
        print(f"Ошибка генерации изображения: {str(e)}")
    
    # Сохранение в историю
    history_entry = {
        'user': user_message,
        'bot': {
            'text': bot_response['text'],
            'image': bot_response['image']
        }
    }
    
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    session['chat_history'].append(history_entry)
    session.modified = True
    
    return jsonify({
        'user_message': user_message,
        'bot_response': bot_response
    })

@app.route('/static/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, host='0.0.0.0', port=5021)