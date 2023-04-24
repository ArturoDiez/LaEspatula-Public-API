from ..models import datosCompetitivo


def run():
    numeroSnapshot = "2"

    totalNow = datosCompetitivo.objects.filter(tipo="Total Cups", set=8, region="ESP")
    newSnapshot = datosCompetitivo.objects.filter(tipo="MasterCup " + numeroSnapshot, set=8, region="ESP")
    updatedColumn = "MC" + numeroSnapshot

    for tot in totalNow:
        with open('listaTFT/scripts/ESP/Total.json', 'w', encoding='utf-8') as w:
            w.write(str(tot.datos))

    for new in newSnapshot:
        with open("listaTFT/scripts/ESP/" + updatedColumn + ".json", 'w', encoding='utf-8') as wr:
            wr.write(str(new.datos))
