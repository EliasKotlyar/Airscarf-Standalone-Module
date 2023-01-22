rshell rsync static /pyboard/static
rshell rsync lib /pyboard/lib
rshell cp main.py /pyboard/main.py
rshell repl "~ machine.reset()~"
