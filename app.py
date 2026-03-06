from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite:///ipl.db"

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Player(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    class Player(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(100), unique=True)
    team = db.Column(db.String(50))
    role = db.Column(db.String(50))
    country = db.Column(db.String(50))
    base_price = db.Column(db.Integer)
    current_bid = db.Column(db.Integer)
    team = db.Column(db.String(50))
    role = db.Column(db.String(50))
    country = db.Column(db.String(50))
    base_price = db.Column(db.Integer)
    current_bid = db.Column(db.Integer)


@app.route('/')
def index():
    players = Player.query.all()
    return render_template("index.html", players=players)


@app.route('/player/<int:id>', methods=["GET", "POST"])
def player(id):

    player = Player.query.get(id)

    if request.method == "POST":

        new_bid = int(request.form['bid'])

        # 🔒 Prevent lower bid
        if new_bid > player.current_bid:
            player.current_bid = new_bid
            db.session.commit()

        return redirect('/')

    return render_template("player.html", player=player)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5001)

