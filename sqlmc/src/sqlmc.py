from lib.scanner import Scanner
from lib.error import Checker
from lib.http import HTTP
from lib.parser import Parser
from lib.arg import ArgParser
from lib.logger import Logger
from colorama import Fore, Style

class SQLMC(Logger):
    DEF_INI_DEPTH = 0
    DEF_INI_DEPTH_INCR = 1
    LOGGER_NAME = "sqlmc"

    def __init__(self):
        super().__init__(self.LOGGER_NAME)
        self.args = ArgParser.parse_arguments()
        self.domain = self.args.url
        self.scanner = Scanner(self.domain)
        self.error_checker = Checker()
        self.http = HTTP()
        self.parser = Parser()
        self.server = self.http.get_server(self.domain)
        self.errors = []

    def scan(self):
        self.logger.info(f"{Fore.GREEN}Scanning {self.domain}...{Style.RESET_ALL}")
        self.scan_links(self.domain, self.DEF_INI_DEPTH)
        self.test_for_get_sqli()
        self.test_for_post_sqli()

    def scan_links(self, url, depth):

        if depth > int(self.args.depth):
            return
        
        html = self.http.get(url)

        self.scanner.feed(html)
        links = self.scanner.get_links()

        for link in links:
            self.scan_links(link, depth + self.DEF_INI_DEPTH_INCR)
        
    def test_for_get_sqli(self):
        self.logger.info(f"{Fore.YELLOW}Will now test for GET SQL Injection of all links..{Style.RESET_ALL}")
        for link in self.scanner.get_links():
            self.test_url_for_sqli(link, self.parser.inject_all_get_params)

    def test_for_post_sqli(self):
        self.logger.info(f"{Fore.YELLOW}Will now test for POST SQL Injection of all forms..{Style.RESET_ALL}")
        for form in self.scanner.get_forms():
            self.test_form_for_sqli(form)

    def test_url_for_sqli(self, url, inject_params_func):
        for injected_url in inject_params_func(url):
            self.logger.info(f"{Fore.CYAN}Testing {injected_url}...{Style.RESET_ALL}")
            response = self.http.get(injected_url)
            self.process_sqli_result(response, injected_url)

    def test_form_for_sqli(self, form):
        self.logger.info(f"{Fore.CYAN}Testing {form.url}...{Style.RESET_ALL}")
        for injected_form in self.parser.inject_all_post_params(form):
            self.logger.debug(f"{Fore.CYAN}Testing {injected_form.url}...{Style.RESET_ALL}")
            response = self.http.post(injected_form.url, injected_form.data)
            self.process_sqli_result(response, injected_form.url, form=injected_form.data)

    def process_sqli_result(self, response, url, form=None):
        scan_result = self.error_checker.check(response)
        if scan_result.error:
            if form == None:
                affected_param = self.parser.get_affected_param(url)
                self.logger.info(f"{Fore.GREEN}GET SQL Injection found in {url}, the affected parameter is [{Style.RESET_ALL}{Fore.YELLOW}{affected_param}{Style.RESET_ALL}{Fore.GREEN}]{Style.RESET_ALL}")
            else:
                self.logger.info(f"{Fore.GREEN}POST SQL Injection found in {url}, with form data [{Style.RESET_ALL}{Fore.YELLOW}{form}{Style.RESET_ALL}{Fore.GREEN}]{Style.RESET_ALL}")
            self.errors.append(scan_result)
