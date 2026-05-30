from pyspark.sql import SparkSession
from pyspark.sql.types import *

spark = SparkSession.builder \
    .appName("StreamingLab") \
    .getOrCreate()

schema = StructType([
    StructField(
        "shipment_id",
        IntegerType()
    ),
    StructField(
        "status",
        StringType()
    )
])

stream_df = spark.readStream \
    .schema(schema) \
    .csv(
        "../data/stream_input"
    )

print(stream_df.isStreaming)

result = stream_df.groupBy(
    "status"
).count()

query = result.writeStream \
    .format("console") \
    .outputMode("complete") \
    .option(
        "checkpointLocation",
        "../data/streaming/checkpoints"
    ) \
    .start()

query.awaitTermination()