# NetApp Automation Demos

Welcome to my collection of automation demos. In this repository you will find various examples on how to automate administrative and operational tasks on NetApp solutions.

## Quick Start
If you are a customer, partner or NetApp employee:

1. Please use the virtual hands-on lab:
   https://handsonlabs.netapp.com/lab/ontapapi

2. Log into the first Linux machine (rhel1) and clone this repository
   ```
   git clone https://github.com/AdrianBronder/ntap-automation.git
   ```

3. Initialize the environment by running the lab init script:
   ```
   ./ntap-automation/ntaplod_init/sl10599_init.sh
   ```

4. Execute scripts from subfolders depending on type of solution, method and task, e.g.: ontap9 --> python --> create SVM
