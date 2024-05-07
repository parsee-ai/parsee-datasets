# finRAG Study
The finRAG study is looking at a subset of 50 filings chosen from the 1116 reports.
We believe this number is sufficient to yield statistically significant results as each filing has 3 sub-datasets and 6 questions each, so a total of 900 rows.
We encourage further research to be done with the dataset and as all the materials are open sourced, checking this hypothesis is open for anyone to explore.

## Models Used
We selected the following models for our study:

* Claude 3 Opus by Anthropic
* ChatGPT 4 (1106-preview and 1106-vision-preview) by OpenAI
* Google Gemini 1.5 Pro by Google
* Llama-3-70b-instruct by Meta
* Llama-3-8b-instruct by Meta
* Mixtral-8x22B-instruct-v0.1 by Mistral
* Mixtral-8x7b-instruct-v0.1 by Mistral
* dbrx-instruct by Databricks
* Command R by Cohere

We believe this selection is as of the date of the study a selection of the most capable instruct models available.

We accessed all models via either their proprietary APIs or via Replicate/together AI.