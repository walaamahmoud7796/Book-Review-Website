import os
from sqlalchemy import create_engine


db = create_engine(os.getenv("DATABASE_URL"))

def create_users_table():
    query = "CREATE TABLE users(fname VARCHAR,lname VARCHAR,email VARCHAR PRIMARY KEY,password VARCHAR,gender VARCHAR)"
    db.execute(query)


def create_reviews_table():
    query = "CREATE TABLE reviews(user_id VARCHAR REFERENCES users(email),review VARCHAR,rate INTEGER,book_isbn VARCHAR REFERENCES books(isbn),PRIMARY KEY(user_id,book_isbn))"
    db.execute(query)

def main():
    print("Create database tables")
    #create_users_table()
    print("users table created")
    db.execute("DROP TABLE reviews")
    create_reviews_table()
    print("revies table created")


if __name__=="__main__":
    main()
