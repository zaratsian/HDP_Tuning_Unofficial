<h3>Unofficial Guide for Tuning HDP Services</h3>

<br>####################################################################
<br>#
<br>#&ensp;&ensp;<b>Apache Hive</b>
<br>#
<br>####################################################################
<br>
<br>&bull; Enable Tez
<br>&bull; Store as ORC and use Zlib/Snappy compression
<br>&bull; Use Vectorization
<br>&bull; Use CBO (Cost-Based Optimizer) with Column Stats (CBO requires stats)
<br>&bull; Write Good SQL
<br>
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
<br><label><input type="checkbox" id="111" value="111">set hive.exec.dynamic.partition=true;</label>
<br><label><input type="checkbox" id="222" value="222">set hive.optimize.sort.dynamic.partition=true;</label>
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
<br><b>References:</b>
<br><a href="http://docs.hortonworks.com/HDPDocuments/HDP2/HDP-2.5.3/bk_hive-performance-tuning/content/ch_hive_architectural_overview.html">Hortonworks - Apache Hive Tuning for High Performance</a>
<br><a href="https://community.hortonworks.com/content/kbentry/14309/demystify-tez-tuning-step-by-step.html">Apache Hive on Tez - Tuning Best Practices (Part 1)</a>
<br><a href="https://community.hortonworks.com/articles/22419/hive-on-tez-performance-tuning-determining-reducer.html">Apache Hive on Tez - Tuning Best Practices (Part 2)</a>
<br><a href="http://hortonworks.com/blog/5-ways-make-hive-queries-run-faster/">5 Ways to Improve Hive Performance</a>
