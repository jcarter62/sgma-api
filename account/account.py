from wmisdb import WMISDB


class Accounts:
    _wmisdb = None

    def __init__(self):
        self._wmisdb = WMISDB()
        super().__init__()

    def account_list_all(self,
                         search_term: str = None,
                         include: str = None,
                         accounts_with_well: str = None,
                         ) -> []:
        result = []
        conn = self._wmisdb.connection
        cursor = conn.cursor()
        cmd = 'select name_id, fullname as account from name '
        cmd = ''
        cmd += 'SELECT n.name_id, n.fullname AS account, '
        cmd += ' CASE WHEN w.account IS NULL THEN 0 ELSE 1 END AS has_well '
        cmd += ' FROM name n '
        cmd += ' LEFT JOIN ( '
        cmd += '     SELECT DISTINCT account FROM sgma_wellassoc '
        cmd += ' ) w ON n.name_id = w.account '

        if include is None:
            cmd += 'where isnull(isactive,0) = 1 '
        elif include == 'all':
            pass
        elif include == 'inactive':
            cmd += 'where isnull(isactive,0) = 0 '
        elif include == 'active':
            cmd += 'where isnull(isactive,0) = 1 '
        else:
            pass  # default to all

        cmd += 'order by name_id ;'

        try:
            for row in cursor.execute(cmd):
                result.append({"account": row[0], "name": row[1], "has_well": row[2]})
        except Exception as e:
            print(str(e))

        rslt1 = []

        if accounts_with_well is not None:
            if accounts_with_well == '1':
                cmpval = 1
            else:
                cmpval = 0
            for item in result:
                if item['has_well'] == cmpval:
                    rslt1.append(item)
        else:
            rslt1 = result.copy()

        rslt2 = []

        if search_term is not None:
            srch = search_term.lower()
            for item in rslt1:
                txt = str(item['account']) + ' ' + item['name'].lower()
                if srch in txt:
                    rslt2.append(item)
                    # answer.append(item['account'])
        else:
            rslt2 = rslt1.copy()

        answer = []
        for item in rslt2:
            answer.append(item['account'])

        return answer

    def account_one_details(self, account: int) -> {}:
        result = {}
        conn = self._wmisdb.connection
        cursor = conn.cursor()
        cmd = 'select name_id as account, fullname as name, ' + \
              'address1, address2, address3, city, state, zip, isactive ' + \
              f'from name where name_id = {account} ;'
        try:
            for row in cursor.execute(cmd):
                result = self._wmisdb.extract_row(row)
        except Exception as e:
            print(str(e))

        return result

    def account_wells(self, account: int) -> []:
        result = []
        conn = self._wmisdb.connection
        cursor = conn.cursor()
        cmd = ''
        cmd += 'with '
        cmd += f'  owner as (select rec_id, well_id from sgma_wellassoc where account = {account}),'
        cmd += '  owner_count as (select well_id, count(*) as owners from sgma_wellassoc group by well_id)'
        cmd += 'select '
        cmd += '  wa.well_id, wa.amount, wa.begindate, wa.enddate, '
        cmd += '  case '
        cmd += '    when oc.owners = 1 then \'Full Owner\' '
        cmd += '	else \'Partial Owner\' '
        cmd += '  end as OwnerType,'
        cmd += '  oc.owners as OwnerCount '
        cmd += 'from sgma_wellassoc wa '
        cmd += 'join owner o on wa.rec_id = o.rec_id '
        cmd += 'left join owner_count oc on o.well_id = oc.well_id; '
        try:
            for row in cursor.execute(cmd):
                rowdata = self._wmisdb.extract_row(row)
                result.append(rowdata)
        except Exception as e:
            print(str(e))

        return result
