from models import Base, engine, SessionLocal, Transaction, Category, Tag
from sqlalchemy import select

Base.metadata.create_all(engine)
print("budget database intialized!")

def seed_category_data():
    session = SessionLocal()
    try:
        category_names = ["Misc", "Income", "Utilities", "Food", "Doctor", "Gas", "Actualize repayment", "*ignore*",
                          "Samaritans share", "Toll", "Charity", "Pet", "Investment", "Mortgage", "Entertainment", "Phone",
                          "Amazon Prime membership", "HOA", "Justin App resources", "Hair Supplies", "Travel", "Clothing", "Car", "Health"]
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
                     "federal taxes", "home", "FISD paycheck", "hair", "coserv electric", "atmos gas", "water/garbage", "internet",
                     "groceries", "eating out", "alcohol", "pt", "justin shoulder", "prescription", "dentist", "younglife",
                     "compassion int", "children int", "tithe", "donation", "gift", "kim - american funds", "transfer to savings",
                     "prime video", "trail life", "sports", "kim at&t", "justin verizon", "serpapi", "openAI", "wash"]
        category_ids = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 11, 11, 11, 11, 11, 11, 13, 13,
                        15, 15, 15, 16, 16, 19, 19, 23]
        for i in range(0, len(tag_names)):
            tag = Tag(name=tag_names[i], category_id=category_ids[i])
            session.add(tag)
        session.add(Tag(name="hulu", archived=True, category_id=15))
        session.commit()
        return print({"message": f"Tag seed data created successfully. {len(tag_names) + 1 + len(categories)} tags added."})
    finally:
        session.close()

def seed_transaction_data():
    session = SessionLocal()
    try:
        transactions = Transaction.read_statement("./seed-data/BECU-Statement-17-Jan-2025.pdf", session)
        cats = [8,8,None,2,23,2,2,8,2,2,1,2,2,2,2,None,2,8,1,6,4,11,10,10,11,6,4,4,1,1,1,1,1,4,11,4,6,4,4,11,11,4,8,4,15,1,1,1,4,\
                1,16,4,1,8,16,1,4,None,4,4,11,15,3,8,15,15,1,4,4,1,4,4,4,15,1,11,8,14,8,3,4,4,4,1,13,1,4,4,24,4,4,4,13,4,1,6,4,11,\
                    1,1,4,4,4,4,1,15,4,4,11,12,4,4,4,6,4,4,15,11,1,4,4,4,1,6,6,None,1,10,15,1,1,15,4,4,4,6,4,6,4,1,4,15,4,7,1,9,4,\
                        4,None,1,4,4,1,1,4,1,6,1]
        tags = [1,1,None,37,8,37,37,1,37,37,29,37,37,37,36,None,37,1,25,1,43,54,1,1,54,1,42,42,25,28,29,29,29,43,54,42,1,42,43,53,\
                53,42,1,43,57,25,29,25,42,25,60,43,25,1,60,35,42,None,43,43,54,15,38,1,65,15,28,42,43,25,42,43,43,15,25,52,1,1,1,\
                    41,43,42,42,29,55,25,43,42,1,42,43,43,56,43,25,1,42,51,29,32,43,42,42,42,25,57,43,42,50,1,42,42,42,1,42,44,57,\
                        49,29,43,43,43,25,1,1,None,25,1,59,25,25,57,42,42,43,1,42,1,43,1,43,57,43,1,29,1,43,42,None,28,42,42,25,25,\
                            43,25,1,35]
        for i in range(len(transactions)):
            tx = transactions[i]
            tx.category_id = cats[i]
            tx.tag_id = tags[i]
            session.add(tx)
        session.commit()
        return print({"message": f"Transaction seed data created successfully. {len(transactions)} transactions added."})
    finally:
        session.close()

seed_category_data()
seed_tag_data()
seed_transaction_data()