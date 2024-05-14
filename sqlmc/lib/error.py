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

import re
from lib.structs.sql import SqlInjectionReport

class Checker:
    def __init__(self):
        self.error_patterns = {
            "MySQL": [
                r"SQL syntax.*MySQL",
                r"Warning.*mysql_.*",
                r"MySQL Query fail.*",
                r"SQL syntax.*MariaDB server"
            ],
            "PostgreSQL": [
                r"PostgreSQL.*ERROR",
                r"Warning.*\Wpg_.*",
                r"Warning.*PostgreSQL"
            ],
            "Microsoft SQL Server": [
                r"OLE DB.* SQL Server",
                r"(\W|\A)SQL Server.*Driver",
                r"Warning.*odbc_.*",
                r"Warning.*mssql_",
                r"Msg \d+, Level \d+, State \d+",
                r"Unclosed quotation mark after the character string",
                r"Microsoft OLE DB Provider for ODBC Drivers"
            ],
            "Microsoft Access": [
                r"Microsoft Access Driver",
                r"Access Database Engine",
                r"Microsoft JET Database Engine",
                r".*Syntax error.*query expression"
            ],
            "Oracle": [
                r"\bORA-[0-9][0-9][0-9][0-9]",
                r"Oracle error",
                r"Warning.*oci_.*",
                "Microsoft OLE DB Provider for Oracle"
            ],
            "IBM DB2": [
                r"CLI Driver.*DB2",
                r"DB2 SQL error"
            ],
            "SQLite": [
                r"SQLite/JDBCDriver",
                r"System.Data.SQLite.SQLiteException"
            ],
            "Informix": [
                r"Warning.*ibase_.*",
                r"com.informix.jdbc"
            ],
            "Sybase": [
                r"Warning.*sybase.*",
                r"Sybase message"
            ]
        }

    def check(self, html):
        """Check SQL error in HTML"""

        result = SqlInjectionReport(error=False, db=None)
        for db, patterns in self.error_patterns.items():
            for pattern in patterns:
                if re.search(pattern, html):
                    result.error = True
                    result.db = db
        return result
