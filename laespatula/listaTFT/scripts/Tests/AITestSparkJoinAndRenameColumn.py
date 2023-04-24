import pyspark.sql.functions as F
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from ..unirDatosTFTESP import joinAndRenameNameColumn, fillIntAndStrZeros, addAndOrderTotal


def test_joinAndRenameNameColumn(spark):
    # Define the input data
    totalPointsData = [("Alice", 10), ("Bob", 20), ("Charlie", 30)]
    totalPointsSchema = StructType([
        StructField("NAME", StringType(), True),
        StructField("TOTAL_POINTS", IntegerType(), True)
    ])
    totalPoints = spark.createDataFrame(totalPointsData, schema=totalPointsSchema)

    newPointsData = [("Alice", 5), ("David", 15), ("Eve", 25)]
    newPointsSchema = StructType([
        StructField("SUMMONER", StringType(), True),
        StructField("NEW_POINTS", IntegerType(), True)
    ])
    newPointsTable = spark.createDataFrame(newPointsData, schema=newPointsSchema)

    # Define the expected output data
    expectedData = [
        ("Alice", 10, 5),
        ("Bob", 20, None),
        ("Charlie", 30, None),
        ("David", None, 15),
        ("Eve", None, 25)
    ]
    expectedSchema = StructType([
        StructField("NAME", StringType(), True),
        StructField("TOTAL_POINTS", IntegerType(), True),
        StructField("NEW_POINTS", IntegerType(), True)
    ])
    expected = spark.createDataFrame(expectedData, schema=expectedSchema)

    # Call the function under test
    result = joinAndRenameNameColumn(totalPoints, newPointsTable)

    # Assert the output
    assert result.collect() == expected.collect()

    # Assert the function logic
    assert result.filter(F.col("NAME") == "Alice").select("TOTAL_POINTS", "NEW_POINTS").collect() == [(10, 5)]
    assert result.filter(F.col("NAME") == "Bob").select("TOTAL_POINTS", "NEW_POINTS").collect() == [(20, None)]
    assert result.filter(F.col("NAME") == "Charlie").select("TOTAL_POINTS", "NEW_POINTS").collect() == [(30, None)]
    assert result.filter(F.col("NAME") == "David").select("TOTAL_POINTS", "NEW_POINTS").collect() == [(None, 15)]
    assert result.filter(F.col("NAME") == "Eve").select("TOTAL_POINTS", "NEW_POINTS").collect() == [(None, 25)]
    assert result.filter(F.col("SUMMONER").isNull() & F.col("NAME").isNotNull()).count() == 0
    assert result.filter(F.col("SUMMONER").isNull() & F.col("NAME").isNull()).count() == 0
    assert result.filter(F.col("SUMMONER").isNotNull() & F.col("NAME").isNull()).count() == 0
    assert result.filter(F.col("SUMMONER") == F.col("NAME")).count() == 1
