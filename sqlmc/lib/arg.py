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

import argparse

class ArgParser:
    
    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(description="SQLMC - SQL Injection Massive Checker")
        parser.add_argument("-u", "--url", help="URL to scan.", required=True)
        parser.add_argument("-o", "--output", help="Output file.")
        parser.add_argument("-d", "--depth", help="Depth of the scan.", required=True)
        return parser.parse_args()