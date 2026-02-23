from datetime import datetime


def pulisci_data(stringa_data):
    # Controlliamo la lunghezza dell'anno (l'ultima parte della stringa)
    parti = stringa_data.split('/')
    anno = parti[-1]

    if len(anno) == 2:
        formato = "%d/%m/%y"
    else:
        formato = "%d/%m/%Y"

    return datetime.strptime(stringa_data, formato).date()

l = ["29/01/99", "3/01/99", "05/01/00"]

lista_date = []

for s in l:
    lista_date.append(pulisci_data(s))

print(lista_date[0].year)




