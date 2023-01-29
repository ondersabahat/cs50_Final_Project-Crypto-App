"""
This app is my the final project for the harvard's cs50 course 

With this application, I wanted to create a website where users can create 
their own cryptocurrency portfolios and trade, 
and get a breakdown of their previous trading transactions. 

I got help from the videos of algovibes youtube channel while developing this application

"""
# importing libraries
from datetime import datetime
from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# importing our crypto module
from crypto import symbols, get_data, indicators



# flask app 
app = Flask(__name__)
app.secret_key = "AsmmpreCasxaU123hi"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# connect  to database
db = SQLAlchemy(app)

# create database models
# user model and creating user table in database using flask-sqlalchemy
class User(db.Model):
    id = db.Column("user_id", db.Integer, primary_key=True)
    email = db.Column("email", db.String(120), unique=True, nullable=False)
    username = db.Column("username", db.String(80), unique=True, nullable=False)
    hash = db.Column("hash", db.String(), unique=True, nullable=False)
    amount = db.Column("amount", db.Float)
    wallet = db.relationship('Wallet', backref='user')
    transactions = db.relationship('Transaction', backref='user')

    def __init__(self, email, username, hash, amount):
        self.email = email
        self.username = username
        self.hash = hash
        self.amount = amount
        
    def __repr__(self):
        return 'User %r' % self.username

# transaction model
class Transaction(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    coin = db.Column("coin", db.String(8), nullable=False)
    shares = db.Column("shares", db.Float, nullable=False)
    price = db.Column("price", db.Float, nullable=False)
    type = db.Column("type", db.String(6), nullable=False)
    date = db.Column("date", db.DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self,user_id, coin,shares,price, type, date=datetime.utcnow()):
        self.user_id = user_id
        self.coin = coin
        self.shares = shares
        self.price = price
        self.type = type
        self.date = date

    
    def __repr__(self):
        return f'Transaction {self.id}'

# wallet model
class Wallet(db.Model):
    id = db.Column("wallet_id", db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    coins = db.Column("coin", db.String(8), nullable=False)
    shares = db.Column("shares", db.Float, nullable=False)
    price = db.Column("price", db.Float, nullable=False)

    def __init__(self, user_id, coins, shares, price):
        self.user_id = user_id
        self.coins = coins
        self.shares = shares
        self.price = price 

    def __repr__(self):
        return f'Wallet {self.id}'

# application routes
# main page 
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # getting login form datas if post request
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if not email:
            flash("Plesae give an email!", "info")
            return redirect(url_for("login"))
        elif not request.form["password"]:
            flash("Plesae give a password!", "info")
            return redirect(url_for("login"))
        else:
            if not check_password_hash(User.query.filter_by(email=email).first().hash, password):
                flash("Incorrect email or password! Please try again! ")
                return redirect(url_for("login"))
            else:
                current = User.query.filter_by(email=email).first()
                if current:  
                    session["username"] = current.username
                    return redirect(url_for("quote"))
                else:
                    flash("This e mail is not found!", "info")
                    return redirect(url_for('register'))
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
     # getting register form datas if post request
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")

        if not email:
            flash("Plesae give an email!", "info")
            return redirect(url_for("register"))
        elif not username:
            flash("Please give an username!", "info")
            return redirect(url_for("register"))
        elif not password:
            flash("Plesae give a password!", "info")
            return redirect(url_for("register"))
        elif not password:
            flash("Plesae give the password again!", "info")
            return redirect(url_for("register"))
        elif password != password2:
            flash("Passwords don't match!", "info")
            return redirect(url_for("register"))
        
        # if previous steps are correct then generate a hash password for security
        hash = generate_password_hash(password)
        # try block to save information to database
        try:
            current = User(email, username, hash, 0)
            db.session.add(current)
            db.session.commit()
            session["username"] = current.username
            return redirect(url_for("quote"))
        except:
            flash("The username has already taken please try another one!", "info")
            return redirect(url_for("register"))
    else:
        return render_template("register.html")

@app.route('/logout')
def logout():
    # delete user from session object
    session.pop("username", None)
    return redirect('/')

# this function to create a decorator 
def login_required(f):
    """
    a decoreator for routes that require login
    
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if session["username"] is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated

@app.route("/chart", methods=["GET", "POST"])
@login_required
def chart():
    # get user's selections from the form and use that variables for using crypto module to visualize a chart
    if request.method == "POST":
        symbol = request.form.get("sym")
        interval = request.form.get("interval")
        lookback = request.form.get("lookback")
        df = indicators(get_data(symbol, interval=interval, lookback=lookback))
        time = df['Time'].to_list()
        high = df['High'].to_list()
        low = df['Low'].to_list()
        close = df['Close'].to_list()
        return render_template("chart.html", time = time, high=high, low=low, close=close, symbol=symbol, symbols=symbols)

    # default chart     
    symbol = "BTCUSDT"
    df = indicators(get_data(symbol))
    time = df['Time'].to_list()
    high = df['High'].to_list()
    low = df['Low'].to_list()
    close = df['Close'].to_list()
    return render_template("chart.html", time = time, high=high, low=low, close=close, symbol=symbol, symbols=symbols)


@app.route("/quote")
@login_required
def quote():
    # get user informations from database
    username = session["username"]
    amount = User.query.filter_by(username=username).first().amount
    user_id = User.query.filter_by(username=username).first().id

    coins = []
    total_amount = 0
    for i in  Wallet.query.filter_by(user_id=user_id).all():
        coin = i.coins
        shares = i.shares
        price = i.price
        coins.append((coin, shares, price))
        total_amount += price


    return render_template("quote.html", amount="%.2f"%amount, symbols=symbols, coins=coins, totalamount="%.2f"%total_amount)

@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    # get user transactions from database
    username = session["username"]
    user_id = User.query.filter_by(username=username).first().id
    transactions = []
    for i in Transaction.query.filter_by(user_id=user_id).all():
        symbol = i.coin
        shares = i.shares
        price = i.price
        type = i.type
        date = i.date
        transactions.append((symbol, shares, price, type, date))
    return render_template("history.html", transactions=transactions)

@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    if request.method == "POST":
        username = session["username"]
        user = User.query.filter_by(username=username).first()
        user.amount += float(request.form.get("deposit"))
        db.session.commit()

        return redirect(url_for("quote"))

    return render_template("deposit.html")

@app.route("/withdraw", methods=["GET", "POST"])
@login_required
def withdraw():
    username = session["username"]
    user = User.query.filter_by(username=username).first()
    if request.method == "POST":
        if user.amount - float(request.form.get("withdraw")) < 0:
            return f"Sorry you have only {user.amount} USD"
        else:
            user.amount -= float(request.form.get("withdraw"))
            db.session.commit()

        return redirect(url_for("quote"))

    return render_template("withdraw.html", amount=user.amount)


@app.route("/buy", methods=["GET","POST"])
@login_required
def buy():
    if request.method == "POST":
        username = session["username"]
        amount = User.query.filter_by(username=username).first().amount
        user_id = User.query.filter_by(username=username).first().id
        coin = request.form.get("symbolbuy")
        shares = request.form.get("sharesbuy")
        price = float(get_data(coin)['Close'][1])
        new_amount = float(shares)*price
        if new_amount > amount:
            flash("Sorry you don't have that much amount!", "info")
            return redirect(url_for("buy"))
        else:
            amount -= new_amount
            User.query.filter_by(username=username).first().amount = amount
            db.session.commit()

            user_id = User.query.filter_by(username=username).first().id
            if Wallet.query.filter_by(coins=coin).first():
                Wallet.query.filter_by(user_id=user_id).first().shares += float(shares)
                Wallet.query.filter_by(user_id=user_id).first().price += new_amount
                db.session.commit()
            else:
                # try block to save information to database
                try:
                    wallet = Wallet(user_id, coin, shares, new_amount)
                    db.session.add(wallet)
                    db.session.commit()
                except:
                    flash("Wallet couldn't save!", "info")
                    return redirect(url_for("buy"))
            # try block to save information to database
            try:
                transaction = Transaction(user_id, coin, shares, price, 'BUY')
                db.session.add(transaction)
                db.session.commit()
            except:
                flash("Transaction couldn't save!", "info")
                return redirect(url_for("buy"))
    return redirect(url_for("quote"))

@app.route("/sell", methods=['GET', 'POST'])
@login_required
def sell():
    if request.method == "POST":
        username = session["username"]
        user_id = User.query.filter_by(username=username).first().id
        amount = User.query.filter_by(username=username).first().amount
        coin = request.form.get("symbolsell")
        shares = request.form.get("sharessell")

        wallet = Wallet.query.filter_by(user_id=user_id).all()
        for i in wallet:
            if i.coins == coin:
                if float(shares) > i.shares:
                    flash("Sorry you don't have that much shares!", "info")
                    return redirect(url_for("sell"))
                else:
                    if float(shares) == i.shares:
                        price = float(shares) * float(get_data(coin)['Close'][1])
                        new_amount = amount + price
                        User.query.filter_by(username=username).first().amount = new_amount
                        Wallet.query.filter_by(user_id=user_id).first().price += price
                        db.session.commit()
                        db.session.delete(i)
                        db.session.commit()
                        # try block to save information to database
                        try:
                            transaction = Transaction(user_id, coin, shares, price, 'SELL')
                            db.session.add(transaction)
                            db.session.commit()
                        except:
                            flash("Transaction couldn't save!", "info")
                            return redirect(url_for("sell"))
                    else:
                        i.shares -= float(shares)
                        Wallet.query.filter_by(coins=coin).first().shares = i.shares
                        price = float(shares) * float(get_data(coin)['Close'][1])
                        new_amount = amount + price
                        User.query.filter_by(username=username).first().amount = new_amount
                        Wallet.query.filter_by(user_id=user_id).first().price -= price
                        db.session.commit()
                        # try block to save information to database
                        try:
                            transaction = Transaction(user_id, coin, shares, price, 'SELL')
                            db.session.add(transaction)
                            db.session.commit()
                        except:
                            flash("Transaction couldn't save!", "info")
                            return redirect(url_for("sell"))
    return redirect(url_for("quote"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)