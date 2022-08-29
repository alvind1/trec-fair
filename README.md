# TREC Fair

This repo holds scripts used to process data for TREC Fair 2021, 2022.

# Prepare topics

2021 Ex.
```bash
python convert_trec_fair_queries_to_tsv.py \
  --input topics-and-qrels/trec-fair-2021/raw/trecfair2021.train.topics.json \
  --output topics-and-qrels/trec-fair-2021/trecfair2021.train.queries.tsv

python convert_trec_fair_queries_to_tsv.py \
  --input topics-and-qrels/trec-fair-2021/raw/trecfair2021.eval.topics.json \
  --output topics-and-qrels/trec-fair-2021/trecfair2021.eval.queries.tsv
```

2022 Ex.
```bash
python convert_trec_fair_queries_to_tsv.py \
  --input topics-and-qrels/trec-fair-2022/raw/trecfair2022.train.topics_meta.jsonl \
  --output topics-and-qrels/trec-fair-2022/trecfair2022.train.queries.tsv

python convert_trec_fair_queries_to_tsv.py \
  --input topics-and-qrels/trec-fair-2022/raw/trecfair2022.eval.topics.jsonl \
  --output topics-and-qrels/trec-fair-2022/trecfair2022.eval.queries.tsv \
  --eval
```

# Get Doc IDs

2021 Ex.
```bash
python get_trec_fair_doc_ids.py \
  --input collections/trec-fair-2021/text/trecfair2021.text.jsonl \
  --output topics-and-qrels/trec-fair-2021/trecfair2021.docids.txt
```

2022 Ex.
```bash
python get_trec_fair_doc_ids.py \
  --input collections/trec-fair-2022/plain/trecfair2022.plain.jsonl \
  --output topics-and-qrels/trec-fair-2022/trecfair2022.docids.txt
```

# Prepare qrels

Convert train reldocs to qrels of the form `query_id 0 doc_id relevant`

2021 Ex.
```bash
python convert_trec_fair_reldocs_to_qrels.py \
  --input topics-and-qrels/trec-fair-2021/raw/trecfair2021.train.topics.json \
  --output topics-and-qrels/trec-fair-2021/trecfair2021.train.qrels.txt

python convert_trec_fair_reldocs_to_qrels.py \
  --input topics-and-qrels/trec-fair-2021/raw/trecfair2021.train.topics.json \
  --random-negative-samples \
  --docIDs topics-and-qrels/trec-fair-2021/trecfair2021.docids.txt \
  --output topics-and-qrels/trec-fair-2021/trecfair2021.train.qrels_w_random_negative_samples.txt

python convert_trec_fair_reldocs_to_qrels.py \
  --input topics-and-qrels/trec-fair-2021/raw/trecfair2021.train.topics.json \
  --run-negative-samples \
  --docIDs topics-and-qrels/trec-fair-2021/trecfair2021.docids.txt \
  --run runs/trec-fair-2021/trecfair2021.train.run100000.text_corpus.bm25.txt \
  --output topics-and-qrels/trec-fair-2021/trecfair2021.train.qrels_w_run_negative_samples.txt
```

2022 Ex.
```bash
python convert_trec_fair_reldocs_to_qrels.py \
  --input topics-and-qrels/trec-fair-2022/raw/trecfair2022.train.topics_meta.jsonl \
  --output topics-and-qrels/trec-fair-2022/trecfair2022.train.qrels.txt

python convert_trec_fair_reldocs_to_qrels.py \
  --input topics-and-qrels/trec-fair-2022/raw/trecfair2022.train.topics_meta.jsonl \
  --random-negative-samples \
  --docIDs topics-and-qrels/trec-fair-2022/trecfair2022.docids.txt \
  --output topics-and-qrels/trec-fair-2022/trecfair2022.train.qrels_w_random_negative_samples.txt

python convert_trec_fair_reldocs_to_qrels.py \
  --input topics-and-qrels/trec-fair-2022/raw/trecfair2022.train.topics_meta.jsonl \
  --run-negative-samples \
  --docIDs topics-and-qrels/trec-fair-2022/trecfair2022.docids.txt \
  --run runs/trec-fair-2022/trecfair2022.train.run100000.plain_corpus_ignore_duplicates.bm25.txt \
  --output topics-and-qrels/trec-fair-2022/trecfair2022.train.qrels_w_run_negative_samples.txt
```

# Preparing T5 input

2021 Ex.
```bash
python create_trec_fair_monot5_input.py \
  --corpus collections/trec-fair-2021/text/trecfair2021.text.jsonl \
  --topics topics-and-qrels/trec-fair-2021/trecfair2021.train.queries.tsv \
  --qrel topics-and-qrels/trec-fair-2021/trecfair2021.train.qrels.txt \
  --output_t5_texts t5_inputs/trec-fair-2021/trecfair2021.train.t5input.text_corpus.qrels.txt \
  --output_t5_ids t5_inputs/trec-fair-2021/trecfair2021.train.t5input.text_corpus.qrels.ids.txt \
  --stride 4 \
  --max_length 8
```

2022 Ex.
```bash
python create_trec_fair_monot5_input.py \
  --corpus collections/trec-fair-2022/plain-ignore-duplicates/trecfair2022.plain_ignore_duplicates.jsonl \
  --topics topics-and-qrels/trec-fair-2022/trecfair2022.train.queries.tsv \
  --qrel topics-and-qrels/trec-fair-2022/trecfair2022.train.qrels.txt \
  --output_t5_texts t5_inputs/trec-fair-2022/trecfair2022.train.t5input.plain_corpus_ignore_duplicates.qrels.txt \
  --output_t5_ids t5_inputs/trec-fair-2022/trecfair2022.train.t5input.plain_corpus_ignore_duplicates.qrels.ids.txt \
  --stride 4 \
  --max_length 8
```

## Selecting only true/false examples

2021 Ex.
```bash
python select_truefalse_examples_trec_fair_t5.py \
  --t5-input t5_inputs/trec-fair-2021/trecfair2021.train.t5input.text_corpus.qrels_w_random_negative_samples.txt \
  --t5-ids-input t5_inputs/trec-fair-2021/trecfair2021.train.t5input.text_corpus.qrels_w_random_negative_samples.ids.txt \
  --output t5_inputs/trec-fair-2021/trecfair2021.train.t5input.text_corpus.qrels_only_negatives.txt \
  --output-ids t5_inputs/trec-fair-2021/trecfair2021.train.t5input.text_corpus.qrels_only_negatives.ids.txt \
  --relevance false

python select_truefalse_examples_trec_fair_t5.py \
  --t5-input t5_inputs/trec-fair-2021/trecfair2021.eval.t5input.text_corpus.qrels_w_random_negative_samples.txt \
  --t5-ids-input t5_inputs/trec-fair-2021/trecfair2021.eval.t5input.text_corpus.qrels_w_random_negative_samples.ids.txt \
  --output t5_inputs/trec-fair-2021/trecfair2021.eval.t5input.text_corpus.qrels_only_negatives.txt \
  --output-ids t5_inputs/trec-fair-2021/trecfair2021.eval.t5input.text_corpus.qrels_only_negatives.ids.txt \
  --relevance false
```

2022 Ex.
```bash
python select_truefalse_examples_trec_fair_t5.py \
  --t5-input t5_inputs/trec-fair-2022/trecfair2022.train.t5input.plain_corpus_ignore_duplicates.qrels_w_random_negative_samples.txt \
  --t5-ids-input t5_inputs/trec-fair-2022/trecfair2022.train.t5input.plain_corpus_ignore_duplicates.qrels_w_random_negative_samples.ids.txt \
  --output t5_inputs/trec-fair-2022/trecfair2022.train.t5input.plain_corpus_ignore_duplicates.qrels_only_negatives.txt \
  --output-ids t5_inputs/trec-fair-2022/trecfair2022.train.t5input.plain_corpus_ignore_duplicates.qrels_only_negatives.ids.txt \
  --relevance false
```

## Selecting best segments for training

2021 Ex.
```bash
python select_best_segment_trec_fair_t5.py \
  --t5-predictions t5_predictions/trec-fair-2021/trecfair2021.train.t5input.qrels.pred \
  --t5-input t5_inputs/trec-fair-2021/trecfair2021.train.t5input.text_corpus.bm25.qrels_no_negatives.txt \
  --t5-ids-input t5_inputs/trec-fair-2021/trecfair2021.train.t5input.text_corpus.bm25.qrels_no_negatives.ids.txt \
  --negative-segments t5_inputs/trec-fair-2021/trecfair2021.train.t5input.text_corpus.qrels_only_negatives.txt \
  --negative-ids t5_inputs/trec-fair-2021/trecfair2021.train.t5input.text_corpus.qrels_only_negatives.ids.txt \
  --t5-output t5_inputs/trec-fair-2021/trecfair2021.train.t5input.text_corpus.best_segments_w_random_negatives.txt \
  --t5-ids-output t5_inputs/trec-fair-2021/trecfair2021.train.t5input.text_corpus.best_segments_w_random_negatives.ids.txt

python select_best_segment_trec_fair_t5.py \
  --t5-predictions t5_predictions/trec-fair-2021/trecfair2021.eval.t5input.qrels.pred \
  --t5-input t5_inputs/trec-fair-2021/trecfair2021.eval.t5input.text_corpus.qrels_no_negatives.txt \
  --t5-ids-input t5_inputs/trec-fair-2021/trecfair2021.eval.t5input.text_corpus.qrels_no_negatives.ids.txt \
  --negative-segments t5_inputs/trec-fair-2021/trecfair2021.eval.t5input.text_corpus.qrels_only_negatives.txt \
  --negative-ids t5_inputs/trec-fair-2021/trecfair2021.eval.t5input.text_corpus.qrels_only_negatives.ids.txt \
  --t5-output t5_inputs/trec-fair-2021/trecfair2021.eval.t5input.text_corpus.best_segments_w_random_negatives.txt \
  --t5-ids-output t5_inputs/trec-fair-2021/trecfair2021.eval.t5input.text_corpus.best_segments_w_random_negatives.ids.txt
```

2022 Ex.
```bash
python select_best_segment_trec_fair_t5.py \
  --t5-predictions t5_predictions/trec-fair-2022/trecfair2022.train.t5input.qrels.pred \
  --t5-input t5_inputs/trec-fair-2022/trecfair2022.train.t5input.plain_corpus_ignore_duplicates.qrels_no_negatives.txt \
  --t5-ids-input t5_inputs/trec-fair-2022/trecfair2022.train.t5input.plain_corpus_ignore_duplicates.qrels_no_negatives.ids.txt \
  --negative-segments t5_inputs/trec-fair-2022/trecfair2022.train.t5input.plain_corpus_ignore_duplicates.qrels_only_negatives.txt \
  --negative-ids t5_inputs/trec-fair-2022/trecfair2022.train.t5input.plain_corpus_ignore_duplicates.qrels_only_negatives.ids.txt \
  --t5-output t5_inputs/trec-fair-2022/trecfair2022.train.t5input.plain_corpus_ignore_duplicates.best_segments_w_random_negatives.txt \
  --t5-ids-output t5_inputs/trec-fair-2022/trecfair2022.train.t5input.plain_corpus_ignore_duplicates.best_segments_w_random_negatives.ids.txt
```
