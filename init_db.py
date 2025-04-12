from models import Base, engine, SessionLocal
from models import Transaction

Base.metadata.create_all(engine)
print("budget database intialized!")

def seed_data():
  session = SessionLocal()
  transactions = Transaction.read_statement("./seed-data/BECU-Statement-21-Mar-2025.pdf")
  for t in transactions:
      session.add(t)
  session.commit()
  return print({"message": f"Seed data created successfully. {len(transactions)} transactions added."})

seed_data()
