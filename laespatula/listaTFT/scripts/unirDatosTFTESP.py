import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col, expr, monotonically_increasing_id


def joinAndRenameNameColumn(totalPoints, newPointsTable):
    joined = totalPoints.join(newPointsTable, totalPoints.NAME == newPointsTable.SUMMONER, "full_outer")

    return joined.withColumn("SUMMONER",
                             when(col("SUMMONER").isNull(), col("NAME")).otherwise(col("SUMMONER")))


def fillIntAndStrZeros(joinedNoOrderDF):
    joinedWithZerosStr = joinedNoOrderDF.fillna("0")
    return joinedWithZerosStr.fillna(0)


def addAndOrderTotal(joinedFilledWithZerosDF):
    expresionSum = "TOTAL +" + updatedColumn

    newTotal = joinedFilledWithZerosDF.withColumn("TOTAL", expr(expresionSum).cast("Integer")).drop("NAME")

    return newTotal.orderBy(col("Total").desc()).withColumn("POSITION", monotonically_increasing_id() + 1)


if __name__ == '__main__':
    spark = SparkSession.builder \
        .master("local[1]") \
        .appName("Unir Datos ESP") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    numeroSnapshot = "3"
    updatedColumn = "MC" + numeroSnapshot

    total = spark.read.json("ESP/Total.json").withColumnRenamed("SUMMONER", "NAME")
    newTable = spark.read.json("ESP/" + updatedColumn + ".json").withColumnRenamed("PUNTOS", updatedColumn) \
        .select('SUMMONER', updatedColumn)

    joinedNameCleaned = joinAndRenameNameColumn(total, newTable)
    joinedWithZeros = fillIntAndStrZeros(joinedNameCleaned)
    newTotalOrdered = addAndOrderTotal(joinedWithZeros)

    newTotalOrdered.toPandas().to_json("ESP/NewTotal.json", orient='records', force_ascii=False, lines=True)

    print("------------ Nueva tabla ----------------")
    newTotalOrdered.show()

    data = []

    with open("ESP/NewTotal.json", 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            data.append(json.loads(line))

    out = json.dumps(data, ensure_ascii=False)

    with open('ESP/NewTotalBueno.txt', 'w', encoding='utf-8') as wr:
        wr.write(out)