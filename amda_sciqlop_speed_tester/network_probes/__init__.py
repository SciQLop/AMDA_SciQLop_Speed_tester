import subprocess


def trace_route(address: str, ttl=30):
    def extract_ip(line: str):
        line = line.strip().replace('  ', ' ').split()
        if len(line) > 1:
            return line[1]
        return None

    route = subprocess.run(['traceroute', f'-m{ttl}', address], stdout=subprocess.PIPE).stdout.decode().split(
        '\n')[1:]
    route = [extract_ip(line) for line in route]
    return [ip for ip in route if ip is not None]

