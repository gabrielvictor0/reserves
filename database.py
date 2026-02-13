import json

def read_db():
    with open("db.json", 'r') as db:
        database = json.load(db)
    return database

def write_db(database):
    with open('db.json', 'w') as db:
        json.dump(database, db, indent=2)