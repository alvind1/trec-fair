# Generating qrels for TREC Fair 2022

Types
- train qrels
- train qrels with random negative samples
- train qrels with run negative samples

## Output
The files generated should take the format  
`{year}.{dataset}.{qrels<negative sampling specification>}.txt`

`year`
- trecfair2021
- trecfair2022

`dataset`
- train

`qrels_<negative sampling specification>`
- qrels
- qrels_w_random_negative_samples
- qrels_w_run_negative_samples


## Train Data

Train qrels
```bash
python convert_trec_fair_2022_reldocs_to_qrels.py \
  --input topics-and-qrels/raw/trecfair2022.train.topics_meta.jsonl \
  --output topics-and-qrels/trecfair2022.train.qrels.txt
```
There should be 1,974,943 qrels generated.

Train qrels with random negative sampling
```bash
python convert_trec_fair_2022_reldocs_to_qrels.py \
  --input topics-and-qrels/raw/trecfair2022.train.topics_meta.jsonl \
  --random-negative-samples \
  --docIDs topics-and-qrels/trecfair2022.docids.txt \
  --output topics-and-qrels/trecfair2022.train.qrels_w_random_negative_samples.txt
```
There should be 3,949,886 qrels generated.

Train qrels with run negative sampling
```bash
python convert_trec_fair_2022_reldocs_to_qrels.py \
  --input topics-and-qrels/raw/trecfair2022.train.topics_meta.jsonl \
  --run-negative-samples \
  --docIDs topics-and-qrels/trecfair2022.docids.txt \
  --run runs/trecfair2022.train.run100000.plain_corpus_ignore_duplicates.bm25.txt \
  --output topics-and-qrels/trecfair2022.train.qrels_w_run_negative_samples.txt
```
There should be 3,458,088 qrels generated.

Check that each train qrel generation is valid with
```bash
./trec_eval -c -mrecall.500 -mP.10 -mndcg -mndcg_cut.10 topics-and-qrels/trecfair2022.train.qrels<type>.txt runs/trecfair2022.train.run500.plain_corpus.bm25.txt
```

Output should be
```
P_10                  	all	0.6739
recall_500            	all	0.0138
ndcg                  	all	0.0241
ndcg_cut_10           	all	0.6827
```
