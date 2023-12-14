from flask import Blueprint, render_template, request, redirect, url_for
from .models import Admin
from . import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        nim = request.form.get('nim')
        password = request.form.get('password')
        user = Admin.query.filter_by(nim = nim).first()
        if user is not None:
            if user.password == password:
                login_user(user, remember=True)
                return redirect(url_for('views.admin'))
            else:
                return render_template("login.html", user=current_user)
        else:
            return render_template("login.html", user=current_user)
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method =='POST':
        nim = request.form.get('nim')
        if Admin.query.filter_by(nim = nim).first() is not None:
            print("nim udah ada")
            return render_template("signup.html", user=current_user)
        password0 = request.form.get('password0')
        password1 = request.form.get('password1')
        if password0 != password1:
            print("pasword beda")
            return render_template("signup.html", user=current_user)
        admin = Admin(
            nim = nim,
            password = password0
        )
        db.session.add(admin)
        db.session.commit()
        print("signup!")
        return redirect(url_for('auth.login'))
    print("halo")
    return render_template("signup.html", user=current_user)