# pythonIperf3

This project has two script files: iperf3.py and iscsiAdm.py

written for python3(3.6.8)


iperf3.py is a quick bandwidth test between a server and n number of clients as defined on the commandline. 
iperf3.py will first start an iperf3 server on the "server" system. 
Next, iperf3.py will use the "client" systems to drive traffic to the "server" system.
Finally, iperf3.py will kill the iperf3 server on the "server" system.

To use, the server and the clients must have iperf3 installed. The firewall on the server system must be disabled 
or the port # the iperf3 server uses must be opened in the firewall.

Sample commandline/screen output:

niverson@Gengar:~/pythonProjects$ ./iperf3.py 192.168.86.30 192.168.86.34

2019-08-26 12:49:31,418 -                      root - CRITICAL - logs saved at: /tmp/iperf3_2019_08_26__18_49_31.log

2019-08-26 12:49:31,418 -  modules.iperfClientClass -     INFO - iperf3 for 192.168.86.34 uses logfile /tmp/iperf3_192.168.86.34__2019_08_26__18_49_31.dat
...

2019-08-26 12:49:46,456 -     modules.hostBaseClass -     INFO - iperf3 stopped on 192.168.86.30


_________________________________________________________________________________________________________________


iscsiAdm.py is a simple connectivity test that uses iscsiadm on the iscsiAdmHost to discover the iscsi target, 
log into the iscsi target, then logout of the iscsi target. 

To use, the target must already be setup and configured to let the iscsiAdmHost login.

Sample commandline/screen output:

niverson@Gengar:~/pythonProjects$ ./iscsiAdm.py -port 3261 192.168.86.30 192.168.86.34

2019-08-26 13:36:04,452 -                      root - CRITICAL - logs saved at: /tmp/iscsiadm_2019_08_26__19_36_04.log

2019-08-26 13:36:04,453 -     modules.iscsiadmClass -     INFO - iscsiAdm discovering 192.168.86.30:3261
...

2019-08-26 13:36:05,392 -     modules.iscsiadmClass -     INFO - logged out iqn.2003-01.org.linux-iscsi.target.x8664:sn.89a9bf5ddf8d at 192.168.86.30:3261

