
########################################################################################
#
#  This code is used to benchmark, then optimize your Hive queries & environment
#
#  NOTE: Please change "yourTableName" to make the Hive table you are testing against.
#
########################################################################################

# Get info on your table:
describe formatted yourTableName;

# Get create table info for your table:
show create table yourTableName;

# Run your query (To get current runtime as a baseline):
select count(*) from yourTableName;

# Output Explain plan:
explain select count(*) from yourTableName;

# Set Tez Execution Engine as Tez (instead of MapReduce)
set hive.execution.engine=tez;

# Enable Vectorization
set hive.vectorized.execution.enabled = true;
set hive.vectorized.execution.reduce.enabled = true;

# Use Cost-Based Optimization
set hive.cbo.enable=true;
set hive.compute.query.using.stats=true;
set hive.stats.fetch.column.stats=true;
set hive.stats.fetch.partition.stats=true;
set hive.stats.autogather=true;

# Compute Table Stats and Column Stats (for CBO to use)
analyze table yourTableName compute statistics;
analyze table yourTableName compute statistics for columns;
#ANALYZE TABLE yourTableName partition (yourCol1, yourCol2, yourCol3) COMPUTE STATISTICS; 
#ANALYZE TABLE yourTableName partition (yourCol1, yourCol2, yourCol3) COMPUTE STATISTICS for columns; 

# Additional Hive Tuning Parameters:
set mapred.reduce.tasks=-1;                 # Automatically set reducer count, with a max of hive.exec.reducers.max
set hive.tez.auto.reducer.parallelism=true; # Hive will estimate data sizes and set parallelism estimates by sampling source vertices
set hive.exec.parallel=true; 
#set mapred.compress.map.output=true;
#set mapred.output.compress=true;
#set hive.exec.compress.output=true;

# Run your optimized query plan (To get new runtime - compare against baseline):
select count(*) from yourTableName;

# Output Explain plan:
explain select count(*) from yourTableName;

#ZEND
