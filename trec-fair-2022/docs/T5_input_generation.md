# Generating T5 input for TREC Fair 2022

Types
- train qrels
- train qrels with random negative samples
- train qrels with run negative samples

## Output
The files generated should take the format  
`{year}.{dataset}.t5input.{corpus type}.{run type/qrels<negative sampling specification>}.txt`

`year`
- trecfair2021
- trecfair2022

`dataset`
- train

`corpus type`
- {plain,text,html}_corpus{_ignore_duplicates,_merge_duplicates}

`run type/qrels_<negative sampling specification>`
- qrels_w_random_negative_samples if we are generating input for training
- qrels_w_run_negative_samples if we are generating input for training
- bm25 otherwise

## Train Data

Training qrels
```bash
python create_trec_fair_2022_monot5_input.py \
  --corpus collections/plain-ignore-duplicates/trecfair2022.plain_ignore_duplicates.jsonl \
  --topics topics-and-qrels/trecfair2022.train.queries.tsv \
  --qrel topics-and-qrels/trecfair2022.train.qrels.txt \
  --output_t5_texts t5_inputs/trecfair2022.train.t5input.plain_corpus_ignore_duplicates.qrels.txt \
  --output_t5_ids t5_inputs/trecfair2022.train.t5input.plain_corpus_ignore_duplicates.qrels.ids.txt \
  --stride 4 \
  --max_length 8
```

Training qrels with random negative samples
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

Training qrels with run negative samples
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
