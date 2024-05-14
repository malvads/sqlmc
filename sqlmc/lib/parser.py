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
    def inject_all_post_params(url, data):
        urls = []
        for key, value in data.items():
            modified_value = f"{value}%27"
            modified_data = {k: v for k, v in data.items()}
            modified_data[key] = modified_value
            urls.append((url, modified_data))
        return urls