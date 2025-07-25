from flask import Flask, jsonify, request
from sqlalchemy import select
from flask_cors import CORS
from models import SessionLocal, Transaction, Category, Tag
from sqlalchemy.orm import joinedload, selectinload
from datetime import date, datetime

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
        return jsonify(error="No file uploaded"), 400
    file_path = f"./uploads/{file.filename}"
    file.save(file_path)

    session = SessionLocal()
    try:
        upload_type = request.form.get('uploadType')
        transactions = None
        if upload_type == "statement":
            transactions = Transaction.read_statement(file_path, session)
        elif upload_type == "currentHistory":
            transactions = Transaction.read_current_transaction_history(file_path, session)
        for t in transactions:
            session.add(t)
        session.commit()
        return jsonify({"message": f"{len(transactions)} transactions added."})
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

@app.route('/transactions/<int:id>', methods=['POST'])
def child_transactions_create(id):
    session = SessionLocal()
    try:
        parent = session.get(Transaction, id)
        if not parent:
            return jsonify({"error": f"Transaction with id {id} not found."}), 404
        for child in parent.child_transactions:
            session.delete(child)
        session.commit()
        tx_type = parent.type
        date_obj = parent.date
        payee = parent.payee
        splits = request.get_json()
        for split in splits:
            amount = float(split['amount'])
            category_id = int(split['category']['id'])
            tag_id = int(split['tag']['id'])
            transaction = Transaction(
                type=tx_type, date=date_obj, amount=amount, payee=payee,
                category_id=category_id, tag_id=tag_id, parent_transaction_id=parent.id)
            session.add(transaction)
        session.commit()
        return jsonify({"message": f"{len(splits)} transactions added."})
    except Exception as e:
        session.rollback()
        print("Error:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route('/transactions')
def transaction_index():
    session = SessionLocal()
    try:
        result = Transaction.filterQuery(session, request)
        return jsonify(result)
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
        if 'category_id' in request.form:
            category_id = request.form.get('category_id')
            transaction.category_id = int(category_id) if category_id not in [None, ""] else None
            category = session.get(Category, category_id)
            num_tags = len(category.tags) if category else 0
            if category and category.name == '*ignore*' or num_tags == 1:
                tag = session.query(Tag).filter(Tag.name=="-").first()
                transaction.tag_id = tag.id
        if 'tag_id' in request.form:
            tag_id = request.form.get('tag_id')
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
        query = select(Category).options(
            selectinload(Category.tags),
            selectinload(Category.transactions)
        )
        start_date = request.args.get('startDate')
        end_date = request.args.get('endDate')
        categories = session.scalars(query).all()
        if start_date and end_date:
            return jsonify([c.to_dict(True, False, start_date, end_date) for c in categories])
        else:
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
        name = request.form.get('catName')
        archive = request.form.get('archive')
        budget = request.form.get('budget')
        category.name = name or category.name
        if archive:
            category.archived = archive == "true"
        if budget:
            category.budget_amount = float(budget)
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
        query = select(Tag).options(
            selectinload(Tag.transactions)
        )
        tags = session.scalars(query).all()
        # tags = session.scalars(select(Tag)).all()
        return jsonify([t.to_dict() for t in tags])
    except Exception as e:
        raise e
    finally:
        session.close()

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
        name = request.form.get(str(tag.id)+"_name")
        archive = request.form.get('archive')
        new_budget = request.form.get(str(tag.id)+"_budget")
        tag.name = name or tag.name
        if archive:
            tag.archived = archive == 'true'
        tag.budget_amount = float(new_budget) if new_budget else tag.budget_amount
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

@app.route('/archived')
def archived_index():
    session = SessionLocal()
    try:
        categories = session.scalars(select(Category).where(Category.archived==True)).all()
        tags = session.scalars(select(Tag).where(Tag.archived==True)).all()
        return jsonify({
            'categories': [c.to_dict(True) for c in categories],
            'tags': [t.to_dict(True) for t in tags]
        })
    except Exception as e:
        raise e
    finally:
        session.close()


if __name__ == "__main__":
    app.run(debug=True)