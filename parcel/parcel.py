from wmisdb.wmisdb import WMISDB
from decouple import config


class Parcels:
    _wmisdb = None
    parcel_id = None
    isactive = None
    data = []

    def __init__(self, parcel_id=None, isactive=None) -> None:
        self.isactive = isactive
        self.parcel_id = parcel_id
        self._wmisdb = WMISDB()
        super().__init__()

    def parcel_details_w_acres(self) -> []:
        self.data = []
        conn = self._wmisdb.connection
        cursor = conn.cursor()

        params = ''
        if not(self.isactive is None):
            if params.__len__() > 0:
                params = params + ', '
            params = f"{params} @isactive = {self.isactive} "

        if not(self.parcel_id is None):
            if params.__len__() > 0:
                params = params + ', '
            params = f"{params} @parcel_id = '{self.parcel_id}' "

        cmd = f'exec sp_sgma_parcels {params};'

        try:
            for row in cursor.execute(cmd):
                item = self._wmisdb.extract_row(row)
                self.data.append(item)
        except Exception as e:
            print(str(e))
        conn.close()
        return self.data

    def parcel_list(self) -> []:
        result = []
        conn = self._wmisdb.connection
        cursor = conn.cursor()
        cmd = f'select parcel_id from parcel order by parcel_id;'
        try:
            for row in cursor.execute(cmd):
                result.append(row[0])
        except Exception as e:
            print(str(e))
        conn.close()
        return result

    def parcel_details(self) -> {}:
        result = None
        conn = self._wmisdb.connection
        cursor = conn.cursor()
        # cmd = f'select top 1 * from parcel where parcel_id = \'{self.parcel_id}\';'
        cmd = 'select top 1 '
        cmd += '  p.Parcel_Id, p.Acres, p.LegalDesc, p.Notes, p.IsActive, '
        cmd += '  p.Township, p.Range, p.Section, p.ParcelType, p.CountyCode, '
        cmd += '  p.DateCreated, p.UserCreated, p.DateChanged, p.UserChanged, '
        cmd += '  isnull(pa_sgma.Acres,0.0) as sgma_acres, '
        cmd += '  isnull(pa_spa.Acres,0.0) as spa_acres '
        cmd += 'from parcel p '
        cmd += 'left join papacode pa_sgma on p.Parcel_Id = pa_sgma.Parcel_Id and pa_sgma.Code_Id = ? '
        cmd += 'left join papacode pa_spa on p.Parcel_Id = pa_spa.Parcel_Id and pa_spa.Code_Id = ? '
        cmd += 'where p.parcel_id = ? '

        # SGMA_ELIGIBLE = PA0052
        # SGMA_SPA = PA0053

        try:
            for row in cursor.execute(cmd, (config('SGMA_ELIGIBLE'), config('SGMA_SPA'), self.parcel_id)):
                result = self._wmisdb.extract_row(row)
        except Exception as e:
            print(str(e))
        conn.close()
        return result
