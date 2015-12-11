#!/usr/bin/python

"""
A script that will approve a puppet cert if the serial number is in Sal.
Mostly stolen from https://github.com/macadmins/docker-puppetmaster-whdcli/blob/master/check_csr.py
"""

import os
import sys
import subprocess
import requests
import json
import logging


LOG_FILENAME = '/var/log/check_csr.out'

logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)
logger = logging.getLogger(__name__)

def my_handler(type, value, tb):
    logger.exception("Uncaught exception: {0}".format(str(value)))
sys.excepthook = my_handler
logger.info('Start script')

for key in os.environ.keys():
    logger.info("%30s %s \n" % (key,os.environ[key]))

sal_url = os.getenv('SAL_PUPPETSERVER_URL', 'http://sal')
logger.info("Sal URL: %s", sal_url)
public_key = os.getenv('SAL_PUPPETSERVER_PUBLIC_KEY', '123')
logger.info("Public Key: %s", public_key)
private_key = os.getenv('SAL_PUPPETSERVER_PRIVATE_KEY', '123')
logger.info("Private Key: %s", private_key)
if s.getenv('SAL_PUPPETSERVER_VERIFY', 'True').lower == 'false':
    verify = False
else:
    verify = True

try:
    hostname = sys.argv[1]
    logger.info("Hostname: %s", hostname)
except:
    logger.info("Wasn't sent the hostname.")

if hostname == "puppet":
    logger.info("It's the puppetmaster, of course we approve it.")
    sys.exit(0)

certreq = sys.stdin.read()
logger.info(certreq)

cmd = ['/usr/bin/openssl', 'req', '-noout', '-text']
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(output, err) = proc.communicate(certreq)

lineList = output.splitlines()

strippedLineList = [line.lstrip() for line in lineList]
strippedLineList2 = [line.rstrip() for line in strippedLineList]

try:
    trusted_attribute1 = strippedLineList2.index("1.3.6.1.4.1.34380.1.2.1.1:")
except:
    logger.info("No serial number in CSR. Rejecting CSR.")
    sys.exit(1)

serial_number = strippedLineList2[trusted_attribute1+1].upper()

logger.info("Serial number: %s", serial_number)

api_url = sal_url+'/api/machines/'+serial_number+'/'

headers = {'privatekey': private_key, 'publickey': public_key}
r = requests.get(api_url, headers=headers, verify=verify)
logger.info(r.text)

# We get json back.
try:
    machine = json.loads(r.text)
except:
    logger.info("No JSON response.")
    sys.exit(1)

# Found a matching serial
if 'serial' in machine:
    if machine['serial'] == serial_number:
        logger.info("Found serial number in inventory. Approving.")
        sys.exit(0)
else:
    logger.info("Serial number not found in inventory.")
    sys.exit(1)
