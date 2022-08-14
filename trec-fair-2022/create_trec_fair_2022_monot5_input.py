import argparse
import json
import logging
import re
import spacy
from tqdm import tqdm


def load_corpus(path):
    logging.info('loading corpus...')
    corpus = {}
    with open(path, 'r') as fcorpus:
        for line in tqdm(fcorpus):
            line = json.loads(line)
            corpus[int(line['id'])] = line
    return corpus


def load_queries(path):
    queries = {}
    with open(path, 'r') as fqueries:
        for line in tqdm(fqueries):
            line = line.rstrip().split('\t')
            query_id = int(line[0])
            query, keywords = line[1].split(maxsplit=1)
            queries[query_id] = (query, keywords)
    return queries


def load_run(path):
    logging.info('loading runs...')
    run = {}
    with open(path, 'r') as frun:
        for line in tqdm(frun):
            query_id, _, doc_id, _, _, _ = line.split()
            query_id = int(query_id)
            doc_id = int(doc_id.rstrip('\n'))
            if query_id not in run:
                run[query_id] = []
            run[query_id].append((doc_id, -1))
    return run

def load_qrels(path):
    logging.info('loading qrels...')
    run = {}
    with open(path, 'r') as fqrels:
        for line in tqdm(fqrels):
            query_id, _, doc_id, rel = line.split()
            query_id = int(query_id)
            doc_id = int(doc_id)
            rel = int(rel.rstrip('\n'))
            if query_id not in run:
                run[query_id] = []
            run[query_id].append((doc_id, rel))
    return run


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Create T5 input for Fair Trec 2022 queries.')
    parser.add_argument('--topics', required=True,
                        help='Topics file (queries)')
    parser.add_argument('--run', required=False, default='',
                        help='TREC run file')
    parser.add_argument('--qrel', required=False, default='',
                        help='qrels file')
    parser.add_argument('--corpus', type=str, required=True)
    parser.add_argument('--output_t5_texts', required=True, default='',
                        help='output file')
    parser.add_argument('--output_t5_ids', required=True, default='',
                        help='output id file')
    parser.add_argument('--stride', type=int, default=5, help='')
    parser.add_argument('--max_length', type=int, default=10, help='')
    parser.add_argument('--only-first-segment', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose')
    args = parser.parse_args()

    if args.run == '' and args.qrel == '':
        parser.error("at least one of --run, --qrel is required")
        quit()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logging.info('starting...')

    queries = load_queries(args.topics)
    run = {}
    if args.run != '':
        run = load_run(args.run)
    elif args.qrel != '':
        run = load_qrels(args.qrel)
    assert len(run) > 0
    corpus = load_corpus(args.corpus)

    logging.info('creating t5 inputs...')
    nlp = spacy.blank("en")
    nlp.add_pipe("sentencizer")
    n_docs = 0
    n_segments = 0
    n_no_segments = 0
    n_no_content = 0
    n_not_found = 0
    set_ids = set()
    with open(args.output_t5_texts, 'w') as fout_t5_texts,  \
            open(args.output_t5_ids, 'w') as fout_t5_ids:
        for (query_id, docs) in tqdm(run.items()):
            query, keywords = queries[query_id]
            for doc_id, rel in docs:
                if doc_id not in corpus:
                    #print(f'Doc id not found: {doc_id}')
                    n_not_found += 1
                    continue
                contents = corpus[doc_id]
                n_docs += 1
                passage_text = contents['contents']
                doc_title = contents['title']

                # Remove any duplicated spaces or line breaks.
                passage_text = ' '.join(passage_text.split())

                doc = nlp(passage_text)
                sentences = [sent.text.strip() for sent in doc.sents]
                doc_title = ' '.join(doc_title.split())
                if not sentences:
                    n_no_segments += 1
                    sentences = [""]
                for i in range(0, len(sentences), args.stride):
                    segment = ' '.join(
                        sentences[i:i + args.max_length]).strip()
                    if doc_title:
                        if doc_title.startswith('.'):
                            doc_title = doc_title[1:]

                        if i == 0:
                            segment = '. '.join([doc_title, segment[len(doc_title):]])
                        else:
                            segment = '. '.join([doc_title, segment])

                    # Remove starting #'s as T5 skips those lines by default.
                    segment = re.sub(r'^#*', '', segment)

                    fout_t5_ids.write(f'{query_id}\t{doc_id}\t{i}\n')

                    if keywords == "":
                        relevant = ''
                        if rel == 1:
                            relevant = '\ttrue'
                        elif rel == 0:
                            relevant = '\tfalse'
                        assert args.qrel != '' and relevant != ''
                        fout_t5_texts.write(
                            f'Query: {query} Document: {segment} Relevant:{relevant}\n')
                    else:
                        relevant = ''
                        if rel == 1:
                            relevant = '\ttrue'
                        elif rel == 0:
                            relevant = '\tfalse'
                        assert args.qrel != '' and relevant != ''
                        fout_t5_texts.write(
                            f'Query: {query} Keywords: {keywords} Document: {segment} Relevant:{relevant}\n')
                    n_segments += 1
                    if i + args.max_length >= len(sentences):
                        break
                    if args.only_first_segment:
                        break

    logging.info(f'{n_no_content} examples with only title')
    logging.info(f'{n_not_found} examples not found')
    logging.info(f'Wrote {n_segments} segments from {n_docs} docs.')
    logging.info(f'There were {n_no_segments} docs without segments/sentences.')
    logging.info('Done')
