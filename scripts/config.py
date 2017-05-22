
FILE_NAME_META_DATA = '/Users/Ralph/data/imagemend/neuroimage/20160415_RUNMC_NeuroIMAGE_CleanSample.xlsx'
FILE_NAME_SURFACE = '/Users/Ralph/data/imagemend/neuroimage/CorticalMeasures_SurfAvg_NeuroIMAGE.csv'
FILE_NAME_THICKNESS = '/Users/Ralph/data/imagemend/neuroimage/CorticalMeasures_ThickAvg_NeuroIMAGE.csv'
FILE_NAME_VOLUME = '/Users/Ralph/data/imagemend/neuroimage/SubcorticalMeasures_Volume_NeuroIMAGE.csv'

TABLE_NAME_META_DATA = 'NeuroIMAGE'
TABLE_NAME_SURFACE = 'Surface'
TABLE_NAME_THICKNESS = 'Thickness'
TABLE_NAME_VOLUME = 'Volume'

QUERY_META_DATA = '''
  SELECT
    NeuroIMAGE_Number,
    type,
    Diagnosis,
    Gender
  FROM
    NeuroIMAGE;
'''
