# TriviaHG: A Dataset for Automatic Hint Generation for Factoid
In this repository, we prepared some folders about the results and experiments of the paper "TriviaHG: A Dataset for Automatic Hint Generation for Factoid". In the following, we describe the materials of this repository:

## Dataset
In this folder, there are training, validation, and test sets of TriviaHG dataset. In the following table, we show the statistics of the dataset.

|                   | Training | Validation | Test |
| ----------------- | -------- | ---------- | ---- |
| Num. of Questions | 14645    | 1000       | 1000 |
| Num. of Hints     | 140973   | 9638       | 9619 |

## Human Evaluation- Answering
In this folder, there are the excel files that we asked from 6 humans to answer their questions using 2791 hints. For each person, there are 10 excel files which every file contains 10 questions. In the table below, B,F, and V refer to Bing, Finetuned LLaMA 7b and LLaMA 7b vanilla.

|  Question Type  |  Hard-B  |  Hard-F  |  Hard-V  |  Medium-B  |  Medium-F  |  Medium-V  |  Easy-B  |  Easy-F  |  Easy-V  |
|-----------------|----------|----------|----------|------------|------------|------------|----------|----------|----------|
|      ENTITY     |  5 / 9   |  5 / 9   |  4 / 9   |   8 / 8    |   6 / 8    |   4 / 8    |  8 / 8   |  8 / 8   |  6 / 8   |
|      HUMAN      |  2 / 9   |  0 / 9   |  0 / 9   |   5 / 8    |   1 / 8    |   0 / 8    |  6 / 8   |  6 / 8   |  4 / 8   |
|     LOCATION    |  0 / 9   |  0 / 9   |  0 / 9   |   7 / 8    |   5 / 8    |   2 / 8    |  7 / 8   |  6 / 8   |  4 / 8   |
|      OTHER      |  3 / 9   |  2 / 9   |  0 / 9   |   5 / 8    |   2 / 8    |   0 / 8    |  8 / 8   |  7 / 8   |  7 / 8   |

## Human Evaluation - Quality
In this folder, there are 10 excel files that include the human annotation values based on the relevance, readability, ambiguity, convergence, and familiarity quality attributes for 2791 hints. In the table below, there are the average of each quality feature.


|       Method      |    Match     | Readability  |  Ambiguity   | Convergence  | Familiarity  |
|-------------------|--------------|--------------|--------------|--------------|--------------|
|        Bing       | 4.09 (81.8%) | 4.67 (93.4%) | 1.51 (30.2%) | 2.23 (44.6%) | 2.47 (49.4%) |
| LLaMA - Finetuned | 4.01 (80.2%) | 4.7 (94.0%)  | 1.56 (31.2%) | 2.22 (44.4%) | 2.41 (48.2%) |
|  LLaMA - Vanilla  | 3.64 (72.8%) | 4.47 (89.4%) | 1.87 (37.4%) | 2.21 (44.2%) | 2.02 (40.4%) |
