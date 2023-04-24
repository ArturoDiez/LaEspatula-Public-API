import json

from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col, expr, monotonically_increasing_id

from ..models import datosCompetitivo

spark = SparkSession.builder \
    .master("local[1]") \
    .appName("Unir Datos ESP") \
    .getOrCreate()

numeroSnapshot = "5"

totalNow = datosCompetitivo.objects.filter(tipo="Total Snapshot", set=8, region="EU")
newSnapshot = datosCompetitivo.objects.filter(tipo="Snapshot " + numeroSnapshot, set=8, region="EU")
updatedColumn = "SS" + numeroSnapshot

total = spark.read.json(totalNow).withColumnRenamed("SUMMONER", "NAME")
newTable = spark.read.json(newSnapshot).withColumnRenamed("PUNTOS", updatedColumn) \
    .select('SUMMONER', updatedColumn)

joined = total.join(newTable, total.NAME == newTable.SUMMONER, "full_outer")

joinedNameCleaned = joined.withColumn("SUMMONER",
                                      when(col("SUMMONER").isNull(), col("NAME")).otherwise(col("SUMMONER")))

joinedWithZerosStr = joinedNameCleaned.fillna("0")
joinedWithZeros = joinedWithZerosStr.fillna(0)

expresionSum = "TOTAL +" + updatedColumn

newTotal = joinedWithZeros.withColumn("TOTAL", expr(expresionSum).cast("Integer")).drop("NAME")

newTotalOrdered = newTotal.orderBy(col("Total").desc()).withColumn("POSITION", monotonically_increasing_id() + 1)

newTotalOrdered.toPandas().to_json("EU/NewTotal.json", orient='records', force_ascii=False, lines=True)

data = []

with open("EU/NewTotal.json", 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        data.append(json.loads(line))

out = json.dumps(data, ensure_ascii=False)

with open('EU/NewTotalBueno.txt', 'w', encoding='utf-8') as wr:
    wr.write(out)
