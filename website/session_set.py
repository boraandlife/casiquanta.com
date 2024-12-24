from flask import Blueprint, render_template, request, flash, jsonify, Response, redirect, url_for, current_app, session
from flask_login import login_required, current_user
from .models import Note, User, Img
from . import db
import json


from flask_login import login_user, login_required, logout_user, current_user

import sys


def session_ruler():
	if "user" in session:
	    user = session["user"]
	    return f"<h1>{user}</h1>"
    


