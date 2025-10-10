import sys
import os

if os.name == 'nt':
    import msvcrt
    def get_key():
        while True:
            key = msvcrt.getch()
            if key in [b'w', b'a', b's', b'd']:
                return key.decode()
else:
    import tty
    import termios
    def get_key():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                key = sys.stdin.read(1)
                if key in ['w', 'a', 's', 'd']:
                    return key
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
