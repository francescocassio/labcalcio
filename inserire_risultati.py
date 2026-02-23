import pandas as pd
import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",          # cambia se necessario
    "password": "",  # metti la tua password
    "database": "seriea"
}


file_path = "serie_a_master.csv"

df = pd.read_csv(file_path)


conn = mysql.connector.connect(**db_config)
cursor = conn.cursor(dictionary=True)


cursor.execute("SELECT team_id, team_name FROM teams")
teams_data = cursor.fetchall()

team_dict = {row["team_name"]: row["team_id"] for row in teams_data}

print(team_dict)

print("Squadre caricate in memoria.")

matches_data = []

for _, row in df.iterrows():
    home_id = team_dict[row["HomeTeam"]]
    away_id = team_dict[row["AwayTeam"]]

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