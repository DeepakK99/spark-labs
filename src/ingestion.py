def read_shipments(spark):

    df = spark.read.csv(
        "../data/raw/shipments.csv",
        header=True,
        inferSchema=True
    )

    print("\nSchema:")
    df.printSchema()

    print(
        "\nRow count:",
        df.count()
    )

    return df