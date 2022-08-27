import argparse
import logging
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--t5-input', type=str, required=True)
parser.add_argument('--t5-ids-input', type=str, required=True)
parser.add_argument('--output', type=str, required=True)
parser.add_argument('--output-ids', type=str, required=True)
parser.add_argument('--relevance', type=str, choices=['true', 'false'], required=True)
args = parser.parse_args()

logging.basicConfig(level=logging.INFO)
logging.info(f'selecting only {args.relevance} from {args.t5_input}...')

relevance = args.relevance+'\n'

count = 0
with open(args.t5_input, 'r') as f_t5, open(args.t5_ids_input, 'r') as f_t5_ids, open(args.output, 'w') as f_out, open(args.output_ids, 'w') as f_out_ids:
  for line in tqdm(f_t5):
    id_line = f_t5_ids.readline()
    if line[-len(relevance):] == relevance:
      f_out.write(line) 
      f_out_ids.write(id_line)
      count += 1
logging.info(f'wrote {count} segments to {args.output}')
