import os
import sqlite3
import config
import pandas as pd
from pandas.io import sql


def run():
    
    file_names = [
        config.FILE_NAME_META_DATA,
        config.FILE_NAME_SURFACE,
        config.FILE_NAME_THICKNESS,
        config.FILE_NAME_VOLUME,
    ]
    
    table_names = [
        config.TABLE_NAME_META_DATA,
        config.TABLE_NAME_SURFACE,
        config.TABLE_NAME_THICKNESS,
        config.TABLE_NAME_VOLUME,
    ]
    
    for i in range(len(file_names)):
        f = file_names[i]
        f_db = f + '.sqlite3'
        if os.path.isfile(f_db):
            os.remove(f_db)
        if f.endswith('xlsx'):
            df = pd.read_excel(f)
        elif f.endswith('csv'):
            df = pd.read_csv(f)
        for col in df.columns:
            df = df.rename(columns={col: col.replace(' ', '_')})
        connection = sqlite3.connect(f_db)
        sql.to_sql(df, table_names[i], connection)
    
    print('Done')


if __name__ == '__main__':
    run()
