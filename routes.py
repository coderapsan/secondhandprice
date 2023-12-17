# routes.py

from flask import render_template, url_for, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db
from app.forms import RegistrationForm, LoginForm, PredictionForm
from app.models import User, Prediction
from sklearn.preprocessing import StandardScaler
from joblib import load

# Load the trained models
linear_model = load('path/to/linear_model.joblib')  # Update with correct path
lasso_model = load('path/to/lasso_model.joblib')    # Update with correct path

def generate_hashed_password(password):
    # Implement your password hashing logic here
    # Example: return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    pass

def check_password(hashed_password, password):
    # Implement your password checking logic here
    # Example: return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    pass

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_hashed_password(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You can now log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password(user.password, form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("predict_price"))
        else:
            flash("Login unsuccessful. Please check your email and password.", "danger")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/predict_price", methods=["GET", "POST"])
@login_required
def predict_price():
    form = PredictionForm()
    if form.validate_on_submit():
        car_company = form.company.data
        car_model = form.model.data
        year = form.year.data
        showroom = form.showroom.data
        engine_type = form.engine.data
        kms = form.kms.data

        # Preprocess the input data as needed (e.g., encoding categorical variables)
        # Make predictions using the loaded models
        linear_prediction = linear_model.predict([[year, kms]])[0]
        lasso_prediction = lasso_model.predict([[year, kms]])[0]

        # Store the prediction in the database
        prediction = Prediction(
            car_company=car_company,
            car_model=car_model,
            year=year,
            showroom=showroom,
            engine_type=engine_type,
            kms=kms,
            user=current_user
        )
        db.session.add(prediction)
        db.session.commit()

        flash(f"Linear Prediction: ${linear_prediction:.2f}, Lasso Prediction: ${lasso_prediction:.2f}", "info")
        return redirect(url_for("predict_price"))

    return render_template("predict_price.html", form=form)
