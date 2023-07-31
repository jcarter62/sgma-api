from wmisdb import WMISDB


class DataCalc:
    _wmisdb = None
    from_date = None
    to_date = None
    calc_date = None
    tc_code = None
    code_code = None
    post = None

    def __init__(self) -> None:
        self.post = 0
        self._wmisdb = WMISDB()
        super().__init__()

    def __del__(self):
        del self._wmisdb

    def sp_gwcalc(self, from_date, to_date, calc_date, tc_code, code_code, post) -> []:
        result = []
        conn = self._wmisdb.connection
        cursor = conn.cursor()
        cmd = f'exec sp_gwcalc @from_date = ?, @to_date = ?, ' \
              f'@calc_date = ?, @tc_code = ?, @code_code = ?, ' \
              f'@post = ?;'
        params = (from_date, to_date, calc_date, tc_code, code_code, post)

        try:
            cursor.execute(cmd, params)
            row = cursor.fetchone()
            item = self._wmisdb.extract_row(row)
            result.append(item)
        except Exception as e:
            print(str(e))
        try:
            pass
        except Exception as e:
            print(str(e))
        return result

    def load_results(self) -> []:
        results = []
        conn = self._wmisdb.connection
        cursor = conn.cursor()
        cmd = 'select * from gwcalc_results order by name_id, code_id, description;'
        try:
            for row in cursor.execute(cmd):
                item = self._wmisdb.extract_row(row)
                results.append(item)
        except Exception as e:
            print(str(e))
        return results

    def load_status(self) -> []:
        results = []
        conn = self._wmisdb.connection
        cursor = conn.cursor()
        cmd = 'select * from gwcalc_status;'
        try:
            for row in cursor.execute(cmd):
                item = self._wmisdb.extract_row(row)
                results.append(item)
        except Exception as e:
            print(str(e))
        return results


