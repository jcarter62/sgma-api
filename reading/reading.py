from wmisdb import WMISDB
from decouple import config


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
        except Exception as e:
            print(str(e))
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