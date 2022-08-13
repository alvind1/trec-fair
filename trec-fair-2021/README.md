# TREC Fair 2021

This is a folder that holds scripts for preprocessing data used for TREC Fair 2021.  
In 2021, the corpus had 6280328 articles.

# Repo Organization
Script naming format: snake case

File naming format: 
{trecfair2021,trecfair2022}.{train,eval}.{file type (ex. qrel)}.{additional format (ex. bm25)}.{file extension}

# Get data

```bash
wget https://data.boisestate.edu/library/Ekstrand-2021/TRECFairRanking2021/trec_topics.json.gz -O topics-and-qrels/raw/trecfair2021.train.topics.json.gz
wget https://data.boisestate.edu/library/Ekstrand-2021/TRECFairRanking2021/eval-topics.json.gz -O tools/topics-and-qrels/raw/trecfair2021.eval.topics.json.gz
wget https://trec.nist.gov/data/fair/2021-eval-topics-with-qrels.json.gz -O topics-and-qrels/raw/trecfair2021.eval.reldocs.json.gz
gzip -d tools/topics-and-qrels/raw/trecfair2021*.json.gz
```

# Prepare topics

## Train
Convert raw train topics to queries of the form `query_id     topic+keywords`
```bash
python convert_trec_fair_2021_queries_to_tsv.py \
  --input topics-and-qrels/raw/trecfair2021.train.topics.json \
  --output topics-and-qrels/trecfair2021.train.queries.tsv
```

## Eval
Convert raw eval topics to queries of the form `queri_id topic+keywords`
```bash
python convert_trec_fair_2021_queries_to_tsv.py \
  --input topics-and-qrels/raw/trecfair2021.eval.topics.json \
  --output topics-and-qrels/trecfair2021.eval.queries.tsv
```

# Baseline runs

## Train

Normal run only needs 1000 hits
```bash
python -m pyserini.search.lucene \
  --index indexes/trec-fair-2021-text \
  --topics topics-and-qrels/trecfair2021.train.queries.tsv \
  --output runs/trecfair2021.train.run1000.text_corpus.bm25.txt \
  --bm25 \
  --hits 1000
```

To perform negative sampling using runs, we need 100,000 hits
```bash
python -m pyserini.search.lucene \
  --index indexes/trec-fair-2021-text \
  --topics topics-and-qrels/trecfair2021.train.queries.tsv \
  --output runs/trecfair2021.train.run100000.text_corpus.bm25.txt \
  --bm25 \
  --hits 100000
```

## Eval

```bash
python -m pyserini.search.lucene \
  --index indexes/trec-fair-2021-text \
  --topics topics-and-qrels/trecfair2021.eval.queries.tsv \
  --output runs/trecfair2021.eval.run1000.text_corpus.bm25.txt \
  --bm25 \
  --hits 1000
```

# Prepare qrels

To perform negative sampling, we need to get the docIDs
```bash
python get_trec_fair_2021_doc_ids.py \
  --input collections/Text/trecfair2021.text.jsonl \
  --output topics-and-qrels/trecfair2021.docids.txt
```

## Train
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

Quick check with `trec_eval` tool
Setup a symbolic link to `tools/eval/trec_eval.9.0.4/trec_eval` in pyseirni
```bash
./trec_eval -c -mrecall.1000 -mP.10 -mndcg -mndcg_cut.10 topics-and-qrels/trecfair2021.train.qrels.txt runs/trecfair2021.train.run1000.text_corpus.bm25.txt
```

The output should be
```bash
P_10                  	all	0.6316
recall_1000           	all	0.0538
ndcg                  	all	0.0740
ndcg_cut_10           	all	0.6245
```

## Eval
Convert eval reldocs to qrels of the form `query_id 0 doc_id 1`
```bash
python convert_trec_fair_2021_reldocs_to_qrels.py \
  --input topics-and-qrels/raw/trecfair2021.eval.reldocs.json \
  --output topics-and-qrels/trecfair2021.eval.qrels.txt
```

Quick with `trec_eval`
```bash
./trec_eval -c -mrecall.1000 -mP.10 -mndcg -mndcg_cut.10 topics-and-qrels/trecfair2021.eval.qrels.txt runs/trecfair2021.eval.run1000.text_corpus.bm25.txt
```

The output should be
```bash
P_10                  	all	0.7714
recall_1000           	all	0.5920
ndcg                  	all	0.5545
ndcg_cut_10           	all	0.7932
```

# Preparing input for T5

## Train

Creating T5 input from qrels with run negative samples
```bash
python create_trec_fair_2021_monot5_input.py \
  --corpus collections/Text/trecfair2021.text.jsonl \
  --topics topics-and-qrels/trecfair2021.train.queries.tsv \
  --qrel topics-and-qrels/trecfair2021.train.qrels_w_run_negative_samples.txt \
  --output_t5_texts t5_inputs/trecfair2021.train.t5input.text_corpus.bm25.qrels_w_run_negative_samples.txt \
  --output_t5_ids t5_inputs/trecfair2021.train.t5input.text_corpus.bm25.qrels_w_run_negative_samples.ids.txt \
  --stride 4 \
  --max_length 8
```

Create T5 input with only the first segment
```bash
python create_trec_fair_2021_monot5_input.py \
  --corpus collections/Text/trecfair2021.text.jsonl \
  --topics topics-and-qrels/trecfair2021.train.queries.tsv \
  --qrel topics-and-qrels/trecfair2021.train.qrels_w_run_negative_samples.txt \
  --output_t5_texts t5_inputs/trecfair2021.train.t5input.text_corpus.bm25.qrels_w_run_negative_samples.first_segment.txt \
  --output_t5_ids t5_inputs/trecfair2021.train.t5input.text_corpus.bm25.qrels_w_run_negative_samples.first_segment.ids.txt \
  --stride 4 \
  --max_length 8 \
  --only-first-segment
```

Create T5 input from qrels with random negative samples
```bash
python create_trec_fair_2021_monot5_input.py \
  --corpus collections/Text/trecfair2021.text.jsonl \
  --topics topics-and-qrels/trecfair2021.train.queries.tsv \
  --qrel topics-and-qrels/trecfair2021.train.qrels_w_random_negative_samples.txt \
  --output_t5_texts t5_inputs/trecfair2021.train.t5input.text_corpus.bm25.qrels_w_random_negative_samples.txt \
  --output_t5_ids t5_inputs/trecfair2021.train.t5input.text_corpus.bm25.qrels_w_random_negative_samples.ids.txt \
  --stride 4 \
  --max_length 8
```

## Eval

Create T5 input from BM25 run
```bash
python create_trec_fair_2021_monot5_input.py \
  --corpus collections/Text/trecfair2021.text.json \
  --topics topics-and-qrels/raw/trecfair2021.eval.queries.tsv \
  --run runs/trecfair2021.eval.run1000.text_corpus.bm25.txt \
  --output_t5_texts t5_inputs/trecfair2021.eval.t5input.text_corpus.bm25.txt \
  --output_t5_ids t5_inputs/trecfair2021.eval.t5input.text_corpus.bm25.ids.txt \
  --stride 4 \
  --max_length 8
```

# Evaluating runs

We will be using [trec fair 2021 evaluator](https://github.com/fair-trec/trec2021-fair-public) to judge our runs.  
It expects runs to be of the form `query_id\tdoc_id`

We can convert Anserini runs of the form `query_id Q0 doc_id _ _ Anserini` to `query_id\tdoc_id`
```bash
python convert_anserini_runs_for_official_eval.py \
  --input runs/trecfair2021.eval.run1000.text_corpus.bm25.txt \
  --output runs/ \
  --task 1
```

Then, we can get the official evaluation stored in results/
```bash
conda activate wptrec
bash trec_fair_2021_run_eval.sh ../../trec2021-fair-public/ runs/trecfair2021.eval.run1000.text_corpus.bm25.eval_format.txt
```

To analyze the results
```bash
python analyze_results.py \
  --files results/trecfair2021.eval.run1000.text_corpus.bm25.eval_format.txt.tsv \
  --output-file results/task1_summary.tsv \
  --task 1
```

The output should be 
```bash
Filename:  trecfair2021
Mean nDCG:  0.1897162787844332
Mean AWRF:  0.6394697380199352
Mean Score:  0.12017384821260774
```
