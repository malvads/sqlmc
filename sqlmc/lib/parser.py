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

from lib.structs.sql import FormSumbit
import re

class Parser:
    @staticmethod
    def inject_all_get_params(url):
        try:
            urls = []
            base_url, query_string = url.split('?', 1)
            params = query_string.split('&')
            for param in params:
                key, value = param.split('=')
                modified_value = f"{value}%27"
                modified_param = f"{key}={modified_value}"
                modified_query_string = "&".join(
                    modified_param if p == param else p for p in params
                )
                modified_url = f"{base_url}?{modified_query_string}"
                urls.append(modified_url)
            return urls
        except ValueError:
            return []
    
    @staticmethod
    def inject_all_post_params(form):
        try:
            urls = []
            url = form.url
            inputs = form.inputs
            for input in inputs:
                data = {}
                for i in inputs:
                    if i == input:
                        data[i] = "%27"
                    else:
                        data[i] = ""
                form_data = "&".join([f"{k}={v}" for k, v in data.items()])
                new_form = FormSumbit(url=url, data=form_data)
                urls.append(new_form)
            return urls
        except ValueError:
            return []
    
    @staticmethod
    def get_inputs(html):
        inputs = []
        for line in html.split('\n'):
            if 'input' in line:
                inputs.append(line)
        return inputs
    
    @staticmethod
    def get_affected_param(url):
        regex = r'[?&]([^=]+)=([^&%]+)%27'
        match = re.search(regex, url)
        return match.group(1)