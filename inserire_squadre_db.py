import csv

lista_squadre = []
with open("serie_a_master.csv", "r", encoding="utf-8") as f:
    lettore = csv.DictReader(f)

    for riga in lettore:
        sq_casa = riga['HomeTeam']
        sq_tr = riga['AwayTeam']
        lista_squadre.append(sq_casa)
        lista_squadre.append(sq_tr)

#ora trasformiamo la lista in set, e poi di nuovo in lista
lista_squadre = list(set(lista_squadre))

print(len(lista_squadre))