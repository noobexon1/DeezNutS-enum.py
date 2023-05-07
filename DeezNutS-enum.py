#!/usr/bin/env python3

from dns import *
import argparse

def asynchronous_full_zone_transfer(name_server, domain_name):
    try:
        axfr = zone.from_xfr(query.xfr(name_server, domain_name))
        if axfr:
            print('[*] Successful Zone Transfer from {}'.format(name_server))
            for record in axfr:
                subdomains.append('{}.{}'.format(record.to_text(), domain_name))

    except Exception as error:
        print(error)
        pass


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog="DeezNutS-enum.py", epilog="DNS Zone Transfer Script",
                                     usage="DeezNutS-enum.py [options] -d <DOMAIN>", prefix_chars='-', add_help=True)

    parser.add_argument('-d', action='store', metavar='Domain', type=str,
                        help='Target Domain.\tExample: inlanefreight.htb', required=True)
    parser.add_argument('-n', action='store', metavar='Nameserver', type=str,
                        help='Nameservers separated by a comma.\tExample: ns1.inlanefreight.htb,ns2.inlanefreight.htb')
    parser.add_argument('-v', action='version', version='DNS-AXFR - v1.0', help='Prints the version of DeezNutS-enum.py')

    args = parser.parse_args()

    domain = args.d
    subdomains = []
    nameservers = list(args.n.split(","))

    # Check if URL is given
    if not args.d:
        print('[!] You must specify target Domain.\n')
        print(parser.print_help())
        exit()

    if not args.n:
        print('[!] You must specify target nameservers.\n')
        print(parser.print_help())
        exit()

    for nameserver in nameservers:
        asynchronous_full_zone_transfer(nameserver, domain)

    if subdomains is not None:
        print('-------- Found Subdomains:')
        for subdomain in subdomains:
            print('{}'.format(subdomain))

    else:
        print('No subdomains found.')
        exit()
