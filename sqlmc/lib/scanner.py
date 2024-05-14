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

from html.parser import HTMLParser

class Scanner(HTMLParser):
    def __init__(self, url):
        super().__init__()
        self.links = []
        self.forms = []
        self.url = url

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    href = value
                    if not href.startswith(('http', '/')):
                        href = self.url + href
                    if href not in self.links:
                        self.links.append(href)

        elif tag == 'form':
            for name, value in attrs:
                if name == 'action':
                    self.forms.append(value)

    def get_links(self):
        return self.links

    def get_forms(self):
        return self.forms
