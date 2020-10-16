import subprocess
import platform


def trace_route(address: str):
    if platform.system() == 'Windows':
        route = subprocess.run(['tracert', address], stdout=subprocess.PIPE).stdout.decode('cp850')
    else:
        route = subprocess.run(['traceroute', address], stdout=subprocess.PIPE).stdout.decode()
    return route

