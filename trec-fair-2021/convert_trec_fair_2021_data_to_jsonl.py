import argparse
import json
import logging
from pathlib import Path
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Convert raw trec fair 2021 corpus to jsonl file for indexing')
parser.add_argument('--input', type=str, required=True, help='path to raw corpus')
parser.add_argument('--output', type=str, required=True, help='jsonl file to write to')
args = parser.parse_args()

logging.basicConfig(level=logging.INFO)
logging.info("loading dataset...")

with open(args.input, 'r') as f, open(args.output, 'w') as outf:
    for line in tqdm(f):
        doc = json.loads(line)
        raw = {
            'doc_id': doc['id'],
            'title': doc['title'],
            'text': doc['text'],
            'marked_up_text': doc['marked_up_text'],
            'url': doc['url']
            #"quality_score": doc.quality_score,
            #"geographic_locations": doc.geographic_locations,
            #"quality_score_disk": doc.quality_score_disk
        }
        output = {
            'id': doc['id'],
            'contents': doc['title'] + '\t' + doc['url'] + "\t" + doc['text'],
            "raw": raw
        }
        outf.write(json.dumps(output) + '\n')
