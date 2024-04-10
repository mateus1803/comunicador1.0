from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Configuração do banco de dados
DB_NAME = 'messages.db'

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT NOT NULL,
                      content TEXT NOT NULL)''')
    conn.commit()
    conn.close()

create_table()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        conn.close()
        
        flash('Mensagem enviada com sucesso', 'success')
        return redirect(url_for('admin'))

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages")
    messages = cursor.fetchall()
    conn.close()

    return render_template('admin.html', messages=messages)


@app.route('/messages')
def view_messages():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages")
    messages = cursor.fetchall()
    conn.close()

    return render_template('messages.html', messages=messages)


@app.route('/edit_message/<int:message_id>', methods=['GET', 'POST'])
def edit_message(message_id):
    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE messages SET title=?, content=? WHERE id=?", (new_title, new_content, message_id))
        conn.commit()
        conn.close()
        
        flash('Mensagem editada com sucesso', 'success')
        return redirect(url_for('admin'))

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages WHERE id=?", (message_id,))
    message = cursor.fetchone()
    conn.close()

    return render_template('edit_message.html', message=message)

@app.route('/delete_message/<int:message_id>')
def delete_message(message_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE id=?", (message_id,))
    conn.commit()
    conn.close()

    flash('Mensagem apagada com sucesso', 'success')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
