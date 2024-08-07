from wmisdb import WMISDB


class DataCalc:
    _wmisdb = None
    from_date = None
    to_date = None
    calc_date = None
    tc_code = None
    code_code = None
    post = None
    username = None

    def __init__(self, username: str = None) -> None:
        self.post = 0
        # self._wmisdb = WMISDB()
        self.username = username
        super().__init__()

    def __del__(self):
        if self._wmisdb is not None:
            del self._wmisdb

    def sp_gwcalc(self, from_date, to_date, calc_date, tc_code, code_code, cc_exclude, post_param) -> []:
        result = []
        self._wmisdb = WMISDB()
        conn = self._wmisdb.connection
        cursor = conn.cursor()
        cmd = f'exec sp_gwcalc @from_date = ?, @to_date = ?, ' \
              f'@calc_date = ?, @tc_code = ?, @code_code = ?, ' \
              f'@cc_exclude = ?, ' \
              f'@post = ?,@username = ?;'
        params = (from_date, to_date, calc_date, tc_code, code_code, cc_exclude, int(post_param), self.username)

        try:
            cursor.execute(cmd, params)
            row = cursor.fetchone()
            item = self._wmisdb.extract_row(row)
            result.append(item)
            conn.commit()
        except Exception as e:
            print(str(e))
        try:
            pass
        except Exception as e:
            print(str(e))
        return result

    def load_results(self) -> []:
        results = []
        self._wmisdb = WMISDB()
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
        self._wmisdb = WMISDB()
        conn = self._wmisdb.connection
        cursor = conn.cursor()
        # cmd = 'select * from gwcalc_status;'
        cmd = "select gs.*, " + \
              "(select count(*) from gwcalc_results where code_id like '%er%') as errors " + \
              "from gwcalc_status gs;"
        try:
            for row in cursor.execute(cmd):
                item = self._wmisdb.extract_row(row)
                results.append(item)
        except Exception as e:
            print(str(e))
        return results

    def load_history(self) -> []:
        results = []
        self._wmisdb = WMISDB()
        conn = self._wmisdb.connection
        cursor = conn.cursor()
        cmd = "select gs.* " + \
              "from gwcalc_status_hist gs " +\
                "order by updated desc;"
        try:
            for row in cursor.execute(cmd):
                item = self._wmisdb.extract_row(row)
                results.append(item)
        except Exception as e:
            print(str(e))
        return results
