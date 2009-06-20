import termios
import tty
import sys

stdin_fd = None
old_mask = None

def eat_keys():
    global stdin_fd, old_mask
    stdin_fd = sys.stdin.fileno()
    old_mask = termios.tcgetattr(stdin_fd)     # a copy to save
    new = old_mask[:]
    new[3] = new[3] & ~termios.ECHO # 3 == 'lflags'
    termios.tcsetattr(stdin_fd, termios.TCSADRAIN, new)
    tty.setraw(stdin_fd)
    while 1:
        yield sys.stdin.read(1)

def restore_keys():
    termios.tcsetattr(stdin_fd, termios.TCSADRAIN, old_mask)

def write(s):
    s = s.replace('\n', '\n\r')
    sys.stdout.write(s)
    sys.stdout.flush()

SCRIPT = """\
Python 2.4.2 (#2, Mar  5 2006, 00:03:25) 
[GCC 4.0.3 20060212 (prerelease) (Ubuntu 4.0.2-9ubuntu1)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> print 'hello world'
hello world
>>> what is up?
File "<stdin>", line 1
    what is up?
              ^
SyntaxError: invalid syntax
>>> quit
'Use Ctrl-D (i.e. EOF) to exit.'
>>> raise SystemExit
"""

def chunk_script(s):
    parts = ['', '']
    while s:
        c = s[0]
        s = s[1:]
        if c == '\r':
            continue
        if c == '\x0c':
            parts.append('')
        else:
            parts[-1] += c
    while parts and parts[-1] == '':
        parts = parts[:-1]
    return parts

if __name__ == '__main__':
    if sys.argv[1:]:
        content = open(sys.argv[1], 'rb').read()
    else:
        content = SCRIPT
    script = chunk_script(content)
    try:
        keys = eat_keys()
        for c in keys:
            if c == '\x03': # ^C
                break
            if not script:
                break
            if not script[0]:
                # Time to do a literal chunk
                script = script[1:]
                while c != '\r':
                    c = keys.next()
                if script:
                    write(script[0])
                script = script[1:]
                continue
            write(script[0][0])
            script[0] = script[0][1:]
    finally:
        restore_keys()
        
            
