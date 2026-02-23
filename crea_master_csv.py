import glob
import pandas as pd
import csv
import os

# 1. Definisci il percorso della cartella
percorso_cartella = 'seriea'

# 2. Crea una lista di tutti i file .csv nella cartella
# Il simbolo * significa "qualsiasi nome"
files_csv = glob.glob(os.path.join(percorso_cartella, "*.csv"))

lista_nuova = []

# 3. Ciclo per aprire ogni file
for file in files_csv:
    with open(file, "r", encoding="utf-8") as f:
        lettore = csv.DictReader(f)

        for riga in lettore:
            if riga['Date'] != "":
                data = riga['Date']
                squadra_casa = riga['HomeTeam']
                squadra_trasferta = riga['AwayTeam']
                gol_casa = int(riga["FTHG"])
                gol_trasferta = int(riga["FTAG"])
                esito = riga["FTR"]

                #ottenere stagione
                #normalizzare le date
                #ordinare il csv in base alla data


                dati = (data, squadra_casa, squadra_trasferta, gol_casa, gol_trasferta, esito)
                lista_nuova.append(dati)

nome_file = "serie_a_master.csv"

# Apertura del file in modalità scrittura ('w')
with open(nome_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # 1. Scrivi l'intestazione (opzionale)
    writer.writerow(["Date", "HomeTeam", "AwayTeam","FTHG","FTAG","FTR"])

    # 2. Scrivi tutte le tuple in un colpo solo
    writer.writerows(lista_nuova)

print(f"File {nome_file} creato con successo!")

