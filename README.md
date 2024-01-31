# TriviaHG: A Dataset for Automatic Hint Generation for Factoid

This repository contains folders pertaining to the results and experiments discussed in the paper "TriviaHG: A Dataset for Automatic Hint Generation for Factoid". Below, we provide details regarding the materials available in this repository:

## Dataset

Within this folder, you will find the training, validation, and test sets of the TriviaHG dataset. Refer to the table below for the dataset statistics:

|                   | Training | Validation | Test  |
| ----------------- | -------- | ---------- | ----- |
| Num. of Questions | 14,645   | 1,000      | 1,000 |
| Num. of Hints     | 140,973  | 9,638      | 9,619 |

## Human Evaluation - Answering

This folder contains Excel files used to solicit responses from six human participants. Each participant received ten Excel files, with each file comprising ten questions. The table below represents the types of questions and the corresponding statistics from each participant.

|  Question Type  |  Hard-B  |  Hard-F  |  Hard-V  |  Medium-B  |  Medium-F  |  Medium-V  |  Easy-B  |  Easy-F  |  Easy-V  |
|-----------------|----------|----------|----------|------------|------------|------------|----------|----------|----------|
|      ENTITY     |  5 / 9   |  5 / 9   |  4 / 9   |   8 / 8    |   6 / 8    |   4 / 8    |  8 / 8   |  8 / 8   |  6 / 8   |
|      HUMAN      |  2 / 9   |  0 / 9   |  0 / 9   |   5 / 8    |   1 / 8    |   0 / 8    |  6 / 8   |  6 / 8   |  4 / 8   |
|     LOCATION    |  0 / 9   |  0 / 9   |  0 / 9   |   7 / 8    |   5 / 8    |   2 / 8    |  7 / 8   |  6 / 8   |  4 / 8   |
|      OTHER      |  3 / 9   |  2 / 9   |  0 / 9   |   5 / 8    |   2 / 8    |   0 / 8    |  8 / 8   |  7 / 8   |  7 / 8   |

## Human Evaluation - Quality

This folder contains ten Excel files including human annotation values for relevance, readability, ambiguity, convergence, and familiarity quality attributes for 2,791 hints. The table below presents the average scores for each quality attribute.

|       Method      |    Match     | Readability  |  Ambiguity   | Convergence  | Familiarity  |
|-------------------|--------------|--------------|--------------|--------------|--------------|
|        Bing       | 4.09 (81.8%) | 4.67 (93.4%) | 1.51 (30.2%) | 2.23 (44.6%) | 2.47 (49.4%) |
| LLaMA - Finetuned | 4.01 (80.2%) | 4.7 (94.0%)  | 1.56 (31.2%) | 2.22 (44.4%) | 2.41 (48.2%) |
|  LLaMA - Vanilla  | 3.64 (72.8%) | 4.47 (89.4%) | 1.87 (37.4%) | 2.21 (44.2%) | 2.02 (40.4%) |

## Model Performance

In this folder, you will find the generated hints and their evaluation values for convergence and familiarity quality attributes. Refer to the table below for the results across different models.

|        Model        | Convergence | Familiarity |
|---------------------|-------------|-------------|
|   LLaMA_7b_Vanilla  |    0.307    |    0.833    |
|  LLaMA_13b_Vanilla  |    0.350    |    0.929    |
|  LLaMA_7b_Finetuned |    0.400    |    0.890    | 
| LLaMA_13b_Finetuned |    0.410    |    0.881    |
|       GPT_3.5       |    0.425    |    0.941    |
|  LLaMA_70b_Vanilla  |    0.438    |    0.911    |
|     WizardLM_70b    |    0.446    |    0.942    |
|        Gemini       |    0.455    |    0.911    |
| LLaMA_70b_Finetuned |    0.494    |    0.862    |
|     GPT_4_turbo     |    0.525    |    0.875    |
|         Bing        |    0.540    |    0.946    |

## Entities

This folder contains a JSON file comprising 50,000 entities used in IQR to find Q1 and Q3 for normalization.
