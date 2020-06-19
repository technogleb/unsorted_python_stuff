"""
Safari on macos often generates many unused processes (mostly serving webcontent), even
when it's closed. They consume some memory.
That scripts is intended to find and kill those.
"""

import subprocess
from space_stripper import replace_spaces

ps_aux = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
safari_proceses = subprocess.check_output(['grep', 'Safari'], stdin=ps_aux.stdout)
ps_aux.wait()


for line in safari_proceses.decode('utf8').split('\n')[:-1]:
    line_cleaned = replace_spaces(line, '\t')
    safari_pid = line_cleaned.split('\t')[1]
    subprocess.call(['kill', '-9', safari_pid])
