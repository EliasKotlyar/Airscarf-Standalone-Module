rshell rsync -m static /pyboard/static
rshell rsync lib /pyboard/lib
rshell cp main.py /pyboard/main.py
rshell cp static/index.html /pyboard/static/index.html
rshell repl "~ machine.reset()~"



rshell rsync /pyboard/lib lib
rshell cp /pyboard/main.py main.py