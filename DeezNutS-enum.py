#!/usr/bin/env python3

import argparse

import dns.resolver
import dns.zone
import dns.query

record_types = ['A', 'AAAA', 'CNAME', 'HINFO', 'ISDN', 'MX', 'NS', 'PTR', 'SOA', 'TXT']


def dns_records_lookup(domain_name):
    print(f"[!] Trying to enumerate DNS records for domain: {domain_name}\n")
    for record_type in record_types:
        try:
            records = dns.resolver.resolve(domain_name, record_type)
            print(f"{record_type} records:")
            print("-"*20)
            for record in records:
                print(record.to_text())
            print()  # Add an empty line for better readability
        except dns.resolver.NoAnswer:
            print(f"No {record_type} records found.\n")
        except dns.exception.DNSException as error:
            print(f"DNS query for {record_type} records failed: {error}\n")


def asynchronous_full_zone_transfer(name_server, domain_name):
    try:
        zone_file = dns.zone.from_xfr(dns.query.xfr(name_server, domain_name))
        if zone_file:
            print('[*] Successful Zone Transfer from {}'.format(name_server))
            for record in zone_file:
                subdomains.append('{}.{}'.format(record.to_text(), domain_name))

    except dns.exception.DNSException as error:
        print(f"DNS zone transfer failed: {error}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog="DeezNutS-enum.py",
                                     epilog="DNS Zone Transfer Script",
                                     usage="DeezNutS-enum.py [options] -d <DOMAIN>",
                                     prefix_chars='-',
                                     add_help=True)

    parser.add_argument('--version',
                        action='version',
                        version='DeezNutS-enum - v1.0',
                        help='Prints the current version of the DeezNutS-enum.py tool')

    parser.add_argument('-d',
                        action='store',
                        metavar='Domain',
                        type=str,
                        help='Target Domain.\tExample: something.com',
                        required=True)

    parser.add_argument('-n',
                        action='store',
                        metavar='Nameservers',
                        type=str,
                        help='Nameservers separated by a comma.\tExample: ns1.something.com,ns2.something.com')

    args = parser.parse_args()

    domain = args.d
    subdomains = []
    nameservers = list(args.n.split(","))

    if not args.d:
        print('[!] You must specify a target Domain.\n')
        print(parser.print_help())
        exit()

    dns_records_lookup(domain)

    for nameserver in nameservers:
        asynchronous_full_zone_transfer(nameserver, domain)

    if subdomains is not None:
        print('-------- Found Subdomains:')
        for subdomain in subdomains:
            print('{}'.format(subdomain))

    else:
        print('No subdomains found.')
        exit()
