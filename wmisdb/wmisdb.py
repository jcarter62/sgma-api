import pyodbc
from decouple import config


class WMISDB:
    _server = ''
    _instance = ''
    _database = ''
    _username = ''
    _password = ''
    connection = None

    def __init__(self) -> None:
        self._server = config('SERVER', default='localhost')
        self._instance = config('INSTANCE', default='')
        self._database = config('DATABASE', default='database')
        self._username = config('UID', default='username')
        self._password = config('PASSWORD', default='password')

        self.connection = self._connection_()
        super().__init__()

    def _conn_str_(self, ):
        con_str = 'Driver={ODBC Driver 17 for SQL Server};'

        con_str += 'SERVER=' + self._server
        if self._instance != '':
            con_str += '\\' + self._instance
        con_str += ';'

        con_str += 'DATABASE=' + self._database + ';'
        con_str += 'UID=' + self._username + ';'
        con_str += 'PWD=' + self._password + ';'
        con_str += 'PORT=1433;ENCRYPT=NO;'
        return con_str

    def _connection_(self):
        if self.connection is None:
            self.connection = pyodbc.connect(self._conn_str_())
        return self.connection

    def account_name(self, account):
        result = ''
        conn = pyodbc.connect(self._conn_str_())
        cursor = conn.cursor()
        cmd = f'select fullname from name where name_id = {account};'
        try:
            for row in cursor.execute(cmd):
                result = row[0]
        except Exception as e:
            print(str(e))
        conn.close()
        return result

    def account_water_types(self, account):
        cmd = f'sp_wmis_api_account_watertypes @account={account};'

        result = []
        conn = pyodbc.connect(self._conn_str_())
        cursor = conn.cursor()
        try:
            for row in cursor.execute(cmd):
                result.append(self.extract_row(row))
        except Exception as e:
            print(str(e))
        conn.close()
        return result

    @staticmethod
    def extract_row(row: pyodbc.Cursor):
        r = {}
        i = 0
        for item in row.cursor_description:
            name = item[0]
            val = str(row[i])
            name = name.lower()
            i += 1
            r[name] = val
        return r
