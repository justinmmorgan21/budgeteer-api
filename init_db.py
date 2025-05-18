from models import Base, engine, SessionLocal, Transaction, Category, Tag
from sqlalchemy import select

Base.metadata.create_all(engine)
print("budget database intialized!")

def seed_category_data():
    session = SessionLocal()
    try:
        budgets = [0,7000,500,2100,0,250,100,0,665,300,30,160,1813.57,65,70,16.23,157,82,100,100,40,300,80,60]
        category_names = ["Misc", "Income", "Utilities", "Food", "Doctor", "Gas", "Actualize repayment", "*ignore*", "Samaritans share", "Charity", 
                          "Pet", "Investment", "Mortgage", "Entertainment", "Phone", "Amazon Prime membership", "HOA", "Justin App resources", 
                          "Hair Supplies", "Travel", "Clothing", "Car", "Health&Beauty", "Home&Garden"]
        for i in range(len(category_names)):
            category = Category(name=category_names[i], budget_amount=budgets[i])
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
        tag_names = ["amazon", "target", "paypal", "venmo", "federal taxes", "fisd paycheck", "hair", "coserv electric", "atmos gas", 
                     "water/garbage", "internet", "groceries", "eating out", "alcohol", "pt", "justin shoulder", "prescription", "dentist", 
                     "younglife", "compassion int", "children int", "tithe", "donation", "gift", "kim - american funds", 
                     "transfer to savings", "prime video", "trail life", "sports", "kim at&t", "justin verizon", "serpapi", "openAI", "wash", 
                     "insurance", "parking", "toll", "camping", "walmart", "oil change", "supplements","home","gardening"]
        category_ids = [1, 1, 1, 1, 1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 10, 10, 10, 10, 10, 10, 12, 12,
                        14, 14, 14, 15, 15, 18, 18, 22, 22, 22, 22, 20, 1, 22, 23, 24, 24]
        budgets = [0,0,0,0,7,5000,2000,150,150,150,79,1000,1000,100,0,0,0,0,30,43,35,140,0,30,60,100,15,20,30,25,13,75,7,0,135,0,80,0,0,50,50,20,20]
        for i in range(0, len(tag_names)):
            tag = Tag(name=tag_names[i], category_id=category_ids[i], budget_amount=budgets[i])
            session.add(tag)
        session.add(Tag(name="hulu", archived=True, category_id=14, budget_amount=10.81))
        session.commit()
        return print({"message": f"Tag seed data created successfully. {len(tag_names) + 1 + len(categories)} tags added."})
    finally:
        session.close()

def seed_transaction_data():
    session = SessionLocal()
    try:
        transactions = Transaction.read_statement("./seed-data/BECU-Statement-17-Jan-2025.pdf", session)
        cats = [8,8,None,2,8,2,2,8,2,2,1,2,2,2,2,None,2,8,1,6,4,10,22,22,10,6,4,4,1,1,1,1,1,4,10,4,6,4,4,10,10,4,8,4,16,1,1,1,4,1,15,4,1,8,15,24,4,None,4,4,10,14,3,8,14,14,1,4,4,1,4,4,4,14,1,10,8,13,8,3,4,4,4,1,12,1,4,4,23,4,4,4,12,4,1,6,4,10,1,1,4,4,4,4,1,14,4,4,10,11,4,4,4,6,4,4,14,10,1,4,4,4,1,6,6,None,1,22,14,1,1,14,4,4,4,6,4,6,4,1,4,14,4,7,1,9,4,4,20,1,4,4,1,1,4,1,6,24]
        tags = [1,1,None,31,1,31,31,1,31,31,27,31,31,31,30,None,31,1,25,1,37,48,61,61,48,1,36,36,25,26,27,27,27,37,48,36,1,36,37,47,47,36,1,37,1,25,27,25,36,25,54,37,25,1,54,1,36,None,37,37,48,12,32,1,65,12,26,36,37,25,36,37,37,12,25,46,1,1,1,35,37,36,36,27,49,25,37,36,1,36,37,37,50,37,25,1,36,45,27,28,37,36,36,36,25,51,37,36,44,1,36,36,36,1,36,38,51,43,27,37,37,37,25,1,1,None,25,61,53,25,25,51,36,36,37,1,36,1,37,1,37,51,37,1,27,1,37,36,1,26,36,36,25,25,37,25,1,1]

        for i in range(len(transactions)):
            tx = transactions[i]
            tx.category_id = cats[i]
            tx.tag_id = tags[i]
            session.add(tx)
        transactions = Transaction.read_statement("./seed-data/BECU-Statement-21-Feb-2025.pdf", session)
        cats = [8,8,2,2,None,2,2,2,2,None,8,8,2,2,2,2,2,2,2,2,2,8,3,3,15,1,4,4,4,1,4,1,1,3,22,4,1,4,1,1,1,22,23,4,6,21,10,21,None,22,11,4,14,4,21,4,1,1,4,16,1,None,1,4,14,4,10,8,None,6,23,23,21,6,4,4,14,None,22,4,4,4,4,20,20,4,18,20,20,4,3,4,4,3,10,13,4,6,1,12,20,14,4,20,4,4,1,9,12,4,6,10,4,4,1,4,4,14,None,4,1,10,1,None,1,1,10,4,1,4,5,None,4,4,1,4,4,1,1,19,24,4,7,4,14,4,1,4,4,None,1,1,4,4,4,3,15,3,3,6,22,18,14,22,22,1,5]
        tags = [1,1,31,31,None,31,31,31,31,None,1,1,31,31,31,31,30,31,31,31,31,1,34,34,55,25,37,37,37,25,36,25,27,33,59,36,26,37,27,27,27,20,1,38,1,1,48,1,None,58,1,36,51,37,1,36,25,25,37,14,26,None,25,37,51,36,48,1,None,1,1,1,1,1,36,36,12,None,61,36,37,36,37,1,1,36,57,1,1,36,35,37,36,32,46,1,37,1,25,49,1,12,37,1,36,37,27,1,50,37,1,45,37,36,25,37,36,52,None,36,27,44,29,None,25,26,43,36,25,37,40,None,36,36,1,36,37,25,25,1,1,36,1,37,51,37,25,36,36,None,26,25,36,36,36,33,55,34,34,1,59,56,53,61,60,25,39]

        for i in range(len(transactions)):
            tx = transactions[i]
            tx.category_id = cats[i]
            tx.tag_id = tags[i]
            session.add(tx)
        transactions = Transaction.read_statement("./seed-data/BECU-Statement-21-Mar-2025.pdf", session)
        cats = [8,8,2,None,2,2,2,2,2,2,2,2,2,2,2,8,4,5,6,4,4,1,20,4,1,None,1,10,4,4,1,1,4,5,None,1,22,14,14,14,4,16,None,4,4,1,4,1,1,1,4,4,8,4,None,None,4,6,4,1,3,10,13,4,4,4,4,1,1,4,12,4,1,None,None,1,12,3,4,4,10,19,1,4,1,5,4,21,24,4,4,4,10,4,4,None,4,10,4,1,1,None,18,4,None,14,14,1,4,1,14,5,4,1,7,4,4,4,4,4,4,14,4,6,4,4,None,6,4,4,4,4,3,8,3,4,15,3,4,22,4,4,4,18,6,4,1,4,4,4]
        tags = [1,1,31,None,31,31,31,31,31,31,30,31,31,31,31,1,36,None,1,36,36,25,62,36,27,None,26,46,36,37,27,27,36,39,None,26,64,51,51,51,37,14,None,36,36,25,36,27,25,25,37,36,1,36,None,None,37,1,36,27,35,46,1,37,37,36,36,25,25,36,49,36,25,None,None,27,50,35,36,37,45,1,25,36,25,39,36,1,1,36,36,37,44,36,38,None,37,43,37,25,26,None,57,36,None,51,51,25,37,25,51,42,36,63,1,36,36,37,36,36,36,51,37,1,36,36,None,1,37,38,36,36,33,1,34,36,55,34,37,59,36,36,36,56,1,36,27,36,36,36]

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