import os
import sqlite3
import config
import pandas as pd
from pandas.io import sql


def get_subject_and_session_id(df, i):
    x = df.iloc[i, 0].split('-')
    return '-'.join(x[0:-1]), '-'.join(x)


def get_subject_session_count(session_counts, subject_id):
    return len(session_counts[subject_id])


def run():

    session_ids = {}

    # df = pd.read_csv('/Users/Ralph/development/brainminer/data/CorticalMeasures_SurfAvg_NeuroIMAGE.csv')
    # for i in df.index:
    #     subject_id, session_id = get_subject_and_session_id(df, i)
    #     if subject_id not in session_ids:
    #         session_ids[subject_id] = [session_id]
    #     else:
    #         session_ids[subject_id].append(session_id)
    #
    # # For each subject we have 2 session IDs. Create two files, each with the same subject IDs but data
    # # from different sessions.
    #
    # subjects1 = []
    # for sid in session_ids.keys():
    #     if len(session_ids[sid]) == 2:
    #         idd = session_ids[sid][0]
    #         subjects1.append(idd)
    #
    # subjects2 = []
    # for sid in session_ids.keys():
    #     if len(session_ids[sid]) == 2:
    #         idd = session_ids[sid][1]
    #         subjects2.append(idd)

    # Open CSV files and merge them
    df1 = pd.read_csv('/Users/Ralph/development/brainminer/data/CorticalMeasures_SurfAvg_NeuroIMAGE.csv')
    df2 = pd.read_csv('/Users/Ralph/development/brainminer/data/CorticalMeasures_ThickAvg_NeuroIMAGE.csv')
    df3 = pd.read_csv('/Users/Ralph/development/brainminer/data/SubcorticalMeasures_Volume_NeuroIMAGE.csv')
    df = pd.concat([df1, df2, df3], axis=1)
    df.to_csv('/Users/Ralph/development/brainminer/data/All.csv', index=True)


# def run():
#
#     file_names = [
#         config.FILE_NAME_META_DATA,
#         config.FILE_NAME_SURFACE,
#         config.FILE_NAME_THICKNESS,
#         config.FILE_NAME_VOLUME,
#     ]
#
#     table_names = [
#         config.TABLE_NAME_META_DATA,
#         config.TABLE_NAME_SURFACE,
#         config.TABLE_NAME_THICKNESS,
#         config.TABLE_NAME_VOLUME,
#     ]
#
#     for i in range(len(file_names)):
#
#         f = file_names[i]
#         f_db = f + '.sqlite3'
#         if os.path.isfile(f_db):
#             os.remove(f_db)
#         if f.endswith('xlsx'):
#             df = pd.read_excel(f)
#         elif f.endswith('csv'):
#             df = pd.read_csv(f)
#         for col in df.columns:
#             df = df.rename(columns={col: col.replace(' ', '_')})
#         connection = sqlite3.connect(f_db)
#         sql.to_sql(df, table_names[i], connection)
#
#     print('Done')


if __name__ == '__main__':
    run()
