# TREC Fair 2021

This is a folder that holds scripts for preprocessing data used for TREC Fair 2021.  
In 2021, the corpus had 6280328 articles.

# Repo Organization
Script naming format: snake case

File naming format: 
{trecfair2021,trecfair2022}.{train,eval}.{file type (ex. qrel)}.{additional format (ex. bm25)}.{file extension}

# Baseline runs
Normal run only needs 1000 hits
```bash
python -m pyserini.search.lucene \
  --index indexes/trec-fair-2021-text \
  --topics topics-and-qrels/trecfair2021.train.queries.tsv \
  --output runs/trecfair2021.train.run1000.text_corpus.bm25.txt \
  --bm25 \
  --hits 1000
```

To negative sample from runs, we need 100,000 hits
```bash
python -m pyserini.search.lucene \
  --index indexes/trec-fair-2021-text \
  --topics topics-and-qrels/trecfair2021.train.queries.tsv \
  --output runs/trecfair2021.train.run100000.text_corpus.bm25.txt \
  --bm25 \
  --hits 100000
```

# Preprocessing topics

To perform negative sampling, we need to get the docIDs
```bash
python get_trec_fair_2021_doc_ids.py \
  --input collections/Text/trecfair2021.text.jsonl \
  --output topics-and-qrels/trecfair2021.docids.txt
```

## Train
Convert raw train topics to queries of the form `query_id     topic + keywords`
```bash
python convert_trec_fair_2021_queries_to_tsv.py \
  --input topics-and-qrels/raw/trecfair2021.train.topics.json \
  --output topics-and-qrels/trecfair2021.train.queries.tsv
```

Convert train reldocs to qrels of the form `query_id 0 doc_id relevant`
```bash
python convert_trec_fair_2021_reldocs_to_qrels.py \
  --input topics-and-qrels/raw/trecfair2021.train.topics.json \
  --output topics-and-qrels/trecfair2021.train.qrels.txt
```

Generate qrels with random negative sampling
```bash
python convert_trec_fair_2021_reldocs_to_qrels.py \
  --input topics-and-qrels/raw/trecfair2021.train.topics.json \
  --output topics-and-qrels/trecfair2021.train.qrels_w_random_negative_samples.txt \
  --random-negative-samples \
  --docIDs topics-and-qrels/trecfair2021.docids.txt
```

Generate qrels with negative sampling from runs
```bash
python convert_trec_fair_2021_reldocs_to_qrels.py \
  --input topics-and-qrels/raw/trecfair2021.train.topics.json \
  --output topics-and-qrels/trecfair2021.train.qrels_w_run_negative_samples.txt \
  --run-negative-samples \
  --docIDs topics-and-qrels/trecfair2021.docids.txt \
  --run runs/trecfair2021.train.run100000.text_corpus.bm25.txt
```

Quick check
```bash
./trec_eval -c -mrecall.1000 -mP.10 -mndcg -mndcg_cut.10 topics-and-qrels/trecfair2021.train.qrels.txt runs/trecfair2021.train.run1000.text_corpus.bm25.txt
```

## Eval

# T5

## Train

Creating T5 input from qrels with run negative samples
```bash
python create_trec_fair_2021_monot5_input.py \
  --corpus collections/Text/trecfair2021.text.jsonl	\
  --topics topics-and-qrels/trecfair2021.train.queries.tsv \
  --qrel topics-and-qrels/trecfair2021.train.qrels_w_run_negative_samples.txt \
  --output_t5_texts t5_inputs/trecfair2021.t5input.text_corpus.bm25.query_keywords_doc_relevant.txt \
  --output_t5_ids t5_inputs/trecfair2021.t5input.text_corpus.bm25.query_keywords_doc_relevant.ids.txt \
  --stride 4 \
  --max_length 8
```

Create T5 input from qrels with random negative samples
```bash
python create_trec_fair_2021_monot5_input.py \
  --corpus collections/Text/trecfair2021.text.jsonl	\
  --topics topics-and-qrels/trecfair2021.train.queries.tsv \
  --qrel topics-and-qrels/trecfair2021.train.qrels_w_random_negative_samples.txt \
  --output_t5_texts t5_inputs/trecfair2021.t5input.text_corpus.bm25.query_keywords_doc_relevant.txt \
  --output_t5_ids t5_inputs/trecfair2021.t5input.text_corpus.bm25.query_keywords_doc_relevant.ids.txt \
  --stride 4 \
  --max_length 8
```

## Eval