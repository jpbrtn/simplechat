from flask import Flask, render_template
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = 'test'

socketio = SocketIO(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class History(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    message = db.Column('message', db.String(250))

@app.before_first_request
def create_tables():
    db.create_all()

@socketio.on('message')
def handlemsg(msg):
    print('Message:'+msg)

    message = History(message = msg)
    db.session.add(message)
    db.session.commit()

    send(msg, broadcast=True)

@app.route('/')
def index():
    messages = History.query.all()
    return render_template('index.html', messages= messages)


if __name__ == '__main__':
    socketio.run(app)