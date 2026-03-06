from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
import pandas as pd

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite:///ipl.db"

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(100), unique=True)
    team = db.Column(db.String(50))
    role = db.Column(db.String(50))
    country = db.Column(db.String(50))
    base_price = db.Column(db.Integer)
    current_bid = db.Column(db.Integer)


def load_players_if_empty():
    if Player.query.first():
        return

    df = pd.read_csv("players.csv")

    for _, row in df.iterrows():
        player = Player(
            player_name=row["player_name"],
            team=row["team"] if pd.notna(row["team"]) else "",
            role=row["role"],
            country=row["country"],
            base_price=int(row["base_price"]),
            current_bid=int(row["base_price"])
        )
        db.session.add(player)

    db.session.commit()


@app.route("/")
def index():
    players = Player.query.all()
    return render_template("index.html", players=players)


@app.route("/player/<int:id>", methods=["GET", "POST"])
def player(id):
    player = Player.query.get_or_404(id)

    if request.method == "POST":
        new_bid = int(request.form["bid"])

        if new_bid > player.current_bid:
            player.current_bid = new_bid
            db.session.commit()

        return redirect("/")

    return render_template("player.html", player=player)


with app.app_context():
    db.create_all()
    load_players_if_empty()


if __name__ == "__main__":
    app.run(debug=True)

