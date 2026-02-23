import glob
import pandas as pd
import os

# --- CONFIGURAZIONE ---
percorso_cartella = 'seriea'
nome_output = 'serie_a_master_vpandas.csv'
# Selezioniamo solo le colonne che ci servono per evitare errori su colonne extra
colonne_target = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR']

# 1. RECUPERO FILE
files_csv = glob.glob(os.path.join(percorso_cartella, "*.csv"))
lista_df = []

print(f"Trovati {len(files_csv)} file. Inizio caricamento...")

# 2. CARICAMENTO ROBUSTO
for f in files_csv:
    try:
        # Leggiamo il file filtrando le colonne e saltando le righe corrotte
        temp_df = pd.read_csv(
            f,
            usecols=lambda x: x in colonne_target,
            on_bad_lines='skip',
            encoding='utf-8' # o 'latin1' se i file sono molto vecchi
        )
        lista_df.append(temp_df)
    except Exception as e:
        print(f"⚠️ Errore nel file {os.path.basename(f)}: {e}")

# Uniamo tutti i file in un unico DataFrame
df = pd.concat(lista_df, ignore_index=True)

# 3. PULIZIA DATI
# Rimuoviamo righe dove la data è assente
df = df.dropna(subset=['Date'])

# Convertiamo la colonna Date in oggetti datetime veri
# dayfirst=True è vitale per il formato 16/01/99 -> 16 Gennaio
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
df = df.dropna(subset=['Date']) # Rimuove date che non è stato possibile convertire

# 4. CALCOLO DELLA STAGIONE (Vettoriale)
# Se il mese è >= 8 (Agosto), la stagione inizia nell'anno della data
# Altrimenti (Gennaio-Luglio), inizia nell'anno precedente
anno = df['Date'].dt.year
mese = df['Date'].dt.month

start_year = anno.where(mese >= 8, anno - 1)
df['Season'] = start_year.astype(int).astype(str) + "-" + (start_year + 1).astype(int).astype(str)

# 5. ORDINAMENTO E FORMATTAZIONE FINALE
# Ordiniamo cronologicamente
df = df.sort_values(by='Date')

# Riordiniamo le colonne come richiesto
ordine_colonne = ["Season", "Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]
df = df[ordine_colonne]

# Opzionale: Pulizia spazi bianchi nei nomi delle squadre (es: "Inter " -> "Inter")
df['HomeTeam'] = df['HomeTeam'].str.strip()
df['AwayTeam'] = df['AwayTeam'].str.strip()

# Formattiamo la data per l'uscita CSV (senza orario)
df['Date'] = df['Date'].dt.strftime('%d/%m/%Y')

# 6. SALVATAGGIO
df.to_csv(nome_output, index=False, sep=';', encoding='utf-8')

print("-" * 30)
print(f"✅ ELABORAZIONE COMPLETATA!")
print(f"File salvato: {nome_output}")
print(f"Totale partite processate: {len(df)}")