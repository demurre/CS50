import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Homepage when you're logged in
@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Create a table for index
    rows = db.execute("SELECT symbol, SUM(shares) FROM transactions WHERE user_id=:user_id GROUP BY symbol HAVING SUM(shares) > 0", user_id=session["user_id"])

    # Creates a place to save the informations
    holdings = []
    all_total = 0

    for row in rows:
        stock = lookup(row['symbol'])
        sum_value = (stock["price"] * row["SUM(shares)"])
        holdings.append({"symbol": stock["symbol"], "name": stock["name"], "shares": row["SUM(shares)"], "price": usd(stock["price"]), "total": usd(sum_value)})
        all_total += stock["price"] * row["SUM(shares)"]

    rows = db.execute("SELECT cash FROM users WHERE id=:user_id", user_id=session["user_id"])
    cash = rows[0]["cash"]
    all_total += cash

    return render_template("index.html", holdings=holdings, cash=usd(cash), all_total=usd(all_total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # Retrieve the stock symbol and shares from the form
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Validate shares input
        try:
            shares = float(shares)
            if shares <= 0 or not shares.is_integer():
                raise ValueError
        except ValueError:
            return apology("Invalid number of shares")

        shares = int(shares)

        # Check if the stock symbol is valid and get its current price
        stock = lookup(symbol)
        if stock is None:
            return apology("Invalid stock symbol")

        # Calculate the total cost of the shares
        total_cost = stock["price"] * shares

        # Retrieve the user's available cash from the database
        rows = db.execute(
            "SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"]
        )
        cash = rows[0]["cash"]

        # Check if the user has enough cash to make the purchase
        if total_cost > cash:
            return apology("Not enough cash to buy")

        # Update the user's cash in the database
        db.execute(
            "UPDATE users SET cash = cash - :total_cost WHERE id = :user_id",
            total_cost=total_cost,
            user_id=session["user_id"],
        )

        # Insert the transaction into the database
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
            user_id=session["user_id"],
            symbol=symbol,
            shares=shares,
            price=stock["price"],
        )

        # Display a success message
        flash("Bought!")

        # Redirect the user to the homepage
        return redirect(url_for("index"))

    else:
        return render_template("buy.html")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Retrieve the user's transaction history from the database
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id = :user_id",
        user_id=session["user_id"],
    )

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure name of stock was submitted
        if not request.form.get("symbol"):
            return apology("must provide stock symbol")

        # Use the lookup function
        symbol = request.form.get("symbol").upper()
        stock = lookup(symbol)

        # Check if stock is valid
        if stock == None:
            return apology("Stock symbol not valid", 400)

        # If its valid
        else:
            return render_template(
                "quoted.html",
                stockSpec={"name": stock["symbol"], "price": usd(stock["price"])},
            )

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Retrieve the username and password from the form
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Perform the necessary validations
        if not username:
            return apology("Missing username")
        elif not password:
            return apology("Missing password")
        elif password != confirmation:
            return apology("Passwords do not match")

        # Check if the username already exists in the database
        rows = db.execute(
            "SELECT id FROM users WHERE username = :username", username=username
        )
        if len(rows) > 0:
            return apology("Username already taken")

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert the new user into the database
        db.execute(
            "INSERT INTO users (username, hash) VALUES (:username, :hash)",
            username=username,
            hash=hashed_password,
        )

        # Display a success message
        flash("Registered!")

        # Redirect the user to the login page
        return redirect(url_for("login"))

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure stock was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol")

        # Ensure shares was submitted
        elif not request.form.get("shares"):
            return apology("must provide shares")

        # Ensure shares is greater than 0
        elif int(request.form.get("shares")) < 0:
            return apology("must provide a valid number of shares")

        # Ensure shock exists
        if not request.form.get("symbol"):
            return apology("must provide an existing symbol")

        # Lookup function
        symbol = request.form.get("symbol").upper()
        stock = lookup(symbol)

        rows = db.execute(
            "SELECT symbol, SUM(shares) FROM transactions WHERE user_id=:user_id GROUP BY symbol HAVING SUM(shares) > 0",
            user_id=session["user_id"],
        )

        # Value of transaction
        shares = int(request.form.get("shares"))
        for row in rows:
            if row["symbol"] == symbol:
                if shares > row["SUM(shares)"]:
                    return apology("you're doing something wrong")

        transaction = shares * stock["price"]

        # Check if user has enough cash for transaction
        user_cash = db.execute(
            "SELECT cash FROM users WHERE id=:id", id=session["user_id"]
        )
        cash = user_cash[0]["cash"]

        # Subtract user_cash by value of transaction
        updt_cash = cash + transaction

        # Update how much left in his account (cash) after the transaction
        db.execute(
            "UPDATE users SET cash=:updt_cash WHERE id=:id",
            updt_cash=updt_cash,
            id=session["user_id"],
        )
        # Update de transactions table
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
            user_id=session["user_id"],
            symbol=stock["symbol"],
            shares=-1 * shares,
            price=stock["price"],
        )
        flash("Sold!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        rows = db.execute(
            "SELECT symbol FROM transactions WHERE user_id=:user_id GROUP BY symbol HAVING SUM(shares) > 0",
            user_id=session["user_id"],
        )
        return render_template("sell.html", symbols=[row["symbol"] for row in rows])
