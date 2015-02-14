import subprocess as sub

p = sub.Popen(('sudo', 'tcpdump', '-l'), stdout=sub.PIPE)
try:
    for row in p.stdout:
        print(row.rstrip())   # process here
except KeyboardInterrupt:
    p.terminate()