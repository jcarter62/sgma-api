"""
Reading class for reading data from WMISDB
"""
from wmisdb import WMISDB


class Reading:
    _wmisdb = None
    well_id = None

    def __init__(self) -> None:
        self._wmisdb = WMISDB()
        super().__init__()


    def last_reading(self, well_id) -> []:
        data = []
        conn = self._wmisdb.connection
        cursor = conn.cursor()

        cmd = 'select top 2 '
        cmd += 't.trndel_id, t.turnout_id as well_id, t.reading, t.readingdate, '
        cmd += 't.priorreading, t.priorreadingdate, t.actual '
        cmd += 'from trndemst t '
        cmd += f'where t.turnout_id = \'{well_id}\' '
        cmd += 'order by readingdate desc;'

        try:
            for row in cursor.execute(cmd):
                reading = self._wmisdb.extract_row(row)
                data.append(reading)
                break
        except Exception as err:
            print(f'Error in last_reading {err}')
        
        conn.close()
        return data

    def last_year(self, well_id) -> []:
        data = []
        conn = self._wmisdb.connection
        cursor = conn.cursor()

        cmd = 'select '
        cmd += 't.trndel_id, t.turnout_id as well_id, t.reading, t.readingdate, '
        cmd += 't.priorreading, t.priorreadingdate, t.actual '
        cmd += 'from trndemst t '
        cmd += f'where (t.readingdate > getdate()-370) and (t.turnout_id = \'{well_id}\') '
        cmd += 'order by readingdate desc;'

        try:
            for row in cursor.execute(cmd):
                reading = self._wmisdb.extract_row(row)
                data.append(reading)
        except Exception as e:
            print(str(e))
        conn.close()
        return data


    def meters(self) -> []:
        data = []
        conn = self._wmisdb.connection
        cursor = conn.cursor()

        cmd = 'select '
        cmd += 't.turnout_id as well_id, t.isactive as active '
        cmd += 'from turnout t '
        cmd += 'where t.subsystem_id in (\'GWMP\', \'SGMA\') '
        cmd += 'order by t.turnout_id;'

        try:
            for row in cursor.execute(cmd):
                reading = self._wmisdb.extract_row(row)
                data.append(reading)
        except Exception as e:
            print(str(e))
        conn.close()
        return data

    def add_reading(self, well_id: str, date: str, time: str, reading: float, operator: str, note: str, guid: str):
        conn = self._wmisdb.connection
        cursor = conn.cursor()

        # Execute Stored Procedure with Parameters in python
        # ref: https://stackoverflow.com/a/71961363
        #
        cmd = ''
        cmd += 'SET NOCOUNT ON; '
        cmd += 'DECLARE @rcode int; '
        cmd += 'DECLARE @rtext varchar(255); '
        cmd += 'DECLARE @rc int; '
        cmd += 'EXEC @rc = sp_mi_reading '
        cmd += '@asset = ?, @odometer = ?, @flow = ?, @assettype = ?, '
        cmd += '@timestamp = ?, @operator = ?, @device = ?, @notes = ?, @readingid = ?, '
        cmd += '@resultcode = @rcode, @resulttext = @rtext ;'
        cmd += 'SELECT @rc as result, @rcode, @rtext;'

        params = (well_id, reading, 0.0, 'w', f'{date} {time}', operator, 'web', note, guid, )

        try:
            cursor.execute(cmd, params)
            returnset = cursor.fetchall()
            cursor.commit()
            if returnset is not None:
                result = {"result": returnset[0][0], "error": ""}
        except Exception as e:
            print(str(e))
            result = {'result': -1, 'error': str(e)}
        conn.close()
        return result

    def process_pending_readings(self):
        conn = self._wmisdb.connection
        cursor = conn.cursor()

        # Execute Stored Procedure with Parameters in python
        # ref: https://stackoverflow.com/a/71961363
        #
        cmd = ''
        cmd += 'SET NOCOUNT ON; '
        cmd += 'EXEC sp_mi_process; '

        try:
            cursor.execute(cmd)
            returnset = cursor.fetchall()
            cursor.commit()
            if returnset is not None:
                result = {"result": returnset[0][0], "error": ""}
        except Exception as e:
            result = {'result': -1, 'error': str(e)}
        conn.close()
        return result


    def get_well_status(self):
        """Get list of wells, with isactive flag and hasreading flag"""
        data = []
        conn = self._wmisdb.connection
        cursor = conn.cursor()

        cmd = '''
            SELECT 
              t.Turnout_ID AS well_id, 
              CASE 
                WHEN ISNULL(t.IsActive,0) = 1 THEN 'x' 
                ELSE ' ' 
              END AS isactive, 
              CASE 
                WHEN lr.Turnout_ID IS NULL THEN ' ' 
                ELSE 'x' END 
              AS hasreadings 
            FROM turnout t 
            LEFT JOIN 
              (
                SELECT MAX(t.trndel_id) AS trndel_id, 
                t.Turnout_ID 
                FROM trndemst t 
                WHERE (t.ReadingDate > (GETDATE() - 370)) 
                GROUP BY t.turnout_id
              ) lr 
              ON t.Turnout_ID = lr.Turnout_ID 
            ORDER BY t.Turnout_ID;
        '''
        try:
            for row in cursor.execute(cmd):
                reading = self._wmisdb.extract_row(row)
                data.append(reading)
        except Exception as e:
            print(str(e))
        conn.close()
        return data
