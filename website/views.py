# store pages of our website
# pages related to authentification will go to auth.py file.
# views.py and auth.py define a blueprint respectively.

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Record
from . import db
from .emojis import emojis, explanations
import json
import sqlalchemy as sa

viewsBP = Blueprint('viewsBP', __name__, static_folder='./static/',
                    template_folder='./templates/', url_prefix='/')


@viewsBP.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        emojiNo = int(request.form['emoji'])
        if not 0 <= emojiNo <= 5:
            flash('Invalid Emoji No.', category='error')
        else:
            record = Record(emoji=emojiNo, user_id=current_user.id)
            db.session.add(record)
            db.session.commit()
    return render_template("home.html", user=current_user, emojis=emojis, explanations=explanations)

@viewsBP.route('/delete-record', methods=['POST'])
def deleteRecord():
    data = json.loads(request.data)
    record_id = data['recordId']
    record = db.session.get(Record, record_id)
    if record:
        if record.user_id == current_user.id:
            db.session.delete(record)
            db.session.commit()
    return jsonify({})
