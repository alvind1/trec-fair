import argparse
import json
import logging
from pathlib import Path
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Convert trec fair 2021 queries to tsv format')
parser.add_argument('--input', type=str, required=True, help='path to trec fair 2021 raw json topics')
parser.add_argument('--output', type=str, required=True, help='tsv file to write queries to')
args = parser.parse_args()

logging.basicConfig(level=logging.INFO)
logging.info('loading topics...')

with open(args.input, 'r') as f, open(args.output, 'w') as outf:
    for line in tqdm(f):
        query = json.loads(line)
        output = str(query['id']) + "\t" + query['title'] + " " + " ".join(query['keywords'])
        outf.write(output + '\n')
