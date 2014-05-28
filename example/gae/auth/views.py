# coding=utf-8
# Created 2014 by Janusz Skonieczny
import logging
from flask import Blueprint, current_app, render_template
from flask_login import login_required

app = Blueprint("auth", __name__, template_folder="templates")


@app.route("/")
@login_required
def profile():
    return render_template('User/profile.html')


