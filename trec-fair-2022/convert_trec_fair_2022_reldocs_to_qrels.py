import argparse
import json
import logging
import numpy as np
from tqdm import tqdm

import config

# from https://tech.hbc.com/2018-03-23-negative-sampling-in-numpy.html
def negsamp_vectorized_bsearch(pos_inds, n_items, n_samp):
    """ Pre-verified with binary search
    `pos_inds` is assumed to be ordered
    """
    raw_samp = np.random.choice(np.arange(n_items - len(pos_inds)), size=n_samp, replace=False)
    raw_samp.sort()
    pos_inds_adj = pos_inds - np.arange(len(pos_inds))
    ss = np.searchsorted(pos_inds_adj, raw_samp, side='right')
    neg_inds = raw_samp + ss
    return set(neg_inds)

def load_runs(path):
    runs = {}
    prev_query_id = -1
    with open(path, 'r') as f_run:
        for line in tqdm(f_run):
            query_id, _, doc_id, _, _, _ = line.split()
            query_id = int(query_id)
            doc_id = int(doc_id.rstrip('\n'))
            if query_id != prev_query_id:
                if prev_query_id != -1:
                    runs[prev_query_id].sort()
                runs[query_id] = []
                prev_query_id = query_id
            runs[query_id].append(doc_id)
        runs[prev_query_id].sort()
    return runs

def load_doc_ids(path):
    logging.info("loading doc_ids")
    docIDs = []
    with open(path, 'r') as f:
        docIDs = json.loads(f.readline())
        assert type(docIDs) == list
        assert len(docIDs) == config.NUM_UNIQUE_DOCUMENTS
    return docIDs

def get_pos_inds_from_docs(doc_ids, rel_docs):
    rel_docs.sort()
    pos_inds = np.searchsorted(doc_ids, rel_docs)
    return pos_inds

def get_pos_inds_from_run(run_docs, rel_docs):
    rel_docs.sort()
    a_temp = np.searchsorted(run_docs, rel_docs, 'left')
    b_temp = np.searchsorted(run_docs, rel_docs, 'right')
    return a_temp[a_temp != b_temp]

parser = argparse.ArgumentParser()
parser.add_argument("--input", type=str, required=True, help='input file containing the rel docs of trec fair 2022 documents')
parser.add_argument("--output", type=str, required=True, help='output file containg the rel docs in qrels format')
parser.add_argument('--run', type=str, default='', required=False, help='path to BM25 run file from which to sample negative examples')
parser.add_argument('--docIDs', type=str, default="", required=False, help='path to docIDs file, used to generate negative examples')
parser.add_argument('--random-negative-samples', action='store_true', default=False, help='add randomly sampled negative examples from the corpus')
parser.add_argument('--run-negative-samples', action='store_true', default=False, help='add sampled negative examples from run')
parser.add_argument('-v', '--verbose', action='store_true', help='verbose')
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
logging.info('converting reldocs to qrels...')

run = []
doc_ids = []
if args.random_negative_samples:
    logging.info('generating random negative samples from rel docs')
    assert args.docIDs != ''
    doc_ids = load_doc_ids(args.docIDs)

if args.run_negative_samples:
    logging.info('generating negative samples from runs')
    assert args.run != ''
    runs = load_runs(args.run)
    assert args.docIDs != ''
    doc_ids = load_doc_ids(args.docIDs)

with open(args.input, 'r') as f, open(args.output, 'w') as outf:
    line = f.readline()
    query = json.loads(line)
    for idx in tqdm(query['rel_docs'].keys()):
        query_id = query['id'][idx]
        line = json.loads(query['rel_docs'][idx])
        rel_docs = set()
        logging.debug(f'query {query_id}')
        logging.debug(f'generating relevant qrels')
        for doc_id in line:
            if doc_id not in rel_docs:
                output = str(query_id) + ' 0 ' + str(doc_id) + ' 1'
                outf.write(output + '\n')
                rel_docs.add(doc_id)
        if args.random_negative_samples:
            logging.debug(f'generating random negative qrels from doc_ids')
            pos_inds = get_pos_inds_from_docs(doc_ids, list(rel_docs))
            neg_inds = negsamp_vectorized_bsearch(pos_inds, config.NUM_UNIQUE_DOCUMENTS, len(rel_docs))
            assert len(neg_inds) == len(rel_docs)
            neg_elements = [doc_ids[i] for i in neg_inds]
            for doc_id in neg_elements:
                output = str(query_id) + ' 0 ' + str(doc_id) + ' 0'
                outf.write(output + '\n')
                assert doc_id not in rel_docs
            logging.debug(f'query_id: {query_id} rel_docs: {len(rel_docs)} pos_inds: {len(pos_inds)} neg_docs: {len(neg_elements)}')
        elif args.run_negative_samples:
            pos_inds = get_pos_inds_from_run(runs[query_id], list(rel_docs))
            run_length = len(runs[query_id])
            num_negative_samples = min(run_length - len(pos_inds), len(rel_docs))
            neg_inds = negsamp_vectorized_bsearch(pos_inds, run_length, num_negative_samples)
            assert len(neg_inds) == num_negative_samples
            neg_elements = [runs[query_id][i] for i in neg_inds]
            for doc_id in neg_elements:
                output = str(query_id) + ' 0 ' + str(doc_id) + ' 0'
                outf.write(output + '\n')
                assert doc_id not in rel_docs
            logging.debug(f'query_id: {query_id} rel_docs: {len(rel_docs)} pos_inds: {len(pos_inds)} neg_docs: {len(neg_elements)}')
