import argparse
import collections
import math
import numpy as np
import re
import json
from tqdm import tqdm

parser = argparse.ArgumentParser(
    description='Convert T5 predictions into TREC runs.')
parser.add_argument('--t5-predictions', required=True,
                    help='T5 predictions file')
parser.add_argument('--t5-input', required=True,
                    help='T5 segment input file')
parser.add_argument('--t5-ids-input', required=True,
                    help='File containing query doc id pairs paired with the '
                         'T5\'s predictions file.')
parser.add_argument('--negative-segments', required=True)
parser.add_argument('--negative-ids', required=True)
parser.add_argument('--t5-output', required=True, help='output file')
parser.add_argument('--t5-ids-output', required=True, help='output file')
args = parser.parse_args()


def load_t5_segments(t5_segment_path, t5_ids_path, t5_predictions_path):
    t5_segments = {}
    with open(t5_segment_path, 'r') as f_t5_segments, open(t5_ids_path, 'r')as f_t5_ids, open(t5_predictions_path, 'r') as f_t5_predictions:
        for segment_line in tqdm(f_t5_segments):
            ids_line = f_t5_ids.readline()
            prediction_line = f_t5_predictions.readline()
            query_id, doc_id, segment_ind = ids_line.split('\t')
            _, score = prediction_line.split('\t')
            if query_id not in t5_segments:
                t5_segments[query_id] = {}
            if doc_id not in t5_segments[query_id]:
                t5_segments[query_id][doc_id] = []
            t5_segments[query_id][doc_id].append(
                (score, segment_line, ids_line))
    return t5_segments


def load_negative_segments(negative_segments_path, negative_ids_path):
    negative_segments = {}
    with open(negative_segments_path, 'r') as f_segments, open(negative_ids_path, 'r') as f_ids:
        for segment_line in tqdm(f_segments):
            line = f_ids.readline()
            query_id, doc_id, segment_ind = line.split('\t')
            if query_id not in negative_segments:
                negative_segments[query_id] = []
            negative_segments[query_id].append((segment_line, line))
    return negative_segments


t5_segments = load_t5_segments(
    args.t5_input, args.t5_ids_input, args.t5_predictions)
negative_segments = load_negative_segments(
    args.negative_segments, args.negative_ids)

with open(args.t5_output, 'w') as f_t5_output, open(args.t5_ids_output, 'w') as f_t5_ids_output:
    for query_id, doc_ids in tqdm(t5_segments.items()):
        for doc_id, segments in doc_ids.items():
            mx_score = -1
            mx_score_idx = -1
            for idx, score in enumerate(segments):
                if float(score[0]) > mx_score:
                    mx_score = float(score[0])
                    mx_score_idx = idx
            f_t5_output.write(segments[mx_score_idx][1])
            f_t5_ids_output.write(segments[mx_score_idx][2])
        num_docs = len(doc_ids)
        choices = np.random.choice(len(negative_segments[query_id]), num_docs)
        for choice in choices:
            f_t5_output.write(negative_segments[query_id][choice][0])
            f_t5_ids_output.write(negative_segments[query_id][choice][1])
