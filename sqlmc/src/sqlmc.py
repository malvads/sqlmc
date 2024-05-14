###################################################################
# This file is licensed under the Affero General Public License   #
#                  Version 3 (AGPLv3)                             #
#                                                                 #
# You should have received a copy of the GNU Affero General       #
# Public License along with this program. If not, see             #
# <https://www.gnu.org/licenses/agpl-3.0.html>.                   #
#                                                                 #
# Author: thegexi@gmail.com                                       #
###################################################################

from lib.scanner import Scanner
from lib.error import Checker
from lib.http import HTTP
from lib.parser import Parser
from lib.arg import ArgParser
from lib.logger import Logger

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
        self.logger.info(f"Scanning {self.domain}...")
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
        self.logger.info("Will now test for GET SQL Injection of all links..")
        for link in self.scanner.get_links():
            urls = self.parser.inject_all_get_params(link)
            for url in urls:
                self.logger.info(f"Testing {url}...")
                response = self.http.get(url)
                scan_result = self.error_checker.check(response)
                self.logger.debug(f"Scan result: {scan_result}")
                if scan_result.error:
                    affected_param = self.parser.get_affected_param(url)
                    self.logger.info(f"GET SQL Injection found in {url} the parameter affected is [{affected_param}]")
                    self.errors.append(scan_result)
    
    def test_for_post_sqli(self):
        self.logger.info("Will now test for POST SQL Injection of all forms..")
        forms = self.scanner.get_forms()
        for form in forms:
            self.logger.info(f"Testing {form.url}...")
            urls = self.parser.inject_all_post_params(form)
            for _form in urls:
                self.logger.debug(f"Testing {_form.url}...")
                response = self.http.post(_form.url, _form.data)
                scan_result = self.error_checker.check(response)
                if scan_result.error:
                    self.logger.info(f"POST SQL Injection found in {_form.url} the post data is [{_form.data}]")
                    self.errors.append(scan_result)
