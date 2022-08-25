# Generating T5 input for TREC Fair 2021

We want to generating training input using the train and evaluation datasets.

Different types of input  
- train qrels
- train qrels with random negative samples
- train qrels with run negative samples
- eval qrels
- eval qrels with random negative samples

## Training Data

Training qrels
```bash
python create_trec_fair_2021_monot5_input.py \
  --corpus collections/text/trecfair2021.text.jsonl \
  --topics topics-and-qrels/trecfair2021.train.queries.tsv \
  --qrel topics-and-qrels/trecfair2021.train.qrels.txt \
  --output_t5_texts t5_inputs/trecfair2021.train.t5input.text_corpus.bm25.qrels.txt \
  --output_t5_ids t5_inputs/trecfair2021.train.t5input.text_corpus.bm25.qrels.ids.txt \
  --stride 4 \
  --max_length 8
```
There should be 10,642,307 lines.

Training qrels with random negative samples
```bash
python create_trec_fair_2021_monot5_input.py \
  --corpus collections/text/trecfair2021.text.jsonl \
  --topics topics-and-qrels/trecfair2021.train.queries.tsv \
  --qrel topics-and-qrels/trecfair2021.train.qrels_w_random_negative_samples.txt \
  --output_t5_texts t5_inputs/trecfair2021.train.t5input.text_corpus.qrels_w_random_negative_samples.txt \
  --output_t5_ids t5_inputs/trecfair2021.train.t5input.text_corpus.qrels_w_random_negative_samples.ids.txt \
  --stride 4 \
  --max_length 8
```

Training qrels with run negative samples
```bash
python create_trec_fair_2021_monot5_input.py \
  --corpus collections/text/trecfair2021.text.jsonl \
  --topics topics-and-qrels/trecfair2021.train.queries.tsv \
  --qrel topics-and-qrels/trecfair2021.train.qrels_w_run_negative_samples.txt \
  --output_t5_texts t5_inputs/trecfair2021.train.t5input.text_corpus.qrels_w_run_negative_samples.txt \
  --output_t5_ids t5_inputs/trecfair2021.train.t5input.text_corpus.qrels_w_run_negative_samples.ids.txt \
  --stride 4 \
  --max_length 8
```

## Eval Data

Eval qrels
```bash
python create_trec_fair_2021_monot5_input.py \
  --corpus collections/text/trecfair2021.text.jsonl \
  --topics topics-and-qrels/trecfair2021.eval.queries.tsv \
  --qrel topics-and-qrels/trecfair2021.eval.qrels.txt \
  --output_t5_texts t5_inputs/trecfair2021.eval.t5input.text_corpus.qrels.txt \
  --output_t5_ids t5_inputs/trecfair2021.eval.t5input.text_corpus.qrels.ids.txt \
  --stride 4 \
  --max_length 8
```

Eval qrels with random negative samples
```bash
python create_trec_fair_2021_monot5_input.py \
  --corpus collections/text/trecfair2021.text.jsonl \
  --topics topics-and-qrels/trecfair2021.eval.queries.tsv \
  --qrel topics-and-qrels/trecfair2021.eval.qrels_w_random_negative_samples.txt \
  --output_t5_texts t5_inputs/trecfair2021.eval.t5input.text_corpus.qrels_w_random_negative_samples.txt \
  --output_t5_ids t5_inputs/trecfair2021.eval.t5input.text_corpus.qrels_w_random_negative_samples.ids.txt \
  --stride 4 \
  --max_length 8
```
