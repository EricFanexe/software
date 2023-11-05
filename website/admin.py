from flask import Blueprint, render_template, url_for
from .models import User, UserType, Record
from . import db
import sqlalchemy as sa
from flask_login import login_required, current_user
from .emojis import emojis, explanations
import random

adminBP = Blueprint('adminBP', __name__, static_folder='./static/', template_folder='./templates/', url_prefix='/admin')

@login_required
@adminBP.route('/users')
def admin_users():
    users = db.session.execute(sa.select(User)).all()
    return render_template('admin_users.html', user=current_user, users=users)

def randColor():
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    return "#{:02X}{:02X}{:02X}".format(red, green, blue)

@login_required
@adminBP.route('/emojis')
def admin_emojis():
    records = db.session.execute(sa.select(Record)).all()
    emoji_stat = db.session.execute(sa.select(Record.emoji, sa.func.count(Record.id)).group_by(Record.emoji)).all()
    labels, counts, barColors = [], [], []
    for emoji, count in emoji_stat:
        labels.append(emojis[emoji])
        counts.append(count)
        barColors.append(randColor())

    return render_template('admin_emojis.html',
                           user=current_user,
                           records=records,
                           emojis=emojis,
                           explanations=explanations,
                           labels=labels,
                           counts=counts,
                           barColors=barColors)
