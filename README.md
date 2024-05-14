# SQLMC - SQL Injection Massive Checker

## Demo
![Alt Text](./assets/demo.gif)


## Overview
SQLMC (SQL Injection Massive Checker) is a tool designed to scan a domain for SQL injection vulnerabilities. It crawls the given URL up to a specified depth, checks each link for SQL injection vulnerabilities, and reports its findings.

## Features
- Scans a domain for GET SQL injection vulnerabilities on multiple GET params
- Scana a domain for POST SQL Injections vulnerabilities on multiple POST params
- Crawls the given URL up to a specified depth
- Reports vulnerabilities along with server information and depth

## Installation
1. Install the required dependencies:
    ```bash
    pip3 install sqlmc
    ```

## Usage

Run `sqlmc` with the following command-line arguments:

- `-u, --url`: The URL to scan (required)
- `-d, --depth`: The depth to scan (required)
- `-o, --output`: The output file to save the results

Example usage:

```bash
sqlmc -u http://example.com -d 2
```

Replace http://example.com with the URL you want to scan and 3 with the desired depth of the scan. You can also specify an output file using the -o or --output flag followed by the desired filename.

The tool will then perform the scan and display the results.

## ToDo
- Add Proxy Support
- Add Support for silence mode
- Add Tor Support
- Better injection checker trigger methods

## Credits

- Developed by [Miguel Álvarez](https://github.com/malvads)

## License

This project is licensed under the [GNU Affero General Public License v3.0](LICENSE).


