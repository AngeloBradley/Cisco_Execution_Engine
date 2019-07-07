import re
import yaml
import time
from paramiko import AutoAddPolicy, SSHClient

def is_testbed_available(traffic_gen):
    # Get process info including runtrex string
    stdin,stdout,stderr = traffic_gen.exec_command('ps -ef | grep runtrex')

    # search through the output of the ps command
    for line in stdout.readlines():
        # if a line contains runtrex
        if re.search(r'runtrex', line):
            # and it doesn't contain grep
            if not re.search(r'grep', line):
                # the testbed is busy - so return False
                print('The testbed is busy!')
                return False

    # Did not find any instances of runtrex
    return True




def connect_traffic_gen(params,retries):
    '''
    This function is to connect to traffic generator and run traffic

    '''
    traffic_gen = SSHClient()
    traffic_gen.set_missing_host_key_policy(AutoAddPolicy())
    print('Connecting to traffic generator {}'.format(params["traffic_gen"]["IP"]))
    for x in range(retries):
        try:
            traffic_gen.connect( params["traffic_gen"]["IP"], port=22, username = params["traffic_gen"]["Username"], password = params["traffic_gen"]["Password"],allow_agent=False,look_for_keys=False,auth_timeout=30,passphrase=None)
            # only start traffic if the testbed is available
            if is_testbed_available(traffic_gen):
                print('\nConnected to traffic generator...preparing to run traffc...')
                stdin,stdout,stderr = traffic_gen.exec_command('cd trex/v2.24;./runtrex')
                time.sleep(60)
                traffic_gen.close()
                return True
            else:
                traffic_gen.close()
                return False

        except Exception as e:
            print('\nSSH Connection error! {}, Retrying again...'.format(e))
            time.sleep(5)

    return False

def connect_csr1000v(params,retries):
    '''
    This function is to connect to csr1000v and run 'show commnds'

    '''
    csr1000v = SSHClient()
    csr1000v.set_missing_host_key_policy(AutoAddPolicy())
    print('\nConnecting to csr1000v {}'.format(params["csr1000v"]["IP"]))
    for x in range(retries):
        try:
            csr1000v.connect( params["csr1000v"]["IP"], port=22, username = params["csr1000v"]["Username"], password = params["csr1000v"]["Password"],allow_agent=False,look_for_keys=False,auth_timeout=30,passphrase=None)
            print('\nConnected to csr1000v...checking for traffic on interfaces...')
            stdin,stdout,stderr = csr1000v.exec_command('show interfaces summary')
            output = stdout.readlines()
            csr1000v.close()
            pattern = r'.*?GigabitEthernet[\d+](\s*\d+){4}\s*([1-9]\d.*)'
            output = str(output)
            ret = re.search(pattern,output)
            if ret:
                return True, output
            else:
                return False, output

        except Exception as e:
            print('\nSSH Connection error! {}, Retrying again...'.format(e))
            time.sleep(5)

    return False,'Failed to connect {}!!!'.format(params["csr1000v"]["IP"])


#Load the yaml file to read parameters needed for test
with open('params.yaml', 'r') as f:
    params = yaml.load(f)

#Connect to the csr1000v anf traffic generator and see if traffic is running between them.
status = connect_traffic_gen(params,retries=5)
if status:
    print('\nTraffic generator is up and sending traffic...')
else:
    print('\nTraffic generator is not running or testbed is busy...please give it a try again...')
    exit(1)

status,output = connect_csr1000v(params,retries=5)
if status:
    print('\nTraffic test Passed...\n\nThe RX/TX counters for interfaces got updated...\n\n{}'.format(output))
else:
    print('\nTraffic test failed...{}'.format(output))

print('\nTest Done !!!')
exit(0)