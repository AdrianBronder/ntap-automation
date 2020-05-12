# NetApp Automation Demos

Welcome to my collection of automation demos. In this repository you will find various examples on how to automate administrative and operational tasks on NetApp solutions. The main purpose is enabling you writing your own scripts/integartions by providing simple examples in small chunks. The scripts in this repository are not tuned for production use.

## Quick Start
If you are a customer, partner or NetApp employee:

1. Please use the virtual hands-on lab (log in with your NetApp support account):
   Customer: https://handsonlabs.netapp.com/lab/ontapapi
   NetApp Partner: https://labondemand.netapp.com/lab/sl10599

2. Log into the first Linux machine (rhel1) and clone this repository:
   ```
   git clone https://github.com/AdrianBronder/ntap-automation.git
   ```

3. Initialize the environment by running the lab init script:
   ```
   ./ntap-automation/ntaplod_init/sl10599_init.sh
   ```

4. Execute scripts from subfolders depending on type of solution, method and task, e.g.: ontap9 --> python --> create SVM
   ```
   ./ntap-automation/ontap9/ansible/21_create_pri_svm.yml
   ./ntap-automation/ontap9/curl/02_get_svm_details.curl
   ./ntap-automation/ontap9/python/90_delete_all.py
   ```
