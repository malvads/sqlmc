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

import requests

class HTTP:
    @staticmethod
    def get(url):
        req = requests.get(url)
        res = req.text
        return res

    @staticmethod
    def post(url, data):
        req = requests.post(url, data)
        res = req.text
        return res

    @staticmethod
    def get_server(url):
        req = requests.get(url)
        server = req.headers.get('Server')
        return server
    