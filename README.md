<h3>Unofficial Guide for Tuning HDP Services</h3>

<br><b>Apache Hive</b>
<br>- Enable Tez
<br>&ensp;&ensp;&ensp;&ensp;```http://openflights.org/data.html```
<br>- Use ORC compressed storage
<br>```CREATE TABLE A_ORC (customerID int, name string, age int, address string) STORED AS ORC tblproperties (“orc.compress" = “SNAPPY”);```
<br>- Use Vectorization
<br>&ensp;&ensp;&ensp;&ensp;```set hive.vectorized.execution.enabled = true;```
<br>&ensp;&ensp;&ensp;&ensp;```set hive.vectorized.execution.reduce.enabled = true;```
<br>- Enable CBO (Cost-Based Optimization)
<br>&ensp;&ensp;&ensp;&ensp;```set hive.cbo.enable=true;```
<br>&ensp;&ensp;&ensp;&ensp;```set hive.compute.query.using.stats=true;```
<br>&ensp;&ensp;&ensp;&ensp;```set hive.stats.fetch.column.stats=true;```
<br>&ensp;&ensp;&ensp;&ensp;```set hive.stats.fetch.partition.stats=true;```
<br>- Write Good SQL
<br>
<br><b>References:</b>
<br><a href="https://community.hortonworks.com/articles/22419/hive-on-tez-performance-tuning-determining-reducer.html">Hive on Tez</a>
<br><a href="http://hortonworks.com/blog/5-ways-make-hive-queries-run-faster/">5 Ways to Improve Hive Performance</a>
