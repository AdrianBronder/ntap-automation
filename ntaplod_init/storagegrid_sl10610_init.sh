#!/usr/bin/env bash

################################################################################
#
# Title:        sl10610_init.sh
# Author:       Adrian Bronder
# Date:         2020-06-18
# Description:  Prepare linux host "Linux1" in LoD lab sl10610
#               --> "Enterprise Object Storage in the Data Fabric
#                   with StorageGRID v1.0"
#
# URLs:         https://labondemand.netapp.com/lab/sl10610 (NetApp + Partner)
#               https://handsonlabs.netapp.com/lab/storagegrid (Customer)
#               https://docs.netapp.com/sgws-113/index.jsp
#               https://galaxy.ansible.com/netapp/storagegrid
#
################################################################################

echo "--> Updating Red Hat system"
yum -y update

echo "--> Installing additional packages"
yum -y install wget gcc libffi-devel epel-release zlib-devel openssl-devel jq

echo "--> Installing Python 3.7.6 (as alternative version)"
wget -P /opt/ https://www.python.org/ftp/python/3.7.6/Python-3.7.6.tgz
tar xf /opt/Python-3.7.6.tgz -C /opt/
cd /opt/Python-3.7.6
./configure --enable-optimizations
make altinstall
ln -s /usr/local/bin/python3.7 /usr/bin/python3
ln -s /usr/local/bin/pip3.7 /usr/bin/pip3
cd ~

echo "--> Upgrading pip"
pip install --upgrade pip
pip3 install --upgrade pip

echo "--> Make sure, required packages for Python are installed"
pip install requests selinux boto3
pip3 install requests selinux boto3

echo "--> Installing Ansible"
pip3 install ansible

echo "--> Installing StorageGRID collection for Ansible"
ansible-galaxy collection install -f netapp.storagegrid

echo ""
echo ""
echo ">>> MANUAL STEP MIGHT BE REQUIRED <<<"
echo "In case downloading collections from Ansible Galaxy fails:"
echo "- Please load 'netapp.storagegrid' collection from another"
echo "  location and install it manually with e.g. this command:"
echo ""
echo "# ansible-galaxy collection install ./netapp-storagegrid-20.6.1.tar.gz -p ~/.ansible/collections"
echo ""
