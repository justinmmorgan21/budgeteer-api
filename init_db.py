from models import Base, engine, SessionLocal, Transaction, Category, Tag

Base.metadata.create_all(engine)
print("budget database intialized!")

session = SessionLocal()

def seed_transaction_data():
  transactions = Transaction.read_statement("./seed-data/BECU-Statement-21-Mar-2025.pdf")
  for t in transactions:
    session.add(t)
  session.commit()
  return print({"message": f"Transaction seed data created successfully. {len(transactions)} transactions added."})

def seed_category_data():
  category_names = ["Income", "Utilities", "Food", "Doctor"]
  for cn in category_names:
    category = Category(name=cn)
    session.add(category)
  session.commit()
  return print({"message": f"Category seed data created successfully. {len(category_names)} categories added."})

def seed_tag_data():
  tag_names = ["from checking to savings", "FISD paycheck", "groceries", "Coserv electric", "Atmos gas"]
  for tn in tag_names:
    tag = Tag(name=tn)
    session.add(tag)
  session.add(Tag(name="dog walking", archived=True))
  session.commit()
  return print({"message": f"Tag seed data created successfully. {len(tag_names) + 1} tags added."})

seed_transaction_data()
seed_category_data()
seed_tag_data()