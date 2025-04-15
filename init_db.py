from models import Base, engine, SessionLocal, Transaction, Category, Tag

Base.metadata.create_all(engine)
print("budget database intialized!")

def seed_transaction_data():
  session = SessionLocal()
  try:
    transactions = Transaction.read_statement("./seed-data/BECU-Statement-21-Mar-2025.pdf")
    for t in transactions:
      session.add(t)
    session.commit()
    return print({"message": f"Transaction seed data created successfully. {len(transactions)} transactions added."})
  finally:
        session.close()

def seed_category_data():
  session = SessionLocal()
  try:
    category_names = ["Income", "Utilities", "Food", "Doctor"]
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
    tag_names = ["from checking to savings", "FISD paycheck", "groceries", "Coserv electric", "Atmos gas"]
    for tn in tag_names:
      tag = Tag(name=tn)
      session.add(tag)
    session.add(Tag(name="dog walking", archived=True))
    session.commit()
    return print({"message": f"Tag seed data created successfully. {len(tag_names) + 1} tags added."})
  finally:
        session.close()


seed_transaction_data()
seed_category_data()
seed_tag_data()