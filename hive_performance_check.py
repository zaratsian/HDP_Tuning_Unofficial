
###################################################################################################
#
#   Hive Tuning Tool (via Ambari)
#   Dan Zaratsian, 15-JUL-2017
#
#   This tool will extract cluster information from your cluster (via Ambari APIs), then the 
#   code will use these extracted parameters in order to calculate the optimal Spark configuration.
#
#   Usage: hive_performance_check.py --ambari_hostname=dzaratsian_hdp.com --ambari_port=8080 --cluster_name=dz_hdp --username=admin --password=admin
#
#   Tested on HDP 2.6.0 (Ambari 2.5.1.0 , HDFS 2.7.3, YARN 2.7.3, Hive 1.2.1000)
#   CentOS Linux release 7.3.1611 (Core) with Python 2.7.5
#
#   https://docs.hortonworks.com/HDPDocuments/HDP2/HDP-2.6.1/bk_hive-performance-tuning/content/ch_hive-perf-tuning-intro.html
#   https://github.com/zaratsian/HDP_Tuning_Unofficial
#   https://github.com/apache/ambari/blob/trunk/ambari-server/docs/api/v1/index.md#resources
#
###################################################################################################


import sys,re
import getopt
import requests
import json
import math


file = '/tmp/hive_performance_check.txt'
output_file = open(file,'wb')


try:
    opts, args = getopt.getopt(sys.argv[1:], 'x', ['ambari_hostname=', 'ambari_port=', 'cluster_name=', 'username=', 'password='])
    
    ambari_hostname     = [opt[1] for opt in opts if opt[0]=='--ambari_hostname'][0]
    ambari_port         = [opt[1] for opt in opts if opt[0]=='--ambari_port'][0]
    cluster_name        = [opt[1] for opt in opts if opt[0]=='--cluster_name'][0]
    username            = [opt[1] for opt in opts if opt[0]=='--username'][0]
    password            = [opt[1] for opt in opts if opt[0]=='--password'][0]
    expected_concurrent_queries = 5
except:
    print '\n\n[ USAGE ] hive_performance_check.py --ambari_hostname=<hostname> --ambari_port=<port> --cluster_name=<cluster_name> --username=<string> --password=<string>\n\n'
    sys.exit(1)



def get_datanode_parameters(ambari_hostname, ambari_port, cluster_name, username, password):
    
    nodes_names = []
    node_cores  = []
    node_ram    = []  
    
    url = 'http://' + str(ambari_hostname) + ':' + str(ambari_port) + '/api/v1/clusters/' + str(cluster_name) + '/services/HDFS/components/DATANODE'
    print '[ INFO ] Collection data from ' + str(url)
    req = requests.get(url, auth=(username,password) )
    
    if req.status_code == 200:
        cluster_info = json.loads(req.content)
        
        for host in cluster_info['host_components']:
            url = host['href'].replace('/host_components/DATANODE','')
            print '[ INFO ] Collection data from ' + str(url)
            req2 = requests.get(url, auth=(username,password) )
            host_info = json.loads(req2.content)
            
            nodes_names.append(host['HostRoles']['host_name'])
            node_cores.append(host_info['Hosts']['cpu_count'])
            node_ram.append( int(math.floor(host_info['Hosts']['total_mem'] / float(1000*1000))) )
    
    node_count = len(nodes_names)
    node_cores = min(node_cores)
    node_ram   = min(node_ram)
    
    return (node_count, node_cores, node_ram)


node_count, node_cores, node_ram = get_datanode_parameters(ambari_hostname, ambari_port, cluster_name, username, password)


total_cores = node_count * node_cores
total_ram   = node_count * node_ram


def get_yarn_parameters(ambari_hostname, ambari_port, cluster_name, username, password):
    
    url = 'http://' + str(ambari_hostname) + ':' + str(ambari_port) + '/api/v1/clusters/' + str(cluster_name) + '/configurations/service_config_versions?service_name=YARN&service_config_version=1'
    print '[ INFO ] Collection data from ' + str(url)
    req = requests.get(url, auth=(username,password))
    
    yarn_parameters = {}
    
    if req.status_code == 200:
        cluster_info = json.loads(req.content)
        
        yarn_site = [config for config in cluster_info['items'][0]['configurations'] if config['type']=='yarn-site']
        
        yarn_nodemanager_resource_memory_mb   = int(yarn_site[0]['properties']['yarn.nodemanager.resource.memory-mb'])
        #yarn_nodemanager_resource_memory_mb  = (node_ram - 2) * 1024
        
        yarn_nodemanager_resource_cpu_vcores  = int(yarn_site[0]['properties']['yarn.nodemanager.resource.cpu-vcores'])
        #yarn_nodemanager_resource_cpu_vcores = (node_cores - 1)
        
        yarn_parameters['yarn.nodemanager.resource.memory-mb']  = yarn_nodemanager_resource_memory_mb
        yarn_parameters['yarn.nodemanager.resource.cpu-vcores'] = yarn_nodemanager_resource_cpu_vcores
        for key,value in yarn_site[0]['properties'].items():      yarn_parameters[key]=value
    
    return (yarn_parameters)


yarn_parameters = get_yarn_parameters(ambari_hostname, ambari_port, cluster_name, username, password)


def get_hive_parameters(ambari_hostname, ambari_port, cluster_name, username, password):
    
    url = 'http://' + str(ambari_hostname) + ':' + str(ambari_port) + '/api/v1/clusters/' + str(cluster_name) + '/configurations/service_config_versions?service_name=HIVE&service_config_version=1'
    print '[ INFO ] Collection data from ' + str(url)
    req = requests.get(url, auth=(username,password))
    
    hive_parameters = {}
    
    if req.status_code == 200:
        cluster_info = json.loads(req.content)
        
        hive_site           = [config for config in cluster_info['items'][0]['configurations'] if config['type']=='hive-site']
        hive_env            = [config for config in cluster_info['items'][0]['configurations'] if config['type']=='hive-env']
        hiveserver2_site    = [config for config in cluster_info['items'][0]['configurations'] if config['type']=='hiveserver2-site']
        
        for key,value in hive_site[0]['properties'].items():        hive_parameters[key]=value
        
        for key,value in hive_env[0]['properties'].items():         hive_parameters[key]=value
        
        for key,value in hiveserver2_site[0]['properties'].items(): hive_parameters[key]=value
    
    return (hive_parameters)


hive_parameters = get_hive_parameters(ambari_hostname, ambari_port, cluster_name, username, password)


recommendations = {}

# General Recommendations:
recommendations['hive.execution.engine=tez']                    = 'true'
recommendations['hive.vectorized.execution.enabled']            = 'true'
recommendations['hive.vectorized.execution.reduce.enabled']     = 'true'
recommendations['hive.cbo.enable']                              = 'true'
recommendations['hive.compute.query.using.stats']               = 'true'

if expected_concurrent_queries <= 20:
    recommendations['hive.heapsize'] = '6000' # MB
elif 20 < expected_concurrent_queries <= 40:
    recommendations['hive.heapsize'] = '12000' # MB
elif expected_concurrent_queries > 40:
    recommendations['hive.heapsize'] = 'Create a new HiveServer2 Instance'
else:
    recommendations['hive.heapsize'] = ''

recommendations['hive.tez.container.size']                          = int(yarn_parameters['yarn.scheduler.minimum-allocation-mb']) * 2
recommendations['tez.am.resource.memory.mb']                        = yarn_parameters['yarn.scheduler.minimum-allocation-mb']
recommendations['yarn.scheduler.maximum-allocation-mb']             = yarn_parameters['yarn.nodemanager.resource.memory-mb']
recommendations['tez.runtime.io.sort.mb']                           = recommendations['hive.tez.container.size'] * 0.40
recommendations['hive.auto.convert.join.noconditionaltask']         = 'true'
recommendations['hive.auto.convert.join.noconditionaltask.size']    = recommendations['hive.tez.container.size'] * 0.33
recommendations['tez.runtime.unordered.output.buffer.size-mb']      = recommendations['hive.tez.container.size'] * 0.10
recommendations['tez.grouping.min-size']                            = '16777216'
recommendations['tez.grouping.max-size']                            = '1073741824'

# Output Summary
log_msg = '\n\n' + '#'*100 + '\n'
log_msg = log_msg + '\nBEST PRACTICES:\n'
log_msg = log_msg + '\n     -  Store all data in ORCFile'
log_msg = log_msg + '\n     -  Use Tez execution engine (instead of MR)'
log_msg = log_msg + '\n     -  Enable CBO (Cost-Based Optimizer)'
log_msg = log_msg + '\n     -  Collect Table Statistics  [ANALYZE TABLE [table_name] COMPUTE STATISTICS;]'
log_msg = log_msg + '\n     -  Collect Column Statistics [ANALYZE TABLE [table_name] COMPUTE STATISTICS for COLUMNS;]'
log_msg = log_msg + '\n'
log_msg = log_msg + '\n\nRECOMMENDATIONS:\n'
for k,v in recommendations.items(): log_msg = log_msg + '\nset ' + str(k) + '=' + str(v) + ';'
log_msg = log_msg + '\n'
log_msg = log_msg + '\n\nResults and Config have been written to ' + str(file)
log_msg = log_msg + '\n\n' + '#'*100 + '\n'

print log_msg

output_file.write(log_msg)
output_file.write('\n\n' + '#'*100 + '\n')
output_file.write('\nCLUSTER CONFIGS:\n')
for k,v in yarn_parameters.items():  output_file.write('\nset ' + str(k) + '=' + str(v) + ';')
for k,v in hive_parameters.items():  output_file.write('\nset ' + str(k) + '=' + str(v) + ';')
output_file.write('\n\n' + '#'*100 + '\n')

output_file.close()


# To Do:



#ZEND
