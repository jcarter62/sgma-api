from wmisdb import WMISDB


class WellAssoc:
    _wmisdb = None

    def __init__(self) -> None:
        self._wmisdb = WMISDB()
        super().__init__()

    def __del__(self):
        del self._wmisdb

    def well_assoc_all(self) -> []:
        result = []
        conn = self._wmisdb.connection
        cursor = conn.cursor()
        params = ''
        cmd = f'select * from sgma_wellassoc order by well_id, account;'
        try:
            for row in cursor.execute(cmd):
                item = self._wmisdb.extract_row(row)
                result.append(item)
        except Exception as e:
            print(str(e))
        try:
            pass
        except Exception as e:
            print(str(e))
        return result

    def get_account_name(self, account: str) -> str:
        result = ''
        conn = self._wmisdb.connection
        cursor = conn.cursor()
        params = ''
        # account is a numeric in the sql server database, so we don't need quotes.
        cmd = f'select n.FirstName, n.LastName, n.FullName from name n where name_id = {account};'
        try:
            for row in cursor.execute(cmd):
                result = {
                    "firstname": row[0],
                    "lastname": row[1],
                    "fullname": row[2],
                }
        except Exception as e:
            print(str(e))
        try:
            pass
        except Exception as e:
            print(str(e))
        return result

    def get_account_details(self, account: str) -> str:
        result = ''
        conn = self._wmisdb.connection
        cursor = conn.cursor()
        params = ''
        # account is a numeric in the sql server database, so we don't need quotes.
        cmd = 'select '
        cmd += 'n.FirstName, n.LastName, n.FullName, '
        cmd += 'isnull(n.address1, \'\') as addr1, '
        cmd += 'isnull(n.Address2, \'\') as addr2, '
        cmd += 'isnull(n.Address3, \'\') as addr3, '
        cmd += 'n.City, n.State, n.Zip, '
        cmd += 'rtrim(ltrim(n.City)) + \' \' + rtrim(ltrim(n.state)) + \' \' + rtrim(ltrim(n.zip)) as CSZ '
        cmd += f'from name n where name_id = {account};'

        try:
            for row in cursor.execute(cmd):
                result = self._wmisdb.extract_row(row)
        except Exception as e:
            print(str(e))
        try:
            pass
        except Exception as e:
            print(str(e))
        return result

    def well_assoc_one(self, well_id: str) -> []:
        result = []
        conn = self._wmisdb.connection
        cursor = conn.cursor()
        params = ''
        cmd = f'select * from sgma_wellassoc where well_id = \'{well_id}\' order by account;'
        try:
            for row in cursor.execute(cmd):
                item = self._wmisdb.extract_row(row)
                result.append(item)
        except Exception as e:
            print(str(e))
        try:
            pass
        except Exception as e:
            print(str(e))
        return result

    def well_assoc_add(self, well_id: str, account: str, amount: float, method: str, begindate: str, enddate: str,
                       ordering: int, isactive: int) -> []:
        result = []
        conn = self._wmisdb.connection
        cursor = conn.cursor()

        cmd = 'insert into sgma_wellassoc (well_id, account, amount, method, begindate, enddate, ordering, isactive) '
        cmd += 'values ( ?, ?, ?, ?, ?, ?, ?, ?);'
        try:

            cursor.execute(cmd, (well_id, account, amount, method, begindate, enddate, ordering, isactive))
            conn.commit()
            result = self.well_assoc_one(well_id)
        except Exception as e:
            print(str(e))
        try:
            pass
        except Exception as e:
            print(str(e))
        return result

    def well_list_all(self) -> []:
        result = []
        conn = self._wmisdb.connection
        cursor = conn.cursor()
        cmd = f'exec sp_sgma_well_list;'
        try:
            for row in cursor.execute(cmd):
                item = self._wmisdb.extract_row(row)
                result.append(item)
        except Exception as e:
            print(str(e))
        try:
            pass
        except Exception as e:
            print(str(e))
        return result

    def well_list_one(self, well_id: str) -> []:
        result = []
        conn = self._wmisdb.connection
        cursor = conn.cursor()
        cmd = f'select * from sgma_wellassoc where well_id = \'{well_id}\' order by ordering, account ;'
        try:
            for row in cursor.execute(cmd):
                item = self._wmisdb.extract_row(row)
                if item['enddate'][0:10] == '1900-01-01':
                    item['enddate'] = ''
                result.append(item)
        except Exception as e:
            print(str(e))
        try:
            pass
        except Exception as e:
            print(str(e))
        return result

    def lookup_one_record(self, rec_id: str) -> {}:
        result = None
        conn = self._wmisdb.connection
        cursor = conn.cursor()
        cmd = f'select * from sgma_wellassoc where rec_id = \'{rec_id}\';'
        try:
            for row in cursor.execute(cmd):
                result = self._wmisdb.extract_row(row)
        except Exception as e:
            print(str(e))
        try:
            pass
        except Exception as e:
            print(str(e))
        return result

    def delete_one_record(self, rec_id: str) -> bool:
        """Delete one record, and return True if successful, False if not."""
        conn = self._wmisdb.connection
        cursor = conn.cursor()
        cmd = f'delete from sgma_wellassoc where rec_id = \'{rec_id}\';'
        try:
            cursor.execute(cmd)
            conn.commit()
            result = True
        except Exception as e:
            print(str(e))
            result = False
        return result

    def update_one_record(self, rec_id: str, well_id: str, account: str, amount: float, method: str, begindate: str,
                          enddate: str, ordering: int, isactive: int) -> {}:
        result = None
        conn = self._wmisdb.connection
        cursor = conn.cursor()
        cmd = 'update sgma_wellassoc ' + \
              'set well_id = ?, account = ?, amount = ?, method = ?, ' + \
              'begindate = ?, enddate = ?, ordering = ?, isactive = ? where rec_id = ?;'
        try:
            if enddate == '' or enddate == '1900-01-01':
                enddate = None
            cursor.execute(cmd, (well_id, account, amount, method, begindate, enddate, ordering, isactive, rec_id))
            conn.commit()
            result = self.lookup_one_record(rec_id)
        except Exception as e:
            print(str(e))
        try:
            pass
        except Exception as e:
            print(str(e))
        return result

    def insert_one_record(self, rec_id: str, well_id: str, account: str, amount: float, method: str, begindate: str,
                          enddate: str, ordering: int, isactive: int) -> {}:
        result = None
        conn = self._wmisdb.connection
        cursor = conn.cursor()
        cmd = 'insert into sgma_wellassoc ' + \
              '(rec_id, well_id, account, amount, method, begindate, enddate, ordering, isactive) ' + \
              'values (?, ?, ?, ?, ?, ?, ?, ?, ?);'
        try:
            if enddate == 'None':
                enddate = None

            cursor.execute(cmd, (rec_id, well_id, account, amount, method, begindate, enddate, ordering, isactive))
            conn.commit()
            result = self.lookup_one_record(rec_id)
        except Exception as e:
            print(str(e))
        try:
            pass
        except Exception as e:
            print(str(e))
        return result

    def reorder_well_records(self, well_id):
        """Reorder sgma_wellassoc records by ordering and account.  Return True if successful, False otherwise."""
        result = True

        conn = self._wmisdb.connection
        cursor = conn.cursor()
        data = []

        # first get list of rec_ids, account, ordering
        cursor = conn.cursor()
        cmd = 'select rec_id, account, ordering from sgma_wellassoc ' + \
              'where well_id = \'' + well_id + '\' ' + \
              'order by ordering, account; '
        try:
            curs = cursor.execute(cmd)
            for row in curs:
                data.append(self._wmisdb.extract_row(row))
        except Exception as e:
            result = False
            print(str(e))

        # if there are no records, then we are done.
        if data.__len__() > 0:
            # now calculate ordering values
            ordering = 10
            for item in data:
                item['ordering'] = ordering
                ordering += 2

            # now update the database
            cmd = 'update sgma_wellassoc set ordering = ? where rec_id = ?;'
            try:
                for item in data:
                    cursor.execute(cmd, (item['ordering'], item['rec_id']))
                conn.commit()
            except Exception as e:
                result = False
                print(str(e))
        else:
            # no records to re-order
            pass

        return result

    def get_well_details(self, well_id) -> {}:
        result = {
            "WellID": well_id,
            "Description": "",
            "SerialNumber": "",
            "TotalAmount": 0.0,
            "RecordCount": 0,
        }
        conn = self._wmisdb.connection
        cursor = conn.cursor()
        cmd = f'select * from turnout where turnout_id = \'{well_id}\';'
        try:
            curs = cursor.execute(cmd)
            for row in curs:
                data = self._wmisdb.extract_row(row)
                if data is not None:
                    result['Description'] = data['description']
                    result['SerialNumber'] = data['serialno']
                    break
        except Exception as e:
            print(str(e))

        cmd = f'select * from sgma_wellassoc where well_id = \'{well_id}\';'
        total_amount = 0.0
        record_count = 0
        try:
            curs = cursor.execute(cmd)
            for row in curs:
                data = self._wmisdb.extract_row(row)
                if data is not None:
                    if int(data['isactive']) == 1:
                        total_amount += float(data['amount'])
                    record_count += 1
        except Exception as e:
            print(str(e))

        result['TotalAmount'] = total_amount
        result['RecordCount'] = record_count

        return result
