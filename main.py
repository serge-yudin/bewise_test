
from datetime import datetime
from traceback import print_exc

from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy

import requests


IP = 'localhost'  # in case of errors (like no db found, does your db accept tcp/ip connections) change to your IP in your localnet e.g. 192.168.1.2
DB_URI = f'postgresql+psycopg2://postgres:postgres@{IP}:5432/postgres'

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI  # 'sqlite:///viktorina.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

API_URL = 'https://jservice.io/api/random?count={}'

class Questions(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, unique=True, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)
    question = db.Column(db.String(512), nullable=False)
    answer = db.Column(db.String(128), nullable=True)

    def export(self) -> dict:
        return {'id': self.id, 'question_id': self.question_id, 'creation_date': self.creation_date,
                'question': self.question, 'answer': self.answer}

    def __repr__(self):
        return f'<Question id-{self.question_id}, question-{self.question}, answer-{self.answer}'


def get_last_question() -> dict:
    '''Gets last inserted question from DB.
    Returns a dict containing last question's data or {} empty dict if no data was found.'''
    q = Questions.query.order_by(Questions.id.desc()).first()
    if not q:
        return {}
    else:
        return q.export()


def insert_data(q: dict) -> bool:
    '''Inserts question's data into DB.
    If insertion was successful returns True otherwise False
    '''
    
    date = datetime.strptime(q['created_at'].split('T')[0], '%Y-%m-%d')
    question = Questions(question_id=q['id'], question=q['question'], answer=q['answer'], creation_date=date)
    try:
        db.session.add(question)
        db.session.commit()
        
        return True
    except Exception as e:
        print_exc()  # delete after debug
        return False


def fetch_data(n: int) -> list:
    '''Fetches data from api.
    n - number of questions to fetch.
    Returns a list of n-dicts if request was successful otherwise emply list'''
    res = requests.get(API_URL.format(int(n)))
    if res.status_code == 200:
        return res.json()
    return []


@app.route('/', methods=["POST"])
def home():
    query = request.json
    quest_num = int(query['questions_num'])
    
    last_question = get_last_question()
   
    #  logic to insert n-times in db from api
    count = 0
    while count < quest_num:
        data = fetch_data(quest_num)
        
        for d in data:
            if insert_data(d):
                count += 1
            if count == quest_num:
                break
           
    return make_response(jsonify(last_question), 200)


def create_db():
    db.create_all()


if __name__ == '__main__':
    
    app.run()
    