import logging
import re

import config


def get_data_mode_from_file_name(file_name):
    if re.search('train', file_name, re.IGNORECASE):
        DATA_MODE = 'TRAIN'
        logging.info('Assuming train data mode')
    elif re.search('eval', file_name):
        DATA_MODE = 'EVAL'
        logging.info('Assuming eval data mode')
    else:
        raise Exception(
            'file naming error: expected topics type to be specified by having "train" or "eval" in file name')
    return DATA_MODE


def get_year_from_file_name(file_name):
    if re.search('2021', file_name):
        YEAR = '2021'
        logging.info('Assuming 2021')
    elif re.search('2022', file_name):
        YEAR = '2022'
        logging.info('Assuming 2022')
    else:
        raise Exception(
            'file naming error: could not deduce year as either "2021" or "2022" from topics file name')
    return YEAR


def get_num_documents(year, unique=False):
    if year == '2021':
        return config.TRECFAIR2021_NUM_DOCUMENTS
    elif year == '2022':
        if unique:
            return config.TRECFAIR2022_NUM_DOCUMENTS
        return config.TRECFAIR2022_NUM_UNIQUE_DOCUMENTS
    else:
        raise ValueError('Expected "2021" or "2022" for year')


def get_num_queries(year, data_type):
    if data_type == 'TRAIN':
        if year == '2021':
            return config.TRECFAIR2021_NUM_TRAIN_QUERIES
        elif year == '2022':
            return config.TRECFAIR2022_NUM_TRAIN_QUERIES
        else:
            raise ValueError('Expected "2021" or "2022" for year')
    elif data_type == 'EVAL':
        if year == '2021':
            return config.TRECFAIR2021_NUM_EVAL_QUERIES
        elif year == '2022':
            return config.TRECFAIR2022_NUM_EVAL_QUERIES
        else:
            raise ValueError('Expected "2021" or "2022" for year')
    else:
        raise ValueError('Expected "TRAIN" or "EVAL" for data type')


def assert_file_naming(year=False, data_mode=False, *file_names):
    for file_name in file_names:
        if file_name == None:
            continue
        if year:
            assert re.search(year, file_name, re.IGNORECASE) != None
        if data_mode:
            assert re.search(data_mode, file_name, re.IGNORECASE) != None
