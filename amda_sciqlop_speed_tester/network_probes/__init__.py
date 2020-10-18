import subprocess
import platform


def trace_route(address: str):
    if platform.system() == 'Windows':
        route = subprocess.run(['tracert', address], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE).stdout.decode('cp850')
    else:
        route = subprocess.run(['traceroute', '-w1', '-m15', address], stdout=subprocess.PIPE).stdout.decode()
    return route
