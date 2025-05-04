from models import Base, engine, SessionLocal, Transaction, Category, Tag
from sqlalchemy import select

Base.metadata.create_all(engine)
print("budget database intialized!")

def seed_transaction_data():
  session = SessionLocal()
  try:
    transactions = Transaction.read_statement("./seed-data/BECU-Statement-17-Jan-2025.pdf")
    for t in transactions:
      session.add(t)
    session.commit()
    return print({"message": f"Transaction seed data created successfully. {len(transactions)} transactions added."})
  finally:
        session.close()

def seed_category_data():
  session = SessionLocal()
  try:
    category_names = ["Misc", "Income", "Utilities", "Food", "Doctor", "Gas"]
    for cn in category_names:
      category = Category(name=cn)
      session.add(category)
    session.commit()
    return print({"message": f"Category seed data created successfully. {len(category_names)} categories added."})
  finally:
        session.close()

def seed_tag_data():
  session = SessionLocal()
  try:
    tag_names = ["Misc", "from checking to savings", "FISD paycheck", "groceries", "Coserv electric", "Atmos gas"]
    category_ids = [1, 2, 2, 4, 3, 3]
    for i in range(0, 6):
      tag = Tag(name=tag_names[i], category_id=category_ids[i])
      session.add(tag)
    session.add(Tag(name="dog walking", archived=True, category_id=2))
    categories = session.scalars(select(Category)).all()
    for cat in categories:
       session.add(Tag(name='-', category_id=cat.id))
    session.commit()
    return print({"message": f"Tag seed data created successfully. {len(tag_names) + 1 + len(categories)} tags added."})
  finally:
        session.close()

seed_transaction_data()
seed_category_data()
seed_tag_data()