from datetime import datetime, timedelta
from flask import Blueprint
from flask import flash, jsonify, redirect, request, render_template, url_for

from remember import db
from remember.memento import Memento
from remember.thresholds import THRESHOLDS

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/text', methods=['POST'])
def text():
    t = request.form.get('memento_text')

    if t and t.strip():
        m = Memento(t)
        db.session.add(m)
        db.session.commit()
        flash("Created memento %s!" % m.id)
    else:
        flash("Didn't create memento -- was it empty?")

    return redirect(url_for('.index'))

@main.route('/__debug__')
def debug():
    for qi in Memento.queue():
        items.append({'id': qi.memento.id, 'type': qi.threshold.name})

    return jsonify({'items': items})
