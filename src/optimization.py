def write_optimized(df):
    (df.write
     .mode("overwrite")
     .partitionBy("Status")
     .parquet("../data/processed/shipments_parquet")
     )