#!/bin/bash

sed -i -e "s*REPLACE_URL*$SAL_PUPPETSERVER_URL*g" /sal_cert.py
sed -i -e "s/REPLACE_PUBLIC/$SAL_PUPPETSERVER_PUBLIC_KEY/g" /sal_cert.py
sed -i -e "s/REPLACE_PRIVATE/$SAL_PUPPETSERVER_PRIVATE_KEY/g" /sal_cert.py
sed -i -e "s/REPLACE_VERIFY/$SAL_PUPPETSERVER_VERIFY/g" /sal_cert.py

cat << EOF >> /etc/default/puppetserver
###########################################
# Init settings for puppetserver
###########################################

# Location of your Java binary (version 7 or higher)
JAVA_BIN="/usr/bin/java"

# Modify this if you'd like to change the memory allocation, enable JMX, etc
JAVA_ARGS="$PUPPETSERVER_JAVA_ARGS"

# These normally shouldn't need to be edited if using OS packages
USER="puppet"
INSTALL_DIR="/usr/share/puppetserver"
CONFIG="/etc/puppetserver/conf.d"
BOOTSTRAP_CONFIG="/etc/puppetserver/bootstrap.cfg"
SERVICE_STOP_RETRIES=60

# START_TIMEOUT can be set here to alter the default startup timeout in
# seconds.  This is used in System-V style init scripts only, and will have no
# effect in systemd.
# START_TIMEOUT=120
EOF

PUPPETDB_IP="${PUPPETDB_PORT_8081_TCP_ADDR:=abc}"

if [ "$PUPPETDB_IP" != "abc" ]
    then

    PUPPETDB_CONF=/etc/puppet/puppetdb.conf
    cat << EOF >> $PUPPETDB_CONF
[main]
server = $PUPPETDB_PORT_8081_TCP_ADDR
port = $PUPPETDB_PORT_8081_TCP_PORT
EOF
fi

puppetserver foreground
