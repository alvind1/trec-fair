import argparse
import json
import logging
from pathlib import Path
from tqdm import tqdm

import utils

parser = argparse.ArgumentParser(
    description='Convert trec fair queries to tsv format')
parser.add_argument('--input', type=str, required=True,
                    help='path to trec fair raw json topics')
parser.add_argument('--output', type=str, required=True,
                    help='tsv file to write queries to')
parser.add_argument('--eval', action='store_true',
                    help='convert eval topics instead of train topics')
args = parser.parse_args()

logging.basicConfig(level=logging.INFO)
logging.info('converting topics...')

YEAR = utils.get_year_from_file_name(args.input)
DATA_MODE = utils.get_data_mode_from_file_name(args.input)
utils.assert_file_naming(YEAR, DATA_MODE, args.input, args.output)

if YEAR == '2021':
    with open(args.input, 'r') as f, open(args.output, 'w') as outf:
        total = utils.get_num_queries(YEAR, DATA_MODE)
        for line in tqdm(f, total=total):
            query = json.loads(line)
            output = str(query['id']) + '\t' + query['title'] + \
                ' ' + ' '.join(query['keywords'])
            outf.write(output + '\n')
elif YEAR == '2022':
    with open(args.input, 'r') as f, open(args.output, 'w') as outf:
        line = f.readline()
        query = json.loads(line)
        total = utils.get_num_queries(YEAR, DATA_MODE)
        for docID, title, keywords in tqdm(zip(query['id'].values(), query['title'].values(), query['keywords'].values()), total=total):
            if args.eval:
                keywords = ' '.join(keywords)
            else:  # There are typos in the train topics so the parsing is different
                keywords = keywords.replace("'", '').replace(
                    '[', '').replace(']', '').replace(',', '')
            output = str(docID) + '\t' + title + ' ' + keywords
            outf.write(output + '\n')
