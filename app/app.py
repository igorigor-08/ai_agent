from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
from database_utils import safe_query_to_dataframe
from plot_table import AutoVisualizer
from gc_utils import get_ans_from_gc
import ast
app = Flask(__name__)

# Папка для хранения изображений
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# История диалога
chat_history = []

@app.route('/')
def index():
    return render_template('index.html', chat_history=chat_history)

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['message']
    
    # Логика ответа
    answer_json = get_ans_from_gc(user_message)
    print(answer_json)
    result = safe_query_to_dataframe(ast.literal_eval(answer_json)['SQL'])
    df = result['data']
    print(df)
    df_new, fig = AutoVisualizer(df).visualize()

    bot_response = {
        'type': 'image',
        'content': 'res.png'  # Имя файла изображения
    }

    chat_history.append({'user': user_message, 'bot': bot_response})
    
    return jsonify({'user_message': user_message, 'bot_response': bot_response})

# Маршрут для отдачи изображений
@app.route('/static/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    # Создаем папку для изображений, если её нет
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)