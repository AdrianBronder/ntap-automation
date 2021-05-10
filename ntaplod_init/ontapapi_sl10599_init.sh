#!/usr/bin/env bash

################################################################################
#
# Title:        ontapapi_sl10599_init.sh
# Author:       Adrian Bronder
# Date:         2020-09-03
# Description:  Prepare linux host "ansible" in LoD lab sl10599
#               --> "Exploring the ONTAP REST API v1.3"
#
# URLs:         https://labondemand.netapp.com/lab/sl10599 (NetApp + Partner)
#               https://handsonlabs.netapp.com/lab/ontapapi (Customer)
#               http://docs.netapp.com/ontap-9/index.jsp
#               https://pypi.org/project/netapp-ontap/
#               https://galaxy.ansible.com/netapp/ontapa
#
# Change Log:   - 2021-05-10: Lab update to v1.3
#                 Multiple changes required to prep environment (on "ansible")
#
################################################################################

echo "--> Updating Red Hat system"
yum -y update

echo "--> Remove AWX"
docker stop awx_task awx_web awx_rabbitmq awx_memcached awx_postgres
docker rm awx_task awx_web awx_rabbitmq awx_memcached awx_postgres
docker image rm ansible/awx_task:9.1.1 ansible/awx_web:9.1.1 postgres:10 ansible/awx_rabbitmq:3.7.4
docker volume prune -f
rm -rf ~/awx ~/.awx

echo "--> Remove Ansible"
sudo -u ansible pip3 uninstall -y ansible
sudo -u ansible rm -rf ~/.ansible

echo "--> Remove Python3"
yum remove -y python3
rm -f /usr/bin/python3
rm -f /usr/bin/pip3

echo "--> Add repositories"
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
curl -sL https://rpm.nodesource.com/setup_14.x | sudo bash -

echo "--> Installing additional packages"
yum install -y wget gcc libffi-devel epel-release zlib-devel openssl-devel jq libxml2 git docker-ce docker-ce-cli containerd.io nodejs

echo "--> Install Python3"
mkdir /tmp/download-python
wget -P /tmp/download-python https://www.python.org/ftp/python/3.9.1/Python-3.9.1.tgz
tar xf /tmp/download-python/Python-3.9.1.tgz -C /opt/
cd /opt/Python-3.9.1
./configure --enable-optimizations
make altinstall
ln -s /usr/local/bin/python3.9 /usr/bin/python3
ln -s /usr/local/bin/pip3.9 /usr/bin/pip3
sudo -u ansible cd ~

echo "--> Upgrading pip"
pip3 install --upgrade pip

echo "--> Installing Asnible"
sudo -u ansible pip3 install ansible

echo "--> Installing additional Python libs"
sudo -u ansible pip3 install --upgrade requests six netapp_lib docker docker-compose selinux
sudo -u ansible pip3 install --upgrade "pywinrm[kerberos]>=0.3.0"

echo "--> Installing additional ansible collections (ONTAP, UM, Windows, AWX)"
sudo -u ansible ansible-galaxy collection install netapp.ontap
sudo -u ansible ansible-galaxy collection install netapp.um_info
sudo -u ansible ansible-galaxy collection install community.windows
sudo -u ansible ansible-galaxy collection install awx.awx:17.1.0

echo "--> Install docker images"
sudo -u ansible cat ~/ntap-automation/ntaplod_init/docker_images/awx_17_lod_db_images.tar.gz.* > ~/ntap-automation/ntaplod_init/docker_images/awx_17_lod_db_images.tar.gz
sudo -u ansible docker load < ~/ntap-automation/ntaplod_init/docker_images/awx_17_lod_db_images.tar.gz

echo "--> Installing AWX"
sudo -u ansible git clone -b 17.1.0 https://github.com/ansible/awx
sudo -u ansible sed -i 's/^\# admin_password=password$/admin_password=Netapp1!/' ~/awx/installer/inventory
sudo -u ansible ansible-playbook -i awx/installer/inventory awx/installer/install.yml

echo "--> Installing libraries and collections in AWX container"
sudo -u ansible docker exec -it awx_task pip3 install --upgrade requests six netapp_lib
sudo -u ansible docker exec -it awx_task ansible-galaxy collection install netapp.ontap -p /usr/share/ansible/collections -f
sudo -u ansible docker exec -it awx_task ansible-galaxy collection install netapp.um_info -p /usr/share/ansible/collections -f

echo "--> Creating aggrgates on primary cluster (cluster 1)"
$(dirname $0)/ontapapi_sl10599_init_helper/sl10599_init_cluster.sh

echo "--> Creating Users and groups in AD (dc1)"
$(dirname $0)/ontapapi_sl10599_init_helper/sl10599_init_ad.yml -i $(dirname $0)/ontapapi_sl10599_init_helper/init_inventory

echo "--> Configuring AWX (demo.netapp.com)"
$(dirname $0)/ontapapi_sl10599_init_helper/sl10599_init_awx.yml


