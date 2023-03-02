from .wmisdb import WMISDB


class Turnouts:
    _wmisdb = None
    turnout_id = None

    def __init__(self, turnout_id=None) -> None:
        self.turnout_id = turnout_id
        self._wmisdb = WMISDB()
        super().__init__()

    def data(self):
        result = []
        conn = self._wmisdb.connection
        cursor = conn.cursor()
        cmd = cmd = 'select turnout_id, description, capacity, code_id, manufacturer, serialno, metersize from turnout'
        if self.turnout_id is None:
            pass
        else:
            cmd = f"{cmd} where turnout_id = '{self.turnout_id}';"
        try:
            for row in cursor.execute(cmd):
                item = self._extract_row(row)
                result.append(item)
        except Exception as e:
            print(str(e))
        conn.close()
        return result

    def _extract_row(self, row):
        r = {}
        i = 0
        for item in row.cursor_description:
            name = item[0]
            val = str(row[i])
            name = name.lower()
            i += 1
            r[name] = val
        return r
