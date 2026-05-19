from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import time

spark = SparkSession.builder.appName("DAGLab").getOrCreate()

# read the data
df = spark.read.csv("../data/raw/shipments.csv",
                    header=True,
                    inferSchema=True)

# df.printSchema()

# build the dag
result = (
    df.filter(col("ShippingCostUSD") > 50)
    .select("Carrier",
          "Status",
          "ShippingCostUSD",
          "OriginCity"
          )
    .groupBy("Carrier")
    .avg("ShippingCostUSD")
    )

# execute and show
result.show()

result.explain(True)

# keep it running, so as to check SparkUI (localhost:4040)
try:
    while True:
        print("Script is running...")
        
        time.sleep(5) 
except KeyboardInterrupt:
    print("\nScript cancelled by user.")