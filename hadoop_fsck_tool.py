

# Run this python program against output from:
# hdfs fsck / > /tmp/test.txt

import re

file = open('/tmp/test.txt','rb')

data = file.read()

lines = data.split('\n')

for line in lines:
    if re.search('Replic',line):
        
        path = re.findall('^.*?\:',line)[0]
        replication = re.findall('Target Replicas is [0-9]+ but found [0-9]+ live replica',line)[0]
        replication_factor = re.sub('Target Replicas is ','',re.findall('Target Replicas is [0-9]+',replication)[0])
        if replication_factor > 3:
            print str(replication) + '\t\t' + str(replication_factor) + '\t\t' + str(path)






# Run this python program against output from:
# hdfs dfs -lsr / > /tmp/newlsr.txt

import re

file = open('/tmp/newlsr.txt','rb')

data = file.read()

lines = data.split('\n')

for line in lines:
    if int(line.split()[4]) >= 100000000000:
        
        print str(line.split()[4]) + '\t\t' + str(line.split()[1]) + '\t\t' + str(line.split()[7])


#ZEND
