import os, signal
ProcessName = 'run_dashboards.py'
p = os.popen("ps ax | grep " + ProcessName + " | grep -v grep")
for line in p:
    fields = line.split()
    pid = fields[0]
    print('Terminating the ' + ProcessName + ' process with pid:', pid)
    os.kill(int(pid), signal.SIGINT) #  SIGINT - interupt process stream, ctrl-C