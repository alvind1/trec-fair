#  Generating qrels for TREC Fair 2021

Different types of input  
- train qrels
- train qrels + random negative samples
- train qrels + run negative samples
- eval qrels
- eval qrels + random negative samples

## Train Data

Train qrels
```bash
python convert_trec_fair_2021_reldocs_to_qrels.py \
  --input topics-and-qrels/raw/trecfair2021.train.topics.json \
  --output topics-and-qrels/trecfair2021.train.qrels.txt
```
There should be 2,185,446 qrels generated.

Train qrels with random negative sampling
```bash
python convert_trec_fair_2021_reldocs_to_qrels.py \
  --input topics-and-qrels/raw/trecfair2021.train.topics.json \
  --random-negative-samples \
  --docIDs topics-and-qrels/trecfair2021.docids.txt \
  --output topics-and-qrels/trecfair2021.train.qrels_w_random_negative_samples.txt
```
There should be 4,370,892 qrels generated.

Train qrels with run negative sampling
```bash
python convert_trec_fair_2021_reldocs_to_qrels.py \
  --input topics-and-qrels/raw/trecfair2021.train.topics.json \
  --run-negative-samples \
  --docIDs topics-and-qrels/trecfair2021.docids.txt \
  --run runs/trecfair2021.train.run100000.text_corpus.bm25.txt \
  --output topics-and-qrels/trecfair2021.train.qrels_w_run_negative_samples.txt
```
There should be 3,438,218 qrels generated.

Check that each train qrel generation is valid with
```bash
./trec_eval -c -mrecall.1000 -mP.10 -mndcg -mndcg_cut.10 topics-and-qrels/trecfair2021.train.qrels***.txt runs/trecfair2021.train.run1000.text_corpus.bm25.txt
```

Output should be
```
P_10                  	all	0.6316
recall_1000           	all	0.0538
ndcg                  	all	0.0740
ndcg_cut_10           	all	0.6245
```

## Eval Data

Eval qrels
```bash
python convert_trec_fair_2021_reldocs_to_qrels.py \
  --input topics-and-qrels/raw/trecfair2021.eval.reldocs.json \
  --output topics-and-qrels/trecfair2021.eval.qrels.txt
```
There should be 13,631 qrels generated.

Eval qrels with random negatives sampling
```bash
python convert_trec_fair_2021_reldocs_to_qrels.py \
  --input topics-and-qrels/raw/trecfair2021.eval.reldocs.json \
  --random-negative-samples \
  --docIDs topics-and-qrels/trecfair2021.docids.txt \
  --output topics-and-qrels/trecfair2021.eval.qrels_w_random_negative_samples.txt
```
There should be 27,262 qrels generated.

Check that each eval qrel generation is valid with
```bash
./trec_eval -c -mrecall.1000 -mP.10 -mndcg -mndcg_cut.10 topics-and-qrels/trecfair2021.eval.qrels***.txt runs/trecfair2021.eval.run1000.text_corpus.bm25.txt
```

Output should be
```
P_10                  	all	0.7714
recall_1000           	all	0.5920
ndcg                  	all	0.5545
ndcg_cut_10           	all	0.7932
```
