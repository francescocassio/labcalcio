import pandas as pd


def analizza_csv(percorso_file):
    try:
        # Carichiamo il file (usando on_bad_lines per evitare crash)
        df = pd.read_csv(percorso_file, sep=None, engine='python', on_bad_lines='warn')

        print(f"--- Report Analisi: {percorso_file} ---")
        print(f"Dimensioni: {df.shape[0]} righe e {df.shape[1]} colonne\n")

        # 1. Controllo Valori Mancanti (NaN)
        miss_values = df.isnull().sum()
        if miss_values.sum() > 0:
            print("VALORI MANCANTI TROVATI:")
            print(miss_values[miss_values > 0])
        else:
            print("Nessun valore mancante.")

        # 2. Controllo Duplicati
        dups = df.duplicated().sum()
        if dups > 0:
            print(f"RIGHE DUPLICATE: {dups}")
        else:
            print("Nessuna riga duplicata.")

        # 3. Analisi Tipi di Dato (Potenziali errori di formato)
        print("\n--- Analisi Tipi di Dato ---")
        print(df.dtypes)

        # 4. Statistiche rapide per scovare Outliers (valori assurdi)
        print("\n--- Riepilogo Statistico (Numerico) ---")
        # Include solo colonne numeriche per evitare errori
        print(df.describe())

        # 5. Check colonne con un solo valore (inutili)
        solo_uno = [col for col in df.columns if df[col].nunique() <= 1]
        if solo_uno:
            print(f"\nCOLONNE COSTANTI (forse inutili): {solo_uno}")

        return df

    except Exception as e:
        print(f"❌ Errore durante l'apertura: {e}")
        return None


# Esecuzione
mio_df = analizza_csv('serie_a_master.csv')