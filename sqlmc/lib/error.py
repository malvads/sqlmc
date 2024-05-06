# Original code https://github.com/the-robot/sqliv/blob/master/src/sqlerrors.py
# Thanks to Ekultek (https://github.com/Ekultek) & the-robot (https://github.com/the-robot/)

import re

class Checker:
    def __init__(self):
        pass

    def errors(self):
         return {
            "MySQL": (r"SQL syntax.*MySQL", r"Warning.*mysql_.*", r"MySQL Query fail.*", r"SQL syntax.*MariaDB server"),
            "PostgreSQL": (r"PostgreSQL.*ERROR", r"Warning.*\Wpg_.*", r"Warning.*PostgreSQL"),
            "Microsoft SQL Server": (r"OLE DB.* SQL Server", r"(\W|\A)SQL Server.*Driver", r"Warning.*odbc_.*", r"Warning.*mssql_", r"Msg \d+, Level \d+, State \d+", r"Unclosed quotation mark after the character string", r"Microsoft OLE DB Provider for ODBC Drivers"),
            "Microsoft Access": (r"Microsoft Access Driver", r"Access Database Engine", r"Microsoft JET Database Engine", r".*Syntax error.*query expression"),
            "Oracle": (r"\bORA-[0-9][0-9][0-9][0-9]", r"Oracle error", r"Warning.*oci_.*", "Microsoft OLE DB Provider for Oracle"),
            "IBM DB2": (r"CLI Driver.*DB2", r"DB2 SQL error"),
            "SQLite": (r"SQLite/JDBCDriver", r"System.Data.SQLite.SQLiteException"),
            "Informix": (r"Warning.*ibase_.*", r"com.informix.jdbc"),
            "Sybase": (r"Warning.*sybase.*", r"Sybase message")
        }
    def check(self, html):
        """check SQL error is in HTML or not"""
        for db, errors in self.errors().items():
            for error in errors:
                if re.compile(error).search(html):
                    return True, db
        return False, None