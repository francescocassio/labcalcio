import pandas as pd
import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "seriea"
}

file_path = "serie_a_master.csv"
df = pd.read_csv(file_path)

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor(dictionary=True)

print("Inizio inserimento partite...")

matches_data = []

for _, row in df.iterrows():

    # Recupero ID squadra di casa
    cursor.execute(
        "SELECT team_id FROM teams WHERE team_name = %s",
        (row["HomeTeam"],)
    )
    home_result = cursor.fetchone()

    if not home_result:
        print(f"Squadra non trovata: {row['HomeTeam']}")
        continue

    home_id = home_result["team_id"]

    # Recupero ID squadra ospite
    cursor.execute(
        "SELECT team_id FROM teams WHERE team_name = %s",
        (row["AwayTeam"],)
    )
    away_result = cursor.fetchone()

    if not away_result:
        print(f"Squadra non trovata: {row['AwayTeam']}")
        continue

    away_id = away_result["team_id"]

    dati = (
        row["Date"],
        row["Season"],
        home_id,
        away_id,
        int(row["FTHG"]),
        int(row["FTAG"]),
        row["FTR"]
    )

    matches_data.append(dati)

insert_query = """
INSERT INTO matches
(match_date, season, home_team_id, away_team_id, home_goals, away_goals, final_result)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

cursor.executemany(insert_query, matches_data)
conn.commit()

print(f"Inserite {cursor.rowcount} partite!")

cursor.close()
conn.close()