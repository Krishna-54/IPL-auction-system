import pandas as pd
from app import app, db, Player

df = pd.read_csv("players.csv")

with app.app_context():

    for _, row in df.iterrows():

        player = Player(
            player_name=row["player_name"],
            team=row["team"],
            role=row["role"],
            country=row["country"],
            base_price=row["base_price"],
            current_bid=row["base_price"]
        )

        db.session.add(player)

    db.session.commit()

print("Players inserted successfully")