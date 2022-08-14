import argparse
import json
import logging
import os
from pathlib import Path
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, required=True, help='input file containing the downloaded trec fair 2022 corpus')
parser.add_argument('--output', type=str, required=True, help='output file containing the corpus in jsonl format for indexing')
parser.add_argument('--ignore-duplicates', action='store_true', help='ignore documents with same doc_ids')
parser.add_argument('--merge-duplicates', action='store_true', help='merge documents with same doc_ids')
args = parser.parse_args()

Path(os.path.dirname(args.output)).mkdir(parents=True, exist_ok=True)

logging.basicConfig(level=logging.INFO)

logging.info("converting collection...")

if args.ignore_duplicates and args.merge_duplicates:
    raise Exception("ignore duplicates and merge duplicates cannot both be")

with open(args.input, 'r') as f, open(args.output, 'w') as outf:
    if args.merge_duplicates:
        num_written = 0
        docs = {}
        for line in tqdm(f):
            raw = json.loads(line)
            if 'html' in raw:
                article = raw['html']
            elif 'plain' in raw:
                article = raw['plain']
            elif 'text' in raw:
                article = raw['text']
            else:
                raise Exception("couldn't find article")

            if raw['id'] not in docs:
                docs[raw['id']]= {
                    'id': raw['id'],
                    'contents': raw['title'] + '\t' + raw['url'] + '\t' + article,
                    'title': raw['title'],
                    'url': raw['url'],
                    'article': article
                }
            else:
                docs[raw['id']]['contents'] += '\t' + raw['title'] + '\t' + raw['url'] + '\t' + article
                docs[raw['id']]['title'] += '\t' + raw['title']
                docs[raw['id']]['url'] += '\t' + raw['url']
                docs[raw['id']]['article'] += '\t' + article

        for doc in docs.values():
            outf.write(json.dumps(doc) + "\n")
            num_written += 1
        logging.info(f"Wrote {num_written} documents to {args.output}")
    else:
        num_written = 0
        doc_ids = set()
        for line in tqdm(f):
            raw = json.loads(line)
            if 'html' in raw:
                article = raw['html']
            elif 'plain' in raw:
                article = raw['plain']
            elif 'text' in raw:
                article = raw['text']
            else:
                raise Exception("couldn't find article")

            if args.ignore_duplicates and raw['id'] in doc_ids:
                continue

            output = {
                "id": raw['id'],
                "contents": raw['title'] + "\t" + raw['url'] + "\t" + article,
                "title": raw['title'],
                "url": raw['url'],
                "article": article
            }
            outf.write(json.dumps(output) + "\n")
            num_written += 1
            doc_ids.add(raw['id'])
        logging.info(f"Wrote {num_written} documents to {args.output}")