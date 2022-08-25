TRECFAIR2021_NUM_DOCUMENTS = 6280328
TRECFAIR2021_NUM_TRAIN_QUERIES = 57
TRECFAIR2021_NUM_EVAL_QUERIES = 49

TRECFAIR2022_NUM_DOCUMENTS = 6475537
TRECFAIR2022_NUM_UNIQUE_DOCUMENTS = 6475401
TRECFAIR2022_NUM_TRAIN_QUERIES = 46
TRECFAIR2022_NUM_EVAL_QUERIES = 47


def get_documents(year):
    if year == '2021':
        return TRECFAIR2021_NUM_DOCUMENTS
    elif year == '2022':
        return TRECFAIR2022_NUM_UNIQUE_DOCUMENTS
    else:
        raise ValueError('Expected "2021" or "2022" for year')


def get_queries(year, data_type):
    if data_type == 'TRAIN':
        if year == '2021':
            total = TRECFAIR2021_NUM_TRAIN_QUERIES
        elif year == '2022':
            total = TRECFAIR2022_NUM_TRAIN_QUERIES
        else:
            raise ValueError('Expected "2021" or "2022" for year')
    elif DATA_MODE == 'EVAL':
        if year == '2021':
            total = TRECFAIR2021_NUM_EVAL_QUERIES
        elif year == '2022':
            total = TRECFAIR2022_NUM_EVAL_QUERIES
        else:
            raise ValueError('Expected "2021" or "2022" for year')
    else:
        raise ValueError('Expected "TRAIN" or "EVAL" for data type')
