from flask import Flask, jsonify
from sqlalchemy import select
from flask_cors import CORS
from models import SessionLocal
from models import Transaction

app = Flask(__name__)
CORS(app)

@app.route('/transactions/upload', methods=['POST'])
def create():
  file = request.files['file']
  file_path = f"./uploads/{file.filename}"
  file.save(file_path)

  session = SessionLocal()
  transactions = Transaction.read_statement(file_path)
  for t in transactions:
      session.add(t)
  session.commit()
  return jsonify({"message": f"{len(transactions)} transactions added."})

@app.route('/transactions')
def index():
  session = SessionLocal()
  transactions = session.scalars(select(Transaction)).all()
  return jsonify([t.to_dict() for t in transactions])

@app.route('/transactions/<int:id>')
def show(id):
   session = SessionLocal()
   transaction = session.scalar(select(Transaction).where(Transaction.id==id))
   return jsonify(transaction.to_dict())

if __name__ == "__main__":
  app.run(debug=True)
