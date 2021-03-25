# SSH Tunnel
LabOnDemand or HandsOnLabs are neat ways to test out certain functionalities related to NetApp products.

However, for several reasons the RDP session in the browser might become uncomfortable for specific tasks - e.g. if your local host is a Mac and you're struggling with entering special characters in the remote Windows.

If you're going to use the linux terminal in the lab - which is mandatory for the demos described in this repo - it might become handy to setup a SSH tunnel from your local host to the remote lab.

The following setup has been succesfully tested with a Mac as local host. It is expected that a Linux host works the same way, however, Windows might be a different story...

## Prerequisites
As there is no way to access the lab from the outside (beside the browser RDP session), we have to establish a SSH connection from inside the lab to a remote SSH server. Most likely, your local host is not accessible from the lab directly - even if you have a SSH server running.

Therefore we need a **SSH proxy** (let's call it *sshproxy*) which is reachable in the public internet and can be accessed by the lab via SSH as well as the local machine.

For this setup a free tier compute instance running Ubuntu 18.04 provided by [Oracle Cloud Free Tier](https://www.oracle.com/de/cloud/free/) is being used. Beside the obligatory SSH server, please make sure that you have installed ```nc``` resp. ```netcat```. 

Of course, any other Linux server should work as well.

## Establishing a SSH connection from lab to SSH proxy
Open the lab in the browser RDP session and open a connection to *rhel1* with putty (see lab guide for details). In order to make the lab known to the SSH proxy we first have to get the public SSH key from *rhel1*:
```
$ cat /root/.ssh/id_rsa.pub
```
Copy the output to the clipboard and open a ssh session from your local machine to *sshproxy*. Open file
```
~/.ssh/authorized_keys
```
and append a line with the content from the clipboard. 

Go back to the lab and *rhel1* terminal and try to login to *sshproxy* without password.
If this is working, please exit and run the following command to establish a persistent connection:
```
ssh -o ExitOnForwardFailure=yes -o ConnectTimeout=3 -o TCPKeepAlive=yes -o ServerAliveInterval=5 -o ServerAliveCountMax=5 -N -R 2242:localhost:22 ubuntu@sshproxy
```
Please make sure that you're using the correct username and hostname of the SSH proxy.

**Note:** Do not close the terminal window as long as you're planning to access *rhel1* from your local machine.

## SSH connection from localhost to lab via SSH proxy
In order to check whether the reverse tunnel from the previous step is established, you can login to *sshproxy* and run
```
netstat -anp | grep "2242.*LISTEN"
```
Now, that we have a connection listening on port 2242 on the *sshproxy* with the lab as an endpoint, we only have to establish another SSH connection from localhost to the *sshproxy* and "link" them both together.

Therefore, add to your local ```~/.ssh/config``` (create if not existing) the following lines:
```
Host lod
  User root
  ProxyCommand ssh -e none ubuntu@sshproxy exec nc localhost 2242
```
Again, please make sure to modify username and password of the *sshproxy*. This command establishes a connection on the *sshproxy* to localhost on port 2242 - which is actually the SSH server on *rhel1*. The *root* user is the user to login to *rhel1*.

Now, you can simply call
```
ssh lod
```
and you're prompted for the password of the *rhel1* in the lab, which you can find in the lab guide. 