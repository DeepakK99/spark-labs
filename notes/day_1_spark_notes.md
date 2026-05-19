# spark day 1 notes
1. Why is Spark better than pandas for huge datasets?
    - It distributes the computation and does paralle processing with fault tolerance.

2. What new problems appear in distributed systems?
    - How should data be split?
    - Coordination:
        - what work to do?
        - when they’re done?
        - what failed?
    - Fault Tolerance:
        - machine crashes?
        - executor dies?
        - network fails?
    - Data Movement:
        - network transfer > computation cost

3. What exactly does the Driver do?
    - plans work
    - distributes work
    - collects results

4. What exactly do Executors do?
    - run computations
    - process partitions
    - store intermediate results
    - execute tasks

5. Why do partitions matter?
    - Partitions determine:
        - parallelism
        - scalability
        - execution efficiency
    - Too few:
        - poor parallelism
    - Too many:
        - scheduling overhead