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
    transactions = Transaction.read_statement(file_path, session)

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
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    query = session.query(Transaction).options(
        joinedload(Transaction.category).joinedload(Category.tags),
        joinedload(Transaction.tag)
      ).order_by(Transaction.date.desc())
    
    total_count = query.count()
    transactions = query.offset((page - 1) * per_page).limit(per_page).all()
    
    return jsonify({
        'transactions': [t.to_dict() for t in transactions],
        'total_pages': (total_count + per_page - 1) // per_page,
        'current_page': page
    })
  except Exception as e:
      raise e
  finally:
    session.close()

@app.route('/transactions/<int:id>')
def transaction_show(id):
  session = SessionLocal()
  try:
    transaction = session.get(Transaction, id)
    if not transaction:
      return jsonify({"error": f"Transaction with id {id} not found."}), 404
    return jsonify(transaction.to_dict())
  except Exception as e:
    raise e
  finally:
    session.close()

@app.route('/transactions/<int:id>', methods=['PATCH'])
def transaction_update(id):
  session = SessionLocal()
  try:
    transaction = session.get(Transaction, id)
    if not transaction:
      return jsonify({"error": f"Transaction with id {id} not found."}), 404
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
    category = session.get(Category, id)
    if not category:
      return jsonify({"error": f"Category with id {id} not found."}), 404
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
    tag = session.get(Tag, id)
    if not tag:
      return jsonify({"error": f"Tag with id {id} not found."}), 404
    name = request.form.get(str(tag.id))
    tag.name = name or tag.name
    if request.form.get("archive"):
      tag.archived = True
    session.commit()
    return jsonify(tag.to_dict())
  except Exception as e:
    session.rollback()
    raise e
  finally:
    session.close()

@app.route('/tags/<int:id>', methods=['DELETE'])
def tag_delete(id):
  session = SessionLocal()
  try:
    tag = session.get(Tag, id)
    if not tag:
      return jsonify({"error": f"Tag with id {id} not found."}), 404
    tag_name = tag.name
    session.delete(tag)
    session.commit()
    return jsonify({"message": f"Tag '{tag_name}' deleted successfully."})
  except Exception as e:
    session.rollback()
    return jsonify({"error": str(e)}), 500
  finally:
    session.close()
