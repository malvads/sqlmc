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

from src.sqlmc import SQLMC
from src.banner import Banner

if __name__ == "__main__":
    banner = Banner()
    banner.print_banner()
    sqlmc = SQLMC()
    sqlmc.scan()



