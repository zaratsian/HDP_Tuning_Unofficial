<h3>Unofficial Guide for Tuning HDP Services</h3>

<br><img src="images/Apache_Hive_logo.png" class="inline"/>&ensp;&ensp;<b>Tuning Tips and Tricks</b>
<br>
<br><b>General Recommendations:</b>
<br>&bull; Enable Tez
<br>&bull; Store as ORC and use Zlib/Snappy compression
<br>&bull; Use Vectorization
<br>&bull; Use CBO (Cost-Based Optimizer) with Column Stats (CBO requires stats)
<br>&bull; Check SQL syntax
<br>
<br><b>Configuration Suggestions:</b>
<br>set hive.support.sql11.reserved.keywords=false; 
<br>set hive.execution.engine=tez;
<br>set hive.cbo.enable=true;
<br>set hive.compute.query.using.stats=true;
<br>set hive.stats.autogather=true;
<br>set hive.stats.fetch.column.stats=true;
<br>set hive.stats.fetch.partition.stats=true;
<br>set hive.vectorized.execution.enabled = true;
<br>set hive.vectorized.execution.reduce.enabled = true;
<br>set hive.vectorized.execution.reduce.groupby.enabled = true;
<br>set hive.exec.parallel=true;
<br>set hive.exec.parallel.thread.number=16;
<br>set hive.exec.dynamic.partition.mode=nonstrict;
<br>set hive.exec.dynamic.partition=true;
<br>set hive.optimize.sort.dynamic.partition=true;
<br>
<br>set mapred.reduce.tasks=-1;
<br>set hive.tez.auto.reducer.parallelism=true;
<br>set hive.tez.min.partition.factor=0.25; 
<br>set hive.tez.max.partition.factor=2.0;
<br>set yarn.nodemanager.resource.memory-mb = Usually between 75% - 87.5% RAM
<br>set yarn.scheduler.minimum-allocation-mb = Memory per processor (or less)
<br>set yarn.scheduler.maximum-allocation-mb = yarn.nodemanager.resource.memory-mb
<br>set hive.tez.container.size = yarn.scheduler.minimum-allocation-mb (1 or 2 times) and less than yarn.scheduler.maximum-allocation-mb
<br>
<br>Setup ORC:
<br>```CREATE TABLE A_ORC (ID int, name string, value float) STORED AS ORC tblproperties (“orc.compress" = “SNAPPY”);```
<br>
<br>```INSERT INTO TABLE A_ORC SELECT * FROM A;```
<br>
<br>Create table and column stats:
<br>```ANALYZE TABLE myORCtable partition (col1, col2, col3) COMPUTE STATISTICS;```
<br>```ANALYZE TABLE myORCtable partition (col1, col2, col3) COMPUTE STATISTICS for columns;```
<br>
<br><img src="images/hive_tez_tuning_1.jpg" class="inline"/>
<br>
<br><b>References:</b>
<br><a href="http://docs.hortonworks.com/HDPDocuments/HDP2/HDP-2.5.3/bk_hive-performance-tuning/content/ch_hive_architectural_overview.html">Hortonworks - Apache Hive Tuning for High Performance</a>
<br><a href="https://community.hortonworks.com/content/kbentry/14309/demystify-tez-tuning-step-by-step.html">Apache Hive on Tez - Tuning Best Practices (Part 1)</a>
<br><a href="https://community.hortonworks.com/articles/22419/hive-on-tez-performance-tuning-determining-reducer.html">Apache Hive on Tez - Tuning Best Practices (Part 2)</a>
<br><a href="http://docs.hortonworks.com/HDPDocuments/HDP2/HDP-2.5.3/bk_hive-performance-tuning/content/section_create_configure_yarn_capacity_scheduler_queues.html">Capacity Scheduler Queues - Allocate cluster resources among users and groups</a>
<br><a href="http://hortonworks.com/blog/5-ways-make-hive-queries-run-faster/">5 Ways to Improve Hive Performance</a>
<br>
<br>
<br>
<br><img src="images/Apache_Spark_logo.jpg" class="inline"/>
<br><h3>Tuning Tips and Tricks</h3>
<br>
<br><b>1. Improve Caching:</b> 
<br>&ensp;&ensp;&ensp;MEMORY_ONLY: (default/recommended) Store RDD as deserialized objects in JVM Heap
<br>&ensp;&ensp;&ensp;MEMORY_ONLY_SER: (2nd option) Store RDD as serialized Java objects. Trade CPU time for memory savings
<br>&ensp;&ensp;&ensp;MEMORY_AND_DISK: Spill to disk if can’t fit in memory
<br>&ensp;&ensp;&ensp;MEMORY_AND_DISK_SER: Spill serialized RDD to disk if it can’t fit in memory
<br>
<br><br><b>Configuration Suggestions:</b>
<br>Normally 3 - 6 executors per node is a reasonable, depends on the CPU cores and memory size per executor
<br>set spark.default.parallelism = 2-3 tasks per CPU core in your cluster
<br>conf.set(“spark.serializer”, “org.apache.spark.serializer.KryoSerializer”)
<br>Measure time spent in GC by logging: -verbose:gc –XX:+PrintGCDetails –XX:+PrintGCTimeStamps
<br>
<br><b>References:</b>
<br><a href="https://spark.apache.org/docs/latest/tuning.html">Apache Spark (latest) General Tuning</a>
<br><a href="http://spark.apache.org/docs/latest/configuration.html#Dynamically-Loading-Spark-Properties">Apache Spark (latest) Properties / Configuration Settings</a>
<br><a href="http://docs.hortonworks.com/HDPDocuments/HDP2/HDP-2.5.3/bk_spark-component-guide/content/ch_tuning-spark.html">Hortonworks - Apache Spark Tuning Guide</a>
<br><a href="https://databricks.com/blog/2015/05/28/tuning-java-garbage-collection-for-spark-applications.html">Tuning Java Garbage Collection</a>
