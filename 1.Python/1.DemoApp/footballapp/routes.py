from footballapp import app
from footballapp import db
from footballapp import forms, models
from footballapp.models import User
from flask import render_template, url_for, redirect, flash, redirect
from flask import session
from flask import request


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/unexists')
def unexists():
    return render_template("untaken.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = forms.SignUpForm()

    if form.validate_on_submit():

        if form.data['username'] in [x.username for x in User.query.all()]:
            flash("Username is alredy taken")
            return redirect(url_for('unexists'))

        else:
            user = User(username=form.data['username'])
            user.set_password(form.data['password'])

            db.session.add(user)
            db.session.commit()

            session['user'] = user.username
            return redirect(url_for('login'))

    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm()

    if request.method == "GET" and "user" not in session:
        return render_template("login.html", form=form)

    if request.method == "GET":
        user = User.query.filter_by(username=session["user"]).first()
        form = forms.AddTeam()
        return render_template("logged.html", username=user, teams=user.teams, form=form)

    if form.validate_on_submit():

        if form.data["username"] in [x.username for x in User.query.all()]:
            user = User.query.filter_by(
                username=form.data["username"]).first()
            if user.check_password(form.data["password"]):
                session["user"] = user.username
                form = forms.AddTeam()

                return render_template("logged.html", username=user.username, teams=user.teams, form=form)
            else:
                flash("Sorry, password is not correct.")
        else:
            flash("Sorry, username does not exist.")


@app.route("/addteam", methods=["POST"])
def addteam():
    form = forms.AddTeam()
    username = models.User.query.filter_by(username=session["user"]).first()
    team = models.Team(name=form.data["team"])

    username.teams.append(team)
    db.session.add(username, team)
    db.session.commit()

    return render_template("teamadded.html", team=str(team))


@app.route('/logged')
def logged():
    username = User.query.filter_by(username=session["user"]).first()
    return render_template("logged.html", username=un, teams=teams)


@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))
