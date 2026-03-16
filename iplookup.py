#!/usr/bin/env python3
"""iplookup - IP geolocation and info lookup."""
import urllib.request, json, argparse, sys, socket

def lookup(ip=None):
    url = f"http://ip-api.com/json/{ip}" if ip else "http://ip-api.com/json/"
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            return json.loads(r.read())
    except Exception as e:
        return {'error': str(e)}

def reverse_dns(ip):
    try: return socket.gethostbyaddr(ip)[0]
    except: return None

def main():
    p = argparse.ArgumentParser(description='IP geolocation lookup')
    p.add_argument('ip', nargs='*', help='IP address(es) to look up (default: your IP)')
    p.add_argument('-j', '--json', action='store_true', help='JSON output')
    p.add_argument('-r', '--rdns', action='store_true', help='Include reverse DNS')
    args = p.parse_args()

    ips = args.ip or [None]
    for ip in ips:
        data = lookup(ip)
        if args.json:
            print(json.dumps(data, indent=2))
        elif data.get('status') == 'success':
            print(f"IP:       {data.get('query', 'N/A')}")
            print(f"Location: {data.get('city')}, {data.get('regionName')}, {data.get('country')}")
            print(f"Coords:   {data.get('lat')}, {data.get('lon')}")
            print(f"ISP:      {data.get('isp')}")
            print(f"Org:      {data.get('org')}")
            print(f"AS:       {data.get('as')}")
            print(f"Timezone: {data.get('timezone')}")
            if args.rdns:
                rdns = reverse_dns(data['query'])
                print(f"rDNS:     {rdns or '(none)'}")
            if len(ips) > 1: print()
        else:
            print(f"Error: {data.get('message', data.get('error', 'unknown'))}")

if __name__ == '__main__':
    main()
