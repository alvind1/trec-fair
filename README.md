# TREC Fair

This repo holds scripts used to process data for TREC Fair 2021, 2022.

# Prepare qrels

Convert train reldocs to qrels of the form `query_id 0 doc_id relevant`

2021 Ex.
```bash
python convert_trec_fair_reldocs_to_qrels.py \
  --input trec-fair-2021/topics-and-qrels/raw/trecfair2021.train.topics.json \
  --output trec-fair-2021/topics-and-qrels/trecfair2021.train.qrels.txt

python convert_trec_fair_reldocs_to_qrels.py \
  --input trec-fair-2021/topics-and-qrels/raw/trecfair2021.train.topics.json \
  --random-negative-samples \
  --docIDs trec-fair-2021/topics-and-qrels/trecfair2021.docids.txt \
  --output trec-fair-2021/topics-and-qrels/trecfair2021.train.qrels_w_random_negative_samples.txt

python convert_trec_fair_reldocs_to_qrels.py \
  --input trec-fair-2021/topics-and-qrels/raw/trecfair2021.train.topics.json \
  --run-negative-samples \
  --docIDs trec-fair-2021/topics-and-qrels/trecfair2021.docids.txt \
  --run trec-fair-2021/runs/trecfair2021.train.run100000.text_corpus.bm25.txt \
  --output trec-fair-2021/topics-and-qrels/trecfair2021.train.qrels_w_run_negative_samples.txt
```

2022 Ex.
```bash
python convert_trec_fair_reldocs_to_qrels.py \
  --input trec-fair-2022/topics-and-qrels/raw/trecfair2022.train.topics_meta.jsonl \
  --output trec-fair-2022/topics-and-qrels/trecfair2022.train.qrels.txt

python convert_trec_fair_reldocs_to_qrels.py \
  --input trec-fair-2022/topics-and-qrels/raw/trecfair2022.train.topics_meta.jsonl \
  --random-negative-samples \
  --docIDs trec-fair-2022/topics-and-qrels/trecfair2022.docids.txt \
  --output trec-fair-2022/topics-and-qrels/trecfair2022.train.qrels_w_random_negative_samples.txt

python convert_trec_fair_reldocs_to_qrels.py \
  --input trec-fair-2022/topics-and-qrels/raw/trecfair2022.train.topics_meta.jsonl \
  --run-negative-samples \
  --docIDs trec-fair-2022/topics-and-qrels/trecfair2022.docids.txt \
  --run trec-fair-2022/runs/trecfair2022.train.run100000.plain_corpus_ignore_duplicates.bm25.txt \
  --output trec-fair-2022/topics-and-qrels/trecfair2022.train.qrels_w_run_negative_samples.txt
```
