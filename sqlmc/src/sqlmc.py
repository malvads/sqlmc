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

class SQLMC:
    DEF_INI_DEPTH = 0
    DEF_INI_DEPTH_INCR = 1

    def __init__(self):
        self.args = ArgParser.parse_arguments()
        self.domain = self.args.url
        self.scanner = Scanner(self.domain)
        self.error_checker = Checker()
        self.http = HTTP()
        self.parser = Parser()
        self.server = self.http.get_server(self.domain)
        self.errors = []

    def scan(self):
        self.scan_links(self.domain, self.DEF_INI_DEPTH)

    def scan_links(self, url, depth):
        if depth > int(self.args.depth):
            self.test_for_get_sqli()
            return
        html = self.http.get(url)

        self.scanner.feed(html)
        links = self.scanner.get_links()
        forms = self.scanner.get_forms()

        for link in links:
            self.scan_links(link, depth + self.DEF_INI_DEPTH_INCR)
        for form in forms:
            self.scan_forms(form)
        
    def test_for_get_sqli(self):
        for link in self.scanner.get_links():
            urls = self.parser.inject_all_get_params(link)
            for url in urls:
                response = self.http.get(url)
                scan_result = self.error_checker.check(response)

                if scan_result.error:
                    print(scan_result)
                    self.errors.append(scan_result)
