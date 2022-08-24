# TREC Fair 2022

This is a folder that holds scripts for preprocessing data used for TREC Fair 2022.  
In 2022, the corpus had 6475537 articles.

# Repo Organization
Script naming format: snake case

File naming format:
{trecfair2021,trecfair2022}.{train,eval}.{file type (ex. qrel)}.{additional format (ex. bm25)}.{file extension}

# Get data

Download the corpus
```bash
mkdir collections/raw
wget https://data.boisestate.edu/library/Ekstrand/TRECFairRanking/corpus/trec_corpus_20220301_html.json.gz -P collections/raw/trecfair2022.html.json.gz
wget https://data.boisestate.edu/library/Ekstrand/TRECFairRanking/corpus/trec_corpus_20220301_plain.json.gz -P collections/raw/trecfair2022.plain.json.gz
wget https://data.boisestate.edu/library/Ekstrand/TRECFairRanking/corpus/trec_corpus_20220301_text.json.gz -P collections/raw/trecfair2022.text.json.gz

gzip -d collections/raw/*.gz
```

Next, we need to convert the data to indexing format:

```bash
python convert_trec_fair_2022_data_to_jsonl.py \
  --input collections/raw/trecfair2022.plain.json \
  --output collections/plain/trecfair2022.plain.jsonl
```

Because there are duplicate doc_ids for documents with the same subject but with slightly different articles, titles, we may want to convert a collection without duplicates
```bash
python convert_trec_fair_2022_data_to_jsonl.py \
  --input collections/raw/trecfair2022.plain.json \
  --output collections/plain/trecfair2022.plain_ignore_duplicates.jsonl \
  --ignore-duplicates
```

Alternatively, we can also merge duplicated documents together
```bash
python convert_trec_fair_2022_data_to_jsonl.py \
  --input collections/raw/trecfair2022.plain.json \
  --output collections/plain/trecfair2022.plain_merge_duplicates.jsonl \
  --merge-duplicates
```

Download the topics
```bash
wget https://data.boisestate.edu/library/Ekstrand/TRECFairRanking/2022/train_topics_meta.jsonl -O topics-and-qrels/raw/trecfair2022.train.topics_meta.jsonl
wget https://data.boisestate.edu/library/Ekstrand/TRECFairRanking/2022/trec_2022_articles_discrete.json.gz -O topics-and-qrels/raw/trecfair2022.articles_discrete.json.gz
wget https://data.boisestate.edu/library/Ekstrand/TRECFairRanking/2022/trec_2022_train_reldocs.jsonl -O topics-and-qrels/raw/trecfair2022.train_reldocs.jsonl
```

# Index

```bash
python -m pyserini.index.lucene \
  --collection JsonCollection \
  --input collections/plain-ignore-duplicates \
  --index indexes/plain-ignore-duplicates \
  --generator DefaultLuceneDocumentGenerator \
  --threads 9 \
  --storePositions --storeDocvectors --storeRaw
```

```bash
python -m pyserini.index.lucene \
  --collection JsonCollection \
  --input collections/plain-merge-duplicates \
  --index indexes/plain-merge-duplicates \
  --generator DefaultLuceneDocumentGenerator \
  --threads 9 \
  --storePositions --storeDocvectors --storeRaw
```

# Prepare topics

## Train
Convert raw train topics to queries of the form `query_id     topic+keywords`
```bash
python convert_trec_fair_2022_queries_to_tsv.py \
  --input topics-and-qrels/raw/trecfair2022.train.topics_meta.jsonl \
  --output topics-and-qrels/trecfair2022.train.queries.tsv
```

## Eval
Convert raw train topics to queries of the form `query_id     topic+keywords`
```bash
python convert_trec_fair_2022_queries_to_tsv.py \
  --input topics-and-qrels/raw/trecfair2022.eval.topics.jsonl \
  --output topics-and-qrels/trecfair2022.eval.queries.tsv \
  --eval
```

# Baseline runs

## Train

Normal run only needs 500 hits
```bash
python -m pyserini.search.lucene \
  --index indexes/trec-fair-2022-plain-ignore-duplicates\
  --topics topics-and-qrels/trecfair2022.train.queries.tsv \
  --output runs/trecfair2022.train.run500.plain_corpus_ignore_duplicates.bm25.txt \
  --bm25 \
  --hits 500
```

To perform negative sampling using runs, we need 100,000 hits
```bash
python -m pyserini.search.lucene \
  --index indexes/trec-fair-2022-plain-ignore-duplicates\
  --topics topics-and-qrels/trecfair2022.train.queries.tsv \
  --output runs/trecfair2022.train.run100000.plain_corpus_ignore_duplicates.bm25.txt \
  --bm25 \
  --hits 100000
```

## Eval

Normal run only needs 500 hits
```bash
python -m pyserini.search.lucene \
  --index indexes/trec-fair-2022-plain\
  --topics topics-and-qrels/trecfair2022.eval.queries.tsv \
  --output runs/trecfair2022.eval.run500.plain_corpus.bm25.txt \
  --bm25 \
  --hits 500
```

# Prepare qrels

To perform negative sampling, we need to get the docIDs
```bash
python get_trec_fair_2022_doc_ids.py \
  --input collections/plain/trecfair2022.plain.jsonl \
  --output topics-and-qrels/trecfair2022.docids.txt
```

## Train
Convert train reldocs to qrels of the form `query_id 0 doc_id relevant`

```bash
python convert_trec_fair_2022_reldocs_to_qrels.py \
  --input topics-and-qrels/raw/trecfair2022.train.topics_meta.jsonl \
  --output topics-and-qrels/trecfair2022.train.qrels.txt
```

Generate qrels with random negative sampling
```bash
python convert_trec_fair_2022_reldocs_to_qrels.py \
  --input topics-and-qrels/raw/trecfair2022.train.topics_meta.jsonl \
  --output topics-and-qrels/trecfair2022.train.qrels_w_random_negative_samples.txt \
  --random-negative-samples \
  --docIDs topics-and-qrels/trecfair2022.docids.txt
```

Generate qrels with negative sampling from runs
```bash
python convert_trec_fair_2022_reldocs_to_qrels.py \
  --input topics-and-qrels/raw/trecfair2022.train.topics_meta.jsonl \
  --output topics-and-qrels/trecfair2022.train.qrels_w_run_negative_samples.txt \
  --run-negative-samples \
  --docIDs topics-and-qrels/trecfair2022.docids.txt \
  --run runs/trecfair2022.train.run100000.plain_corpus_ignore_duplicates.bm25.txt
```

Quick check with trec_eval tool   
Setup a symbolic link to `tools/eval/trec_eval.9.0.4/trec_eval` in pyseirni
```bash
./trec_eval -c -mrecall.500 -mP.10 -mndcg -mndcg_cut.10 topics-and-qrels/trecfair2022.train.qrels.txt runs/trecfair2022.train.run500.plain_corpus.bm25.txt
```

The output should be
```bash
P_10                  	all	0.6739
recall_500            	all	0.0138
ndcg                  	all	0.0241
ndcg_cut_10           	all	0.6827
```

## Eval

qrels for TREC Fair 2022 eval has not come out yet.

# Preparing input for T5

## Train
Creating T5 input from qrels with run negative samples

```bash
python create_trec_fair_2022_monot5_input.py \
  --corpus collections/plain-ignore-duplicates/trecfair2022.plain_ignore_duplicates.jsonl \
  --topics topics-and-qrels/trecfair2022.train.queries.tsv \
  --qrel topics-and-qrels/trecfair2022.train.qrels_w_run_negative_samples.txt \
  --output_t5_texts t5_inputs/trecfair2022.train.t5input.plain_corpus_ignore_duplicates.qrels_w_run_negative_samples.txt \
  --output_t5_ids t5_inputs/trecfair2022.train.t5input.plain_corpus_ignore_duplicates.qrels_w_run_negative_samples.ids.txt \
  --stride 4 \
  --max_length 8
```

Create T5 input with only the first segment and run negative samples
```bash
python create_trec_fair_2022_monot5_input.py \
  --corpus collections/plain-ignore-duplicates/trecfair2022.plain_ignore_duplicates.jsonl \
  --topics topics-and-qrels/trecfair2022.train.queries.tsv \
  --qrel topics-and-qrels/trecfair2022.train.qrels_w_run_negative_samples.txt \
  --output_t5_texts t5_inputs/trecfair2022.train.t5input.plain_corpus_ignore_duplicates.qrels_w_run_negative_samples.first_segment.txt \
  --output_t5_ids t5_inputs/trecfair2022.train.t5input.plain_corpus_ignore_duplicates.qrels_w_run_negative_samples.first_segment.ids.txt \
  --stride 4 \
  --max_length 8 \
  --only-first-segment
```

Creating T5 input from qrels with random negative samples
```bash
python create_trec_fair_2022_monot5_input.py \
  --corpus collections/plain-ignore-duplicates/trecfair2022.plain_ignore_duplicates.jsonl \
  --topics topics-and-qrels/trecfair2022.train.queries.tsv \
  --qrel topics-and-qrels/trecfair2022.train.qrels_w_random_negative_samples.txt \
  --output_t5_texts t5_inputs/trecfair2022.train.t5input.plain_corpus_ignore_duplicates.qrels_w_random_negative_samples.txt \
  --output_t5_ids t5_inputs/trecfair2022.train.t5input.plain_corpus_ignore_duplicates.qrels_w_random_negative_samples.ids.txt \
  --stride 4 \
  --max_length 8
```

## Eval

Create T5 input from BM25 run

```bash
python create_trec_fair_2022_monot5_input.py \
  --corpus collections/plain/trecfair2022.plain.json \
  --topics topics-and-qrels/trecfair2022.eval.queries.tsv \
  --run runs/trecfair2022.eval.run500.text_corpus.bm25.txt \
  --output_t5_texts t5_inputs/trecfair2022.eval.t5input.text_corpus.bm25.txt \
  --output_t5_ids t5_inputs/trecfair2022.eval.t5input.text_corpus.bm25.ids.txt \
  --stride 4 \
  --max_length 8
```
