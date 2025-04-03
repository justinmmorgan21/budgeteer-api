from flask import Flask, render_template, url_for #, request
# from flask_cors import CORS
# import db
from models.transaction import Transaction

app = Flask(__name__, template_folder="../templates")
# CORS(app)

# @app.route("/tasks.json")
# def index():
#     return db.tasks_all()

# @app.route("/tasks.json", methods=["POST"])
# def create():
#     name = request.form.get("name")
#     estimated_time = request.form.get("estimated_time")
#     deadline = request.form.get("deadline")
#     return db.tasks_create(name, estimated_time, deadline)

# @app.route("/tasks/<id>.json")
# def show(id):
#     return db.tasks_find_by_id(id)

# @app.route("/tasks/<id>.json", methods=["PATCH"])
# def update(id):
#     name = request.form.get("name")
#     estimated_time = request.form.get("estimated_time")
#     deadline = request.form.get("deadline")
#     return db.tasks_update_by_id(id, name, estimated_time, deadline)

# @app.route("/tasks/<id>.json", methods=["DELETE"])
# def destroy(id):
#     return db.tasks_destroy_by_id(id)


@app.route('/')
def index():
    transactions = Transaction.read_statement()
    return render_template("index.html", transactions=transactions)

@app.route('/budget')
def transaction_reader():
    return "<p>transactions</p>"



# for transaction in transactions:
#     print(transaction)