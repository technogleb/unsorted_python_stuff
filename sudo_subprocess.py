"""A convenient pipeline for granting sudo access to subprocess commands"""

import subprocess
import getpass

# asking for a password only once
passw = getpass.getpass()

"""example commands, requiring sudo"""
p1 = subprocess.Popen('sudo -S ls'.split(), stdin=subprocess.PIPE)
p2 = subprocess.Popen('sudo -S cat /etc/resolv.conf'.split(), stdin=subprocess.PIPE)

for p in [p1, p2]:
    p.communicate(passw.encode())
