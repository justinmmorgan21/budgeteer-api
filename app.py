from flask import Flask, jsonify, request
from sqlalchemy import select
from flask_cors import CORS
from models import SessionLocal, Transaction, Category, Tag
from werkzeug.exceptions import NotFound
from sqlalchemy.orm import joinedload

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
    transactions = session.query(Transaction).options(
      joinedload(Transaction.category).joinedload(Category.tags),
      joinedload(Transaction.tag)
    ).all()
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
    # transaction.category_id = int(category_id) if (category_id := request.form.get("category")) else transaction.category_id
    # transaction.tag_id = int(tag_id) if (tag_id := request.form.get("tag")) else transaction.tag_id
    category_id = request.form.get("category")
    tag_id = request.form.get("tag")

    transaction.category_id = int(category_id) if category_id else transaction.category_id
    transaction.tag_id = int(tag_id) if tag_id not in [None, ""] else None
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
    return jsonify([c.to_dict(True) for c in categories])
  except Exception as e:
    raise e
  finally:
    session.close()

@app.route('/categories', methods=['POST'])
def category_create():
  session = SessionLocal()
  try:
    name = request.form.get('name')
    category = Category(name=name)
    session.add(category)
    session.commit()
    tag = Tag(name='-', category_id=category.id)
    session.add(tag)
    session.commit()
    return jsonify(category.to_dict())
  except Exception as e:
    session.rollback()
    raise e
  finally:
    session.close()

@app.route('/categories/<int:id>', methods=['PATCH'])
def category_update(id):
  session = SessionLocal()
  try:
    category = session.scalar(select(Category).where(Category.id==id))
    if not category:
      raise NotFound(f"Category with id {id} not found.")
    name = request.form.get("catName")
    category.name = name or category.name
    session.commit()
    return jsonify(category.to_dict())
  except Exception as e:
    session.rollback()
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

if __name__ == "__main__":
  app.run(debug=True)

@app.route('/tags', methods=['POST'])
def tag_create():
  session = SessionLocal()
  try:
    name = request.form.get('name')
    category_id = request.form.get('category_id')
    tag = Tag(name=name, category_id=category_id)
    session.add(tag)
    session.commit()
    return jsonify(tag.to_dict())
  except Exception as e:
    session.rollback()
    raise e
  finally:
    session.close()

@app.route('/tags/<int:id>', methods=['PATCH'])
def tag_update(id):
  session = SessionLocal()
  try:
    tag = session.scalar(select(Tag).where(Tag.id==id))
    if not tag:
      raise NotFound(f"Category with id {id} not found.")
    name = request.form.get(str(tag.id))
    print('**********')
    print(name)
    print('**********')
    tag.name = name or tag.name
    session.commit()
    return jsonify(tag.to_dict())
  except Exception as e:
    session.rollback()
    raise e
  finally:
    session.close()