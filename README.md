<span align="center">
    <a href="https://huggingface.co/datasets/JamshidJDMY/TriviaHG/tree/main"><img alt="Huggingface" src="https://img.shields.io/static/v1?label=Dataset&message=TriviaHG&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAIGNIUk0AAHomAACAhAAA+gAAAIDoAAB1MAAA6mAAADqYAAAXcJy6UTwAAAIoUExURQAAAP/////57v/67xUVFf/clv+KAP/uzf/sxv8AAP9TAP/ltP///v/ouP/////////////////////////////8+v/pvP/biP/Vbf/Vbv/cif/qv//9+//////////03v/Yev/Zfv/14//25v/Uav/Vbv/46//////dkf/gmP/////04P/25//pvP/sxf/////lr//ouP/qwP/tyf/msv/ntf/+/P/36f/LUf/36P/w0v/w0//w0//w0//78//gm//QZv/RZv/gm//78v/////14v/nt//gnP/hn//w0f/////w0f/hn//gnP/nt//14v/////////////////LLv/MGv/PGf/LL//LG//THP/THv/SHv/UHv/LGv/LH/7SHuK8JOzDIuW+I+jAI//LHv/PTP/NF/PBG3BkOpyGMvrOH4R0NoV0NvzJGv/MF//QT//MLv/LGPu/FNayJu7FIdq2Jf7DFP/JF//ML//LJurCIsCiKujCIubAI7+hK/DHIf/LJ//HK//NGf/SHeS9IlxSP25QQmtOQmVZPu3DIf/RHf/HLP++Kf/AD/++EP3EFNCfLNhpQthrQdinKv/FFP/AEP+/K/++Dv/BEv+/Ef/CE//MIf/NIP/MGf++D//KTP/FOP/DE//PG//PHP/JGP/EFP/EM//BDf/TH//GFP/CEP/DEP/EEv/BDv/MS//IJ//JHf/JHP/JP//IQf/IHP/IJv/LSf///7SHOh0AAABUdFJOUwAAAAAAAAAAAAAAAAAABiZCQykIAUGn3/Hy4q5KAwRy7vJ/Yfb7cR/X4ipkdpepAqi5mavM2z5v/pGTtZS2QtP4999bIGyry8yUR4fJzbJ2BRIRE9ZoIHEAAAABYktHRAH/Ai3eAAAAB3RJTUUH6AIGEyohVAr+rAAAARZJREFUGNNjYGBgZGTi4xcQFBJmZmRkYQDxRUTFxCUkpaRlZBkZQXw5eYWQ0LCw0HBFJWGgCCOrskpEZFR0dExkrKoaG1BAXSMuPiExOjopOSpFU4uRgV07NS09IzMqKzsnNy9fh4OBU7egsKi4JCo6ubSsvEJPlkHfoDIqqqq6prauPiqqwVCYgcuosam5pbWtvaOzq6nbWJZBy6Snt69/wsRJk6f0TZ1masZgbjF9xsxZhbPnzJ01c8a8+ZYMVgt6F5aHLly0eGHokqVTl1kz2CxYXhi1YuWq1WuiouauXWbLYGe/bv2GjZscHDdv2bh1m5MzA7eLq5u7h6eXoLePr5+/ENDpjBwBgYH6PIyMQcF8vIyMAKnZUpQQgaV4AAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDI0LTAyLTA2VDE5OjQyOjI1KzAwOjAwybP6HAAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyNC0wMi0wNlQxOTo0MjoyNSswMDowMLjuQqAAAAAodEVYdGRhdGU6dGltZXN0YW1wADIwMjQtMDItMDZUMTk6NDI6MzMrMDA6MDBAgVbbAAAAAElFTkSuQmCC&color=20BEFF"/></a>
<a href="https://doi.org/10.1145/3626772.3657855"><img src="https://img.shields.io/static/v1?label=Paper&message=ACM SIGIR&color=green&logo=arxiv"></a>
    <a href="https://colab.research.google.com/github/DataScienceUIBK/TriviaHG/blob/main/Framework/Framework.ipynb"><img src="https://img.shields.io/static/v1?label=Colab&message=Framework&logo=Google%20Colab&color=f9ab00"></a>
</span>
    <a href="https://opensource.org/license/mit"><img src="https://img.shields.io/static/v1?label=License&message=MIT&color=red"></a>
</span>

# TriviaHG: A Dataset for Automatic Hint Generation from Factoid Questions

<img src="https://github.com/DataScienceUIBK/TriviaHG/blob/main/Framework/Framework.png">

*TriviaHG* is an extensive dataset crafted specifically for hint generation in question answering. Unlike conventional datasets, *TriviaHG* provides 10 hints per question instead of direct answers. This unique approach encourages users to engage in critical thinking and reasoning to derive the solution. Covering diverse question types across varying difficulty levels, the dataset is partitioned into training, validation, and test sets. These subsets facilitate the fine-tuning and training of large language models, enhancing the generation of high-quality hints.

## <img src="https://github.com/DataScienceUIBK/TriviaHG/blob/main/Framework/gif-dan.gif" width="32" height="32"/> Attention<img src="https://github.com/DataScienceUIBK/TriviaHG/blob/main/Framework/gif-dan.gif" width="32" height="32"/>

As of **February 2025**, we recommend using **HintEval**, the framework for **hint generation and evaluation**. HintEval includes the **TriviaHG dataset** and the evaluation metrics introduced in the TriviaHG paper, such as **Convergence** and **Familiarity**, making it easier than ever to work with hints.  

Check out HintEval here:  
- 📖 **[HintEval Documentation](http://hinteval.readthedocs.io/)**
- 📦 **[HintEval PyPI Installation](https://pypi.org/project/hinteval/)**
- 💻 **[HintEval GitHub Repository](https://github.com/DataScienceUIBK/HintEval)**
- 📜 **[HintEval Paper (arXiv)](https://doi.org/10.48550/arXiv.2502.00857)**  

For **seamless integration** of hint generation and evaluation, we highly recommend **migrating** to **HintEval**!


## Dataset

*TriviaHG* comprises several sub-datasets, each encompassing [⬇️Training](https://huggingface.co/datasets/JamshidJDMY/TriviaHG/resolve/main/training.json?download=true), [⬇️Validation](https://huggingface.co/datasets/JamshidJDMY/TriviaHG/resolve/main/validation.json?download=true), and [⬇️Test](https://huggingface.co/datasets/JamshidJDMY/TriviaHG/resolve/main/test.json?download=true) sets. You can access and download each subset by clicking on its respective link.

The dataset is structured as JSON files, including training.json, validation.json, and test.json for training, validation, and test phases, respectively:

```json
[
    {
        "Q_ID": "",
        "Question": "",
        "Hints": [ ],
        "Hints_Sources": [  ],
        "Snippet": "",
        "Snippet_Sources": [  ],
        "ExactAnswer": [  ],
        "MajorType": "",
        "MinorType": "",
        "Candidates_Answers": [  ],
        "Q_Popularity": {  },
        "Exact_Answer_Popularity": {  },
        "H_Popularity": [  ],
        "Scores": [  ],
        "Convergence": [  ],
        "Familiarity": [  ]
    }
]

```

### Dataset Statistics
|                   | Training | Validation | Test  |
| ----------------- | -------- | ---------- | ----- |
| Num. of Questions | 14,645   | 1,000      | 1,000 |
| Num. of Hints     | 140,973  | 9,638      | 9,619 |

## Framework and Model Deployment

The `Framework` directory houses essential files for the hint generation framework. Notably, you will find `Framework.ipynb`, a Jupyter Notebook tailored for executing and exploring the framework's code. Utilize [🌐Google Colab](https://colab.research.google.com/github/DataScienceUIBK/TriviaHG/blob/main/Framework/Framework.ipynb) to seamlessly run this notebook and delve into the hint generation process.

### Finetuned Language Models
We have finetuned several large language models, including **LLaMA 7b**, **LLaMA 13b**, and **LLaMA 70b**, on the TriviaHG dataset. These models are not available for direct download but can be accessed via API functions provided by [AnyScale.com](https://www.anyscale.com/). Below are the IDs for the finetuned models:

- LLaMA 7b Finetuned: `meta-llama/Llama-2-7b-chat-hf:Hint_Generator:X6odC0D`
- LLaMA 13b Finetuned: `meta-llama/Llama-2-13b-chat-hf:Hint_Generator:ajid9Dr`
- LLaMA 70b Finetuned: `meta-llama/Llama-2-70b-chat-hf:Hint_Generator:NispySP`

### Querying Finetuned Models
Using CURL:
```shell
export ENDPOINTS_AUTH_TOKEN=YOUR_API_KEY

curl "https://api.endpoints.anyscale.com/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ENDPOINTS_AUTH_TOKEN" \
  -d '{
    "model": "meta-llama/Llama-2-70b-chat-hf:Hint_Generator:NispySP",
    "messages": [
      {"role": "user", "content": "Generate 10 hints for the following question. Question: Which country has the highest population?"}
    ],
    "temperature": 0.0
  }'
```
Or using Python:
```python
import os
import requests

s = requests.Session()

api_base = "https://api.endpoints.anyscale.com/v1"
# Replace with long-lived credentials for production
token = YOUR_API_KEY
url = f"{api_base}/chat/completions"
body = {
  "model": "meta-llama/Llama-2-70b-chat-hf:Hint_Generator:NispySP",
  "messages": [
    {"role": "user", "content": "Generate 10 hints for the following question. Question: Which country has the highest population?"}
  ],
  "temperature": 0.0
}

with s.post(url, headers={"Authorization": f"Bearer {token}"}, json=body) as resp:
  print(resp.json())
```

## Evaluation
### Human Evaluation - Answering

The `Human Evaluation - Answering` folder is a repository that houses Excel files utilized to gather responses from six human participants. Each participant was assigned ten distinct Excel files, each containing a set of ten questions. The table below outlines the types of questions included in the Excel files, along with corresponding statistics collected from participants. The columns in the table below adhere to the format `{Difficulty}-{Model}`, where **B**, **F**, and **V** represent **Bing**, **LLaMA 7b Finetuned**, and **LLaMA 7b Vanilla**, respectively.

|  Question Type  |  Hard-B  |  Hard-F  |  Hard-V  |  Medium-B  |  Medium-F  |  Medium-V  |  Easy-B  |  Easy-F  |  Easy-V  |
|-----------------|----------|----------|----------|------------|------------|------------|----------|----------|----------|
|      ENTITY     |  5 / 9   |  5 / 9   |  4 / 9   |   8 / 8    |   6 / 8    |   4 / 8    |  8 / 8   |  8 / 8   |  6 / 8   |
|      HUMAN      |  2 / 9   |  0 / 9   |  0 / 9   |   5 / 8    |   1 / 8    |   0 / 8    |  6 / 8   |  6 / 8   |  4 / 8   |
|     LOCATION    |  0 / 9   |  0 / 9   |  0 / 9   |   7 / 8    |   5 / 8    |   2 / 8    |  7 / 8   |  6 / 8   |  4 / 8   |
|      OTHER      |  3 / 9   |  2 / 9   |  0 / 9   |   5 / 8    |   2 / 8    |   0 / 8    |  8 / 8   |  7 / 8   |  7 / 8   |

### Human Evaluation - Quality

The `Human Evaluation - Quality` folder encompasses ten Excel files, each containing human annotation values assigned to 2,791 hints across various quality attributes such as relevance, readability, ambiguity, convergence, and familiarity. These attributes are essential markers in assessing the overall quality and effectiveness of the hints generated. The table below provides a concise summary of the average scores attained for each quality attribute, offering insights into the perceived quality of the hints evaluated by human participants.

|         Method       |    Match     | Readability  |  Ambiguity   | Convergence  | Familiarity  |
|----------------------|--------------|--------------|--------------|--------------|--------------|
|      Copilot         |     4.09     |     4.67     |     1.51     |     2.23     |     2.47     |
| LLaMA 7b - Finetuned |     4.01     |     4.70     |     1.56     |     2.20     |     2.41     |
|  LLaMA 7b - Vanilla  |     3.64     |     4.47     |     1.87     |     2.12     |     2.02     |

### Model Performance

Within the `Model Performance` folder, comprehensive insights into the generated hints and their evaluation values for convergence (HICOS) and familiarity (HIFAS) quality attributes are provided. The table below presents a comparative analysis of the results obtained from various models, shedding light on their respective performances in terms of HICOS and HIFAS. This comparative assessment is a valuable resource for gauging the efficacy and effectiveness of each model's hint generation capabilities, thereby informing further enhancements and refinements in the generation process.

|        Model        |    HICOS    |    HIFAS    |
|---------------------|-------------|-------------|
|   LLaMA_7b_Vanilla  |    0.307    |    0.833    |
|  LLaMA_13b_Vanilla  |    0.350    |    0.929    |
|  LLaMA_7b_Finetuned |    0.400    |    0.890    | 
| LLaMA_13b_Finetuned |    0.410    |    0.881    |
|  LLaMA_70b_Vanilla  |    0.425    |    0.941    |
|       GPT_3.5       |    0.438    |    0.911    |
|     WizardLM_70b    |    0.446    |    0.942    |
|        Gemini       |    0.455    |    0.911    |
| LLaMA_70b_Finetuned |    0.494    |    0.862    |
|     GPT_4_turbo     |    0.525    |    0.875    |
|      Copilot        |    0.540    |    0.946    |

## Entities

The `Entities` folder contains a JSON file with 50,000 entities utilized in the Interquartile Range (IQR) method to determine Q1 and Q3 for normalization purposes. These entities play a crucial role in statistical normalization, ensuring robust data distributions and accurate analytical insights. Leveraging the IQR method with this extensive entity set enables users to effectively manage variations and outliers, enhancing the accuracy and reliability of analyses across various domains.

## Citation
### Plain
Jamshid Mozafari, Anubhav Jangra, and Adam Jatowt. 2024. TriviaHG: A Dataset for Automatic Hint Generation from Factoid Questions. In Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR '24). Association for Computing Machinery, New York, NY, USA, 2060–2070. https://doi.org/10.1145/3626772.3657855
### Bibtex
```bibtex
@inproceedings{10.1145/3626772.3657855,
    author = {Mozafari, Jamshid and Jangra, Anubhav and Jatowt, Adam},
    title = {TriviaHG: A Dataset for Automatic Hint Generation from Factoid Questions},
    year = {2024},
    isbn = {9798400704314},
    publisher = {Association for Computing Machinery},
    address = {New York, NY, USA},
    url = {https://doi.org/10.1145/3626772.3657855},
    doi = {10.1145/3626772.3657855},
    booktitle = {Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval},
    pages = {2060–2070},
    numpages = {11},
    keywords = {hint generation, large language models, question answering},
    location = {Washington DC, USA},
    series = {SIGIR '24}
}
