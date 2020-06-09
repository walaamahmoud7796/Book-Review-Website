import os
import requests
from flask import Flask, session,render_template,request,Response,url_for,g,redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from functools import wraps
import json


user=None


app = Flask(__name__)
app.app_context().push()
g.user = None
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        global user
        if user is None:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/Signup",methods=["GET","POST"])
def Signup():
    message = None
    if request.method =="POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        gender = request.form.get("gender")
        email = request.form.get("email")
        password = request.form.get("password")
        if db.execute("SELECT email FROM users WHERE email=:email",{"email":email}).rowcount==0:
            db.execute("INSERT INTO users(fname,lname,email,password,gender) VALUES(:fname,:lname,:email,:password,:gender)",{"fname":fname,"lname":lname,"email":email,"password":password,"gender":gender})
            db.commit()
            return redirect('login')
        else:
            message="username already in use"
        db.commit()
    return render_template("Signup.html",message= message)

@app.route("/login",methods=["GET","POST"])
def login():
    message =None
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        print(email)
        print(password)
        if email == "" or password =="":#handle this case later in html
            message="you must fill both fields"
        else:
            if db.execute("SELECT * FROM users WHERE email=:email AND password =:password",{"email":email,"password":password}).rowcount==0:
                message="Wrong username or password"
            else:
                global user
                user =email
                return render_template("Welcome.html",loggedin=False)
            db.commit()

    return render_template("login.html",message=message)




@app.route("/search",methods=["GET","POST"])
@login_required
def search():
    message = None
    rows=[]
    if request.method =="POST":
        text = request.form.get("search")
        # print(text)
        like = '%'+text+'%'
        list = db.execute("SELECT title FROM books WHERE isbn LIKE :txt or title LIKE :txt or author LIKE :txt",{"txt":like})
        rows = list.fetchall()
        for row in rows:
            print(row[0])

        if list.rowcount==0:
            message = "This book doesn't exist"
        else:
            message = "Found "+str(list.rowcount)+" result"

    return render_template("Welcome.html",message = message,list =rows,loggedin=True)

@app.route("/search/<string:bookname>",methods=['GET','POST'])
@login_required
def searchbook(bookname):
    print('hello from book')
    bookinfo=None
    JSON = None
    ######### Get book info from books table##############
    bookinfo = db.execute("SELECT * FROM books WHERE title=:title",{"title":bookname}).fetchone()

    global user

    #
    if request.method =="POST":

        rate = request.form.get("rate")
        review = request.form.get("review")
        db.execute("INSERT INTO reviews(book_isbn,user_id,review,rate) VALUES(:isbn,:id,:review,:rate)",{"isbn":bookinfo["isbn"],"id":user,"review":review,"rate":rate})
        db.commit()
    ######## Get review counts and rate from GOOD READS############
    goodreads_info = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": os.getenv("GOOD_READS_KEY"), "isbns": bookinfo['isbn']})
    print( goodreads_info.status_code)
    if goodreads_info.status_code == 200:
        JSON =goodreads_info.json()

    ################### Get all reviews on this book######################
    reviews = db.execute("SELECT review from reviews WHERE book_isbn=:isbn",{"isbn":bookinfo["isbn"]}).fetchall()
    can_submit = True

    ############## check if the current user can submit a review on this book#############

    is_review_submittd = db.execute("SELECT review,rate FROM reviews WHERE book_isbn=:isbn AND user_id=:user_id",{"isbn":bookinfo["isbn"],"user_id":user}).fetchone()
    print(is_review_submittd)
    if is_review_submittd is not None :
        print("hello")
        can_submit = False




    return render_template('bookpage.html',booktitle=bookname,bookinfo=bookinfo,json=JSON,can_submit=can_submit,reviews=reviews)

@app.route("/api/<string:isbn>")
def api(isbn):
    JSON =None
    result = db.execute("SELECT * FROM books WHERE isbn=:isbn",{"isbn":isbn}).fetchone()
    # JSON = result.json()
    dict={}
    if result is None:
        return "invalid isbn"
    else:
        for k in result.keys():
            dict[k]=result[k]
        # print(result.keys())
        JSON = json.dumps(dict)
        myjson = json.loads(JSON)

        return myjson
