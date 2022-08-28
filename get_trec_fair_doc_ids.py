import argparse
import json
import logging
from tqdm import tqdm

import config

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, required=True)
parser.add_argument('--output', type=str, required=True)
args = parser.parse_args()

logging.basicConfig(level=logging.INFO)
logging.info('getting doc ids...')

with open(args.input, 'r') as f, open(args.output, 'w') as outf:
    docIDs = set()
    for line in tqdm(f):
        line = json.loads(line)
        docIDs.add(int(line['id']))
    docIDList = list(docIDs)
    docIDList.sort()
    json.dump(docIDList, outf)
    logging.info(f'wrote {len(docIDList)} doc ids')
