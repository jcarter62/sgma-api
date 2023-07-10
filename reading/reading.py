"""
A module containing the Reading class.
"""
from typing import List, Dict
from wmisdb import WMISDB, DBError

class Reading:
    """
    A class for managing well readings in the WMIS database.
    depends on WMISDB class to connect to the database.
    """
    _wmisdb = None
    well_id = None

    def __init__(self) -> None:
        """
        Constructor for the Reading class.
        depends on WMISDB class to connect to the database.
        :return: None
        """
        self._wmisdb = WMISDB()
        super().__init__()


    def last_reading(self, well_id) -> List[Dict]:
        """Retrieves the last reading for a well."""
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
        except DBError as err:
            print(f'Error in last_reading {err}')
        
        conn.close()
        return data

    def last_year(self, well_id) -> List[Dict]:
        """
        Generate a list of readings for well_id for the last year.
        """
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
        except DBError as err:
            print(f'Error in last_year {err}')                
        except Exception as err:
            print(f'Unexpected Error: {err}')
        conn.close()
        return data


    def meters(self) -> List[Dict]:
        """
        Generate a list of meters, with isactive flag.
        """
        data = []
        conn = self._wmisdb.connection
        cursor = conn.cursor()

        # cmd = 'select '
        # cmd += 't.turnout_id as well_id, t.isactive as active '
        # cmd += 'from turnout t '
        # cmd += 'where t.subsystem_id in (\'GWMP\', \'SGMA\') '
        # cmd += 'order by t.turnout_id;'

        cmd = '''
            DECLARE @ReferenceDate DATE = DATEADD(DAY, -370, GETDATE());
            
            SELECT t.turnout_id AS well_id, t.isactive AS active, COUNT(rd.ReadingDate) AS readingcount
            FROM turnout t
            LEFT JOIN TRNDEMST rd ON rd.Turnout_ID = t.Turnout_ID AND rd.ReadingDate > @ReferenceDate
            WHERE t.subsystem_id IN ('GWMP', 'SGMA')
            GROUP BY t.turnout_id, t.isactive
            ORDER BY t.turnout_id;
            '''

        try:
            for row in cursor.execute(cmd):
                reading = self._wmisdb.extract_row(row)
                data.append(reading)
        except Exception as err:
            print(str(err))
        conn.close()
        return data


    def process_pending_readings(self):
        """Process pending readings in the database."""
        conn = self._wmisdb.connection
        cursor = conn.cursor()

        # Execute Stored Procedure with Parameters in python
        # ref: https://stackoverflow.com/a/71961363
        #
        cmd = ''
        cmd += 'SET NOCOUNT ON; '
        cmd += 'DECLARE @n int; '
        cmd += 'select @n = isnull(count(*),0) from TabletIncomingMeterReadings51;'
        cmd += 'if @n > 0 EXEC sp_mi_process; '

        try:
            cursor.execute(cmd)
            returnset = cursor.fetchall()
            cursor.commit()
            if returnset is not None:
                result = {"result": returnset[0][0], "error": ""}
        except DBError as err:
            result = {'result': -1, 'error': str(err)}
        except Exception as err:
            result = {'result': -1, 'error': str(err)}
        finally:
            pass
            # conn.close()
        return result


    def add_reading(self, well_id: str, date: str, time: str, reading: float, operator: str, note: str, guid: str):
        """Add a reading to the database."""
        conn = self._wmisdb.connection
        cursor = conn.cursor()
        #
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
            self.process_pending_readings()
            if returnset is not None:
                result = {"result": returnset[0][0], "error": ""}
        except DBError as err:
            result = {'result': -1, 'error': str(err)}                
        except Exception as err:
            result = {'result': -1, 'error': str(err)}

        try:
            conn.close()
        except Exception as err:
            print(f'Error closing connection: {err}')
        return result


    def get_well_status(self) -> List[Dict]:
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
              AS hasreadings,
			  case 
			    when 
			      (
			       (lrd.ReadingDate is null) or 
			       (lrd.ReadingDate < (getdate() - 15))
			      ) and (isnull(t.IsActive,0) = 1) 
				then 'x'
			    else ' ' 
			  end as needreading
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
		    left join 
			  (
			    select x.ReadingDate, x.TrnDel_ID 
				from trndemst x
			  ) lrd 
			  on lr.trndel_id = lrd.TrnDel_ID
			WHERE t.subsystem_id IN ('GWMP', 'SGMA')              
            ORDER BY t.Turnout_ID;            
        '''
        try:
            for row in cursor.execute(cmd):
                reading = self._wmisdb.extract_row(row)
                data.append(reading)
        except DBError as err:
            print(f'Error in get_well_status {err}')
        except Exception as err:
            print(str(err))
        finally:
            conn.close()
        return data
