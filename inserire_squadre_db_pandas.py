import pandas as pd

import mysql.connector

df = pd.read_csv("serie_a_master.csv")

lista_squadre = pd.concat([df['HomeTeam'], df['AwayTeam']]).unique().tolist()

print(f"Numero di squadre uniche: {len(lista_squadre)}")
# print(lista_squadre)

#inserire queste squadre nel db

conn = mysql.connector.connect(user = "root",password = "",host = "localhost",database = "seriea")

cursor = conn.cursor()

q = "insert into teams (team_name) Values (%s)"

for squadra in lista_squadre:
    cursor.execute(q, (squadra, ))

conn.commit()

conn.close()