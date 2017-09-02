import os
import errno
import socket
import sys
import time
import select
import paramiko

path=r"/home/u1069621/python/input"
output="/home/u1069621/python/output"
i = 1
with open(path, 'r') as f:
        for host in f:
                HOSTN = host.rstrip()

                try:
                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh.connect(host,username='', password='')
                        print "Connected to %s" % host
                        # Send the command (non-blocking)
                        command="run /util bash -c '\''for c in `ls --format single-column /config/filestore/files_d/Common_d/certificate_d/`; do     arr=($(openssl x509 -noout -text -in /config/filestore/files_d/Common_d/certificate_d/${c} |grep -E '\"'sha1'\"'));      if [ -n '\"'${arr[2]}'\"' ];     then         echo ${c};     fi;  done'\''"

                        stdin, stdout, stderr = ssh.exec_command(command)

                        # Wait for the command to terminate
                        while not stdout.channel.exit_status_ready():
                        # Only print data if there is data to read in the channel
                                if stdout.channel.recv_ready():
                                        rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                                        if len(rl) > 0:
                                                # Print data from stdout
                                                print stdout.channel.recv(1024),
                                                a = stdout.channel.recv(1024),
                                                f = open(HOSTN+".txt", 'a')
                                                f.write(str(a)+ "\n")
                        #
                        # Disconnect from the host
                        #
                        print "Command done, closing SSH connection"
                        ssh.close()
                except paramiko.AuthenticationException:
                        print "Authentication failed when connecting to %s" % host
                        sys.exit(1)
                except:
                        print "Could not SSH to %s, waiting for it to start" % host
                        i += 1
                        time.sleep(2)
                        # If we could not connect within time limit
                        if i == 30:
                        print "Could not connect to %s. Giving up" % host
                        sys.exit(1)
