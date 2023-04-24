from ..unirDatosTFTESP import joinAndRenameNameColumn, fillIntAndStrZeros, addAndOrderTotal
import warnings

warnings.filterwarnings("ignore")


def testJoinAndRenameNameColumn(spark):
    spark.sparkContext.setLogLevel("ERROR")
    totalDF = spark.createDataFrame(data=[('1', 'SnoodyBoo', 100, 100)],
                                    schema=['POSITION', 'SUMMONER', 'SS1', 'TOTAL'])

    newDF = spark.createDataFrame(data=[('SnoodyBoo', 'SnoodyBoo', 50)],
                                  schema=['NICK', 'SUMMONER', 'PUNTOS'])

    output = joinAndRenameNameColumn(totalDF, newDF)
    expected = [('1', 'SnoodyBoo', 100, 100, 50)]
    assert output == expected


def testFillIntAndStrZeros(spark):
    spark.sparkContext.setLogLevel("ERROR")
    notFilledDF = spark.createDataFrame(data=[('1', 'SnoodyBoo', None, 0),
                                              ('2', 'Xuso', 90, 90), ],
                                        schema=['POSITION', 'SUMMONER', 'MC1', 'TOTAL'])

    output = fillIntAndStrZeros(notFilledDF)
    expected = [('1', 'SnoodyBoo', 0, 0), ('2', 'Xuso', 90, 90), ]
    assert output == expected


def testAddAndOrderTotal(spark):
    spark.sparkContext.setLogLevel("ERROR")
    newTotalDF = spark.createDataFrame(data=[('1', 'SnoodyBoo', 100, 99, 100)],
                                       schema=['POSITION', 'SUMMONER', 'SS1', 'SS2', 'TOTAL'])

    output = addAndOrderTotal(newTotalDF)
    expected = [('1', 'SnoodyBoo', 100, 99, 199)]
    assert output == expected
