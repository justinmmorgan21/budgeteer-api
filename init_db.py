from models import Base, engine, SessionLocal, Transaction, Category, Tag
from sqlalchemy import select

Base.metadata.create_all(engine)
print("budget database intialized!")

def seed_transaction_data():
    session = SessionLocal()
    try:
        transactions = Transaction.read_statement("./seed-data/BECU-Statement-17-Jan-2025.pdf", session)
        for t in transactions:
            session.add(t)
        session.commit()
        return print({"message": f"Transaction seed data created successfully. {len(transactions)} transactions added."})
    finally:
        session.close()

def seed_category_data():
    session = SessionLocal()
    try:
        category_names = ["Misc", "Income", "Utilities", "Food", "Doctor", "Gas", "Actualize repayment", "*ignore*",
                          "Samaritans share", "Toll", "Charity", "Pet", "Investment", "Mortgage", "Entertainment", "Phone",
                          "Amazon Prime membership", "HOA", "Justin App resources", "Hair Supplies", "Travel", "Clothing", "Car"]
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
        categories = session.scalars(select(Category)).all()
        for cat in categories:
            session.add(Tag(name='-', category_id=cat.id))
        tag_names = ["amazon", "travel", "prime video", "target", "paypal", "sports", "gardening", "venmo", "supplements",
                     "federal taxes", "FISD paycheck", "hair", "coserv electric", "atmos gas", "water/garbage", "internet",
                     "groceries", "eating out", "alcohol", "pt", "justin shoulder", "prescription", "dentist", "younglife",
                     "compassion int", "children int", "tithe", "donation", "gift", "kim - american funds", "transfer to savings",
                     "prime video", "trail life", "kim at&t", "justin verizon", "serpapi", "openAI", "wash"]
        category_ids = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 11, 11, 11, 11, 11, 11, 13, 13,
                        15, 15, 16, 16, 19, 19, 23]
        for i in range(0, len(tag_names)):
            tag = Tag(name=tag_names[i], category_id=category_ids[i])
            session.add(tag)
        session.add(Tag(name="dog walking", archived=True, category_id=2))
        session.commit()
        return print({"message": f"Tag seed data created successfully. {len(tag_names) + 1 + len(categories)} tags added."})
    finally:
        session.close()

seed_transaction_data()
seed_category_data()
seed_tag_data()