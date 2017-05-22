import sqlite3
import config


def run():
    
    connection = sqlite3.connect(config.FILE_NAME_META_DATA + '.sqlite3')
    cursor = connection.cursor()
        
    cursor.execute('''
      SELECT NeuroIMAGE_Number, type, Diagnosis FROM NeuroIMAGE WHERE
        type = 'Child' AND
        Diagnosis = 'CON';
    ''')
        
    for record in cursor.fetchall():
        print(record)
        
    # In the end I should have two datasets each containing the exact same subjects but
    # taken at different time points.


if __name__ == '__main__':
    run()
