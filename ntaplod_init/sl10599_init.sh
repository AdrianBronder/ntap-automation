#!/usr/bin/env bash

################################################################################
#
# Title:        sl10599_init.sh
# Author:       Adrian Bronder
# Date:         2020-09-03
# Description:  Prepare linux host "rhel1" in LoD lab sl10599
#               --> "Exploring the ONTAP REST API v1.2"
#
# URLs:         https://labondemand.netapp.com/lab/sl10599 (NetApp + Partner)
#               https://handsonlabs.netapp.com/lab/ontapapi (Customer)
#               http://docs.netapp.com/ontap-9/index.jsp
#               https://pypi.org/project/netapp-ontap/
#               https://galaxy.ansible.com/netapp/ontap
#
################################################################################

echo "--> Updating Red Hat system"
yum -y update

echo "--> Installing additional packages"
yum -y install jq

echo "--> Upgrading pip"
pip install --upgrade pip

echo "--> Installing NetApp Python lib (for ZAPI use)"
pip install netapp_lib

echo "--> Creating links for Python3"
ln -s /usr/local/bin/python3.7 /usr/bin/python3
ln -s /usr/local/bin/pip3.7 /usr/bin/pip3

echo "--> Installing ONTAP and Active IQ Unified Manager collections for Ansible"
ansible-galaxy collection install netapp.ontap
ansible-galaxy collection install netapp.um_info

echo "--> Creating aggrgates on primary cluster (cluster 1)"
$(dirname $0)/sl10599_init_cluster.sh



### REMOVED FROM 1.1 to 1.2 (already installed in LoD or not relevant anymore):
: '
echo "--> Installing additional packages"
yum -y install epel-release zlib-devel openssl-devel jq

echo "--> Installing Python 3.8.2 (as alternative version)"
wget -P /opt/ https://www.python.org/ftp/python/3.8.2/Python-3.8.2.tgz
tar xf /opt/Python-3.8.2.tgz -C /opt/
cd /opt/Python-3.8.2
./configure --enable-optimizations
make altinstall
ln -s /usr/local/bin/python3.8 /usr/bin/python3
ln -s /usr/local/bin/pip3.8 /usr/bin/pip3
cd ~

echo "--> Upgrading Python pip (for both versions)"
pip install --upgrade pip
pip3 install --upgrade pip

echo "--> Installing ONTAP Python client libraries and dependencies"
pip install requests marshmallow
pip install netapp-lib
pip3 install requests marshmallow
pip3 install netapp-lib
pip3 install netapp-ontap

echo "--> Installing Ansible"
yum -y install ansible
'
