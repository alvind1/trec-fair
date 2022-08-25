import argparse
import json
import logging
import numpy as np
import re
from tqdm import tqdm

import config

# modified from https://tech.hbc.com/2018-03-23-negative-sampling-in-numpy.html


def negsamp_vectorized_bsearch(pos_inds, n_items, n_samp):
    """ Pre-verified with binary search
    `pos_inds` is assumed to be ordered
    """
    raw_samp = np.random.choice(
        np.arange(n_items - len(pos_inds)), size=n_samp, replace=False)
    raw_samp.sort()
    pos_inds_adj = pos_inds - np.arange(len(pos_inds))
    ss = np.searchsorted(pos_inds_adj, raw_samp, side='right')
    neg_inds = raw_samp + ss
    return set(neg_inds)


def load_runs(path):
    logging.info("loading runs...")
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
    logging.info("loading doc ids...")
    docIDs = []
    with open(path, 'r') as f:
        docIDs = json.loads(f.readline())
        assert type(docIDs) == list
        if YEAR == '2021':
            assert len(docIDs) == config.TRECFAIR2021_NUM_DOCUMENTS
        elif YEAR == '2022':
            assert len(docIDs) == config.TRECFAIR2022_NUM_UNIQUE_DOCUMENTS
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


parser = argparse.ArgumentParser(
    description='Converts trec fair 2021 reldocs to qrels')
parser.add_argument('--input', type=str, required=True,
                    help='input file containing the rel docs of trec fair 2021 documents')
parser.add_argument('--output', type=str, required=True,
                    help='output file containg the rel docs in qrels format')
parser.add_argument('--run', type=str, default="", required=False,
                    help='path to BM25 run file from which to sample negative examples')
parser.add_argument('--docIDs', type=str, default="", required=False,
                    help='path to docIDs file, used to generate negative examples')
parser.add_argument('--random-negative-samples', action='store_true',
                    default=False, help='add randomly sampled negative examples from the corpus')
parser.add_argument('--run-negative-samples', action='store_true',
                    default=False, help='add sampled negative examples from run')
parser.add_argument('-v', '--verbose', action='store_true', help='verbose')
args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

DATA_MODE = ''
if re.search('train', args.input, re.IGNORECASE):
    DATA_MODE = 'TRAIN'
    logging.info('Assuming TRAIN data mode')
elif re.search('eval', args.input, re.IGNORECASE):
    DATA_MODE = 'EVAL'
    logging.info('Assuming EVAL data mode')
else:
    raise Exception(
        'file naming error: could not deduce data mode as either "train" or "eval" from input file name')

YEAR = ''
if re.search('2021', args.input):
    YEAR = '2021'
    logging.info('Assuming 2021')
elif re.search('2022', args.input):
    YEAR = '2022'
    logging.info('Assuming 2022')
else:
    raise Exception(
        'file naming error: could not deduce year as either "2021" or "2022" from input file name')

if args.run:
    assert re.search(DATA_MODE, args.run, re.IGNORECASE) != None
    assert re.search(YEAR, args.run) != None
assert re.search(DATA_MODE, args.output, re.IGNORECASE) != None
assert re.search(YEAR, args.output) != None

run = []
doc_ids = []
if args.random_negative_samples and args.run_negative_samples:
    raise Exception(
        'only one of the arguments random-negative-samples, run-negative-samples may be set')
elif args.random_negative_samples:
    assert args.docIDs != ""
    doc_ids = load_doc_ids(args.docIDs)
    logging.info('creating qrels with random negative samples...')
elif args.run_negative_samples:
    assert args.run != ""
    runs = load_runs(args.run)
    assert args.docIDs != ""
    doc_ids = load_doc_ids(args.docIDs)
    logging.info('creating qrles with random negative samples...')
else:
    logging.info('creating qrels...')
if YEAR == '2021':
    with open(args.input, 'r') as f, open(args.output, 'w') as outf:
        if DATA_MODE == 'TRAIN':
            total = config.TRECFAIR2021_NUM_TRAIN_QUERIES
        elif DATA_MODE == 'EVAL':
            total = config.TRECFAIR2021_NUM_EVAL_QUERIES
        else:
            total = None
        for line in tqdm(f, total=total):
            query = json.loads(line)
            rel_docs = set()
            for doc_id in query['rel_docs']:
                if doc_id not in rel_docs:
                    output = str(query['id']) + " 0 " + str(doc_id) + " 1"
                    outf.write(output + '\n')
                    rel_docs.add(doc_id)

            if args.random_negative_samples:
                pos_inds = get_pos_inds_from_docs(doc_ids, list(rel_docs))
                neg_inds = negsamp_vectorized_bsearch(
                    pos_inds, config.TRECFAIR2021_NUM_DOCUMENTS, len(rel_docs))
                assert len(neg_inds) == len(rel_docs)
                neg_elements = [doc_ids[i] for i in neg_inds]
                for doc_id in neg_elements:
                    output = str(query['id']) + " 0 " + str(doc_id) + " 0"
                    outf.write(output + '\n')
                    assert doc_id not in rel_docs
                logging.debug(
                    f"{query['id']} {len(rel_docs)} {len(pos_inds)} {len(neg_elements)}")
            elif args.run_negative_samples:
                pos_inds = get_pos_inds_from_run(
                    runs[query['id']], list(rel_docs))
                run_length = len(runs[query['id']])
                assert len(pos_inds) <= run_length
                num_negative_samples = min(
                    run_length - len(pos_inds), len(rel_docs))
                neg_inds = negsamp_vectorized_bsearch(
                    pos_inds, run_length, num_negative_samples)
                assert len(neg_inds) == num_negative_samples
                neg_elements = [runs[query['id']][i] for i in neg_inds]
                for doc_id in neg_elements:
                    output = str(query['id']) + " 0 " + str(doc_id) + " 0"
                    outf.write(output + '\n')
                    assert doc_id not in rel_docs
                #print(f"{query['id']} {len(rel_docs)} {len(pos_inds)} {num_negative_samples}")
elif YEAR == '2022':
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
                neg_inds = negsamp_vectorized_bsearch(
                    pos_inds, config.TRECFAIR2022_NUM_UNIQUE_DOCUMENTS, len(rel_docs))
                assert len(neg_inds) == len(rel_docs)
                neg_elements = [doc_ids[i] for i in neg_inds]
                for doc_id in neg_elements:
                    output = str(query_id) + ' 0 ' + str(doc_id) + ' 0'
                    outf.write(output + '\n')
                    assert doc_id not in rel_docs
                logging.debug(
                    f'query_id: {query_id} rel_docs: {len(rel_docs)} pos_inds: {len(pos_inds)} neg_docs: {len(neg_elements)}')
            elif args.run_negative_samples:
                pos_inds = get_pos_inds_from_run(
                    runs[query_id], list(rel_docs))
                run_length = len(runs[query_id])
                num_negative_samples = min(
                    run_length - len(pos_inds), len(rel_docs))
                neg_inds = negsamp_vectorized_bsearch(
                    pos_inds, run_length, num_negative_samples)
                assert len(neg_inds) == num_negative_samples
                neg_elements = [runs[query_id][i] for i in neg_inds]
                for doc_id in neg_elements:
                    output = str(query_id) + ' 0 ' + str(doc_id) + ' 0'
                    outf.write(output + '\n')
                    assert doc_id not in rel_docs
                logging.debug(
                    f'query_id: {query_id} rel_docs: {len(rel_docs)} pos_inds: {len(pos_inds)} neg_docs: {len(neg_elements)}')
