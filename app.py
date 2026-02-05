import os
from flaskext.mysql import MySQL
from flask import Flask, request, jsonify

app = Flask(__name__)

mysql = MySQL() 

app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST')
app.config['MYSQL_DATABASE_PORT'] = int(os.getenv('DB_PORT'))
app.config["MYSQL_DATABASE_USER"] = os.getenv('MYSQL_USER')
app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv('MYSQL_PASSWORD')
app.config["MYSQL_DATABASE_DB"] = os.getenv('MYSQL_DATABASE')

mysql.init_app(app)

def create_table():
    conn = mysql.connect() #
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS to_do (
        task_id INT AUTO_INCREMENT PRIMARY KEY, 
        task VARCHAR(120) NOT NULL,
        task_status VARCHAR(20) DEFAULT 'PENDING'
                   )
    """)    
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/')
def hello():
    return 'Hello from Task Manager!'

@app.route('/add', methods = ['POST'])
def add():
    conn = mysql.connect()
    cursor = conn.cursor()

    data = request.get_json()
    task = data.get('task')

    cursor.execute("""
    INSERT INTO to_do (task)
        VALUES (%s)
    """, (task,))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'OK': True}), 201


@app.route('/delete', methods  = ['POST'])
def delete():
    conn = mysql.connect()
    cursor = conn.cursor()

    data = request.get_json()
    task_id = data.get('task_id')

    cursor.execute("""
    DELETE FROM to_do WHERE task_id = %s    
        """, (task_id,))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'OK': True}), 200

@app.route('/update_status', methods = ['POST'])
def update_status():
    conn = mysql.connect()
    cursor = conn.cursor()

    data = request.get_json()
    task_id = data.get('task_id')
    task_status = data.get('task_status')

    cursor.execute("""
    UPDATE to_do SET task_status = %s WHERE task_id = %s    
    """, (task_status, task_id))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'OK': True}), 200
    

@app.route('/view', methods = ['GET'])
def view():

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM to_do
    """)

    rows = cursor.fetchall()
    records = [{"task_id": r[0], "task": r[1], "task_status": r[2]} for r in rows]

    cursor.close()
    conn.close()

    return jsonify(records)


if __name__ == '__main__':
    create_table()
    app.run(host = '0.0.0.0', port = 8000)
    