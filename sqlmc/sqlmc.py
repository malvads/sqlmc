import os
import sqlmc.lib.scanner as scanner
import tabulate
import argparse as ap
import pyfiglet

def print_banner():
    ascii_banner = pyfiglet.figlet_format("SQLMC")
    print(ascii_banner)

def read_version():
    version_file = os.path.join(os.path.dirname(__file__), 'VERSION')
    with open(version_file, 'r') as f:
        version = f.read().strip()
    return version

def save_output(output_file, urls):
    with open(output_file, 'w') as f:
        for url in urls:
            f.write(f"{url['url']}\n")
            f.write(f"Server: {url['server']}\n")
            f.write(f"Depth: {url['depth']}\n")
            f.write(f"Vulnerable: {url['vulnerable']}\n")
            f.write(f"DB Server: {url['db server']}\n")
            f.write("\n")
    
def main():
    print_banner()
    version = read_version()
    print(f"Version: {version}")
    print(f"Author: Miguel Álvarez")

    parser = ap.ArgumentParser(description="A simple SQLi Massive Checker & Scanner")
    parser.add_argument("-u", "--url", help="The URL to scan", required=True)
    parser.add_argument("-d", "--depth", help="The depth to scan", required=True)
    parser.add_argument("-o", "--output", help="The output file")
    args = parser.parse_args()
    url = args.url
    depth = int(args.depth)
    print(f"Scanning {url} with depth {depth}")
    sqlscanner = scanner.Scanner(url, depth)
    print(tabulate.tabulate(sqlscanner.get_urls(), headers="keys", tablefmt="grid"))
    print(f"Scanned {len(sqlscanner.get_urls())} URLs")
    if args.output:
        save_output(args.output, sqlscanner.get_urls())
        print(f"Output saved to {args.output}")

if __name__ == "__main__":
    main()
