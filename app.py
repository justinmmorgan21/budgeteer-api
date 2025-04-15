from flask import Flask, jsonify
from sqlalchemy import select
from flask_cors import CORS
from models import SessionLocal, Transaction, Category, Tag

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
# CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})  # For Credentials


@app.route('/transactions/upload', methods=['POST'])
def create():
  file = request.files['file']
  file_path = f"./uploads/{file.filename}"
  file.save(file_path)

  session = SessionLocal()
  try:
    transactions = Transaction.read_statement(file_path)
    for t in transactions:
        session.add(t)
    session.commit()
    return jsonify({"message": f"{len(transactions)} transactions added."})
  finally:
    session.close()

@app.route('/transactions')
def transaction_index():
  session = SessionLocal()
  try:
    transactions = session.scalars(select(Transaction)).all()
    return jsonify([t.to_dict() for t in transactions])
  finally:
    session.close()

@app.route('/transactions/<int:id>')
def show(id):
   session = SessionLocal()
   try:
    transaction = session.scalar(select(Transaction).where(Transaction.id==id))
    return jsonify(transaction.to_dict())
   finally:
    session.close()

@app.route('/categories')
def category_index():
   session = SessionLocal()
   try:
    categories = session.scalars(select(Category)).all()
    return jsonify([c.to_dict() for c in categories])
   finally:
    session.close()

@app.route('/tags')
def tag_index():
   session = SessionLocal()
   try:
    tags = session.scalars(select(Tag)).all()
    return jsonify([t.to_dict() for t in tags])
   finally:
    session.close()

if __name__ == "__main__":
  app.run(debug=True)
