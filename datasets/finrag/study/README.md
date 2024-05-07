# finRAG Study
The finRAG study is looking at a subset of 100 filings chosen from the 1156 reports.
We believe this number is sufficient to yield statistically significant results as each filing has 3 sub-datasets and 3 questions each, so a total of 900 rows.
We encourage further research to be done with the dataset and as all the materials are open sourced, checking this hypothesis is open for anyone to explore.

A full article explaining the findings can be found here: https://www.parsee.ai/en/blog/finrag-dataset-and-study/

## Models Used
We selected the following models for our study:

* Claude 3 Opus by Anthropic
* ChatGPT 4 (1106-preview and 1106-vision-preview) by OpenAI
* Llama-3-70b-instruct by Meta (hosted on replicate)
* Mistral Large by Mistral
* Mixtral-8x22B-instruct-v0.1 by Mistral (hosted on together.ai)
* dbrx-instruct by Databricks (hosted on together.ai)
* Command R by Cohere
* Snowflake Arctic  (hosted on together.ai)

We believe this selection is as of the date of the study a selection of the most capable instruct models available.

We accessed all models via either their proprietary APIs or via Replicate/together AI, so the goal was to use the "best" (i.e. unquantized) versions of the models.