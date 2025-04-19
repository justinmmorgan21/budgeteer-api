from flask import Flask, jsonify, request
from sqlalchemy import select
from flask_cors import CORS
from models import SessionLocal, Transaction, Category, Tag, Category_Tag
from werkzeug.exceptions import NotFound

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
# CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})  # For Credentials

@app.errorhandler(Exception)
def handle_exception(e):
    status_code = getattr(e, 'code', 500)
    return jsonify(error=str(e)), status_code

@app.route('/transactions/upload', methods=['POST'])
def transactions_create():
  file = request.files['file']
  if not file:
      return jsonify(error="No file uploded"), 400
  file_path = f"./uploads/{file.filename}"
  file.save(file_path)

  session = SessionLocal()
  try:
    transactions = Transaction.read_statement(file_path)
    for t in transactions:
        session.add(t)
    session.commit()
    return jsonify({"message": f"{len(transactions)} transactions added."})
  except Exception as e:
        session.rollback()
        raise e
  finally:
    session.close()

@app.route('/transactions')
def transaction_index():
  session = SessionLocal()
  try:
    transactions = session.scalars(select(Transaction)).all()
    if not transactions:
            raise NotFound(f"Transactions not found.")
    return jsonify([t.to_dict() for t in transactions])
  except Exception as e:
        raise e
  finally:
    session.close()

@app.route('/transactions/<int:id>')
def transaction_show(id):
   session = SessionLocal()
   try:
    transaction = session.scalar(select(Transaction).where(Transaction.id==id))
    if not transaction:
            raise NotFound(f"Transaction with id {id} not found.")
    return jsonify(transaction.to_dict())
   except Exception as e:
        raise e
   finally:
    session.close()

@app.route('/transactions/<int:id>', methods=['PATCH'])
def transaction_update(id):
   session = SessionLocal()
   try:
    transaction = session.scalar(select(Transaction).where(Transaction.id==id))
    if not transaction:
            raise NotFound(f"Transaction with id {id} not found.")
    transaction.category_tag_id = request.form.get("category_tag")
    session.commit()
    return jsonify(transaction.to_dict())
   except Exception as e:
        session.rollback()
        raise e
   finally:
    session.close()

@app.route('/categories')
def category_index():
   session = SessionLocal()
   try:
    categories = session.scalars(select(Category)).all()
    return jsonify([c.to_dict() for c in categories])
   except Exception as e:
        raise e
   finally:
    session.close()

@app.route('/tags')
def tag_index():
   session = SessionLocal()
   try:
    tags = session.scalars(select(Tag)).all()
    return jsonify([t.to_dict() for t in tags])
   except Exception as e:
        raise e
   finally:
    session.close()

@app.route('/category_tags', methods=['POST'])
def category_tag_create():
  session = SessionLocal()
  try:
    category = request.form.get("category")
    tag = request.form.get("tag")
    if not category or not tag:
            return jsonify(error="Both category and tag are required"), 400
    
    ct = Category_Tag(category_id=category, tag_id=tag)
    session.add(ct)
    session.commit()
    return jsonify(ct.to_dict())
  except Exception as e:
        session.rollback()
        raise e
  finally:
    session.close()

@app.route('/category_tags')
def category_tag_index():
  session = SessionLocal()
  try:
    cts = session.scalars(select(Category_Tag)).all()
    return jsonify([ct.to_dict() for ct in cts])
  except Exception as e:
        raise e
  finally:
    session.close()

if __name__ == "__main__":
  app.run(debug=True)
