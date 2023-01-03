import os

def ping(hostname):
    hostname = hostname
    response = os.system('ping -c 5 ' + hostname)

    return 'up' if response == 0 else 'down'