from flask import Flask, jsonify
from models.base import SessionLocal
from models.transaction import Transaction

app = Flask(__name__)

@app.route('/transactions')
def get_transactions():
  session = SessionLocal()
  transactions = session.query(Transaction).all()
  return jsonify([t.to_dict() for t in transactions])

@app.route('/upload', methods=['POST'])
def upload_statement():
  file = request.files['file']
  file_path = f"./uploads/{file.filename}"
  file.save(file_path)

  session = SessionLocal()
  transactions = Transaction.read_statement(file_path)
  for t in transactions:
      session.add(t)
  session.commit()
  return jsonify({"message": f"{len(transactions)} transactions added."})

if __name__ == "__main__":
  app.run(debug=True)