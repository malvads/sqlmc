
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


class Banner:
    def __init__(self):
        self.banner = r"""
 _______ _______ ___
|   _   |   _   |   |  .--------.----.
|   1___|.  |   |.  |  |        |  __|
|____   |.  |   |.  |__|__|__|__|____|
|:  1   |:  1   |:  1   |
|::.. . |::..   |::.. . |
`-------`----|:.`-------'
             `--'
    """
        self.title = "SQL Injection Massive Checker"
        self.author = "Author: Miguel Álvarez"
        self.license = "License: AGPL-3.0"
        self.version = "Version: "
        self.read_version_from_file()

    def read_version_from_file(self):
        with open("VERSION", "r") as version_file:
            self.version += version_file.read()
    
    def print_banner(self):
        print(self.banner)
        print(self.title)
        banner = " | ".join([self.author, self.license, self.version])
        print(banner)