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
from lib.structs.sql import Form

class Scanner(HTMLParser):
    def __init__(self, url):
        super().__init__()
        self.links = []
        self.forms = []
        self.url = url
        self.current_form = None

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    href = value
                    if not href.startswith(('http', '/')):
                        href = self.url + href
                    if href not in self.links:
                        self.links.append(href)
        if tag == 'form':
            action = None
            for name, value in attrs:
                if name == 'action':
                    action = value
                    if not action.startswith(('http', '/')):
                        action = self.url + action
                    break 

            if action:
                self.current_form = Form(url=action, inputs=[])
                if action not in self.forms:
                    self.forms.append(self.current_form)

        elif tag == 'input' and self.current_form:
            input_attrs = dict(attrs)
            if 'name' in input_attrs:
                self.current_form.inputs.append(input_attrs['name'])
        
    def get_links(self):
        return self.links

    def get_forms(self):
        return self.forms