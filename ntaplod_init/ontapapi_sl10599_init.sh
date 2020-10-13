#!/usr/bin/env bash

################################################################################
#
# Title:        ontapapi_sl10599_init.sh
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
pip3 install --upgrade pip

echo "--> Upgrading Asnible"
pip3 install --upgrade ansible

echo "--> Installing additional Python libs"
pip3 install --upgrade netapp_lib
pip3 install "pywinrm[kerberos]>=0.3.0"

echo "--> Creating links for Python3"
ln -s /usr/local/bin/python3.8 /usr/bin/python3
ln -s /usr/local/bin/pip3.8 /usr/bin/pip3

echo "--> Installing additional ansible collections (ONTAP, UM, Windows, AWX)"
ansible-galaxy collection install netapp.ontap
ansible-galaxy collection install netapp.um_info
ansible-galaxy collection install community.windows
ansible-galaxy collection install awx.awx

echo "--> Installing libraries and collections in AWX container"
docker exec -it awx_task pip3 install --upgrade netapp_lib
docker exec -it awx_task ansible-galaxy collection install netapp.ontap -p /usr/share/ansible/collections -f
docker exec -it awx_task ansible-galaxy collection install netapp.um_info -p /usr/share/ansible/collections -f

echo "--> Creating aggrgates on primary cluster (cluster 1)"
$(dirname $0)/ontapapi_sl10599_init_helper/sl10599_init_cluster.sh

echo "--> Creating Users and groups in AD (dc1)"
$(dirname $0)/ontapapi_sl10599_init_helper/sl10599_init_ad.yml -i $(dirname $0)/ontapapi_sl10599_init_helper/init_inventory

echo "--> Configuring AWX (rhel1)"
$(dirname $0)/ontapapi_sl10599_init_helper/sl10599_init_awx.yml



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
