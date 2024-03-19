# Revenues Dataset - Parsing Tables

This dataset consists of 15 pages from annual/quarterly reports of German companies (PDF files), the filings are in English though.

The goal is to evaluate two things:
1) how well can a state-of-the-art LLM retrieve complex structured information from the documents?
2) how does the Parsee.ai document loader fare against the langchain PyPDF loader for this document type

We are using the Claude 3 Opus model for all runs here, as this was the most capable model in our prior experiments (beating GPT 4).

Both datasets have their own Readme's with more info about the methodology, notebooks for the creation of the dataset and evaluation results:
* [Parsee Loader](./parsee-loader/README.md)
* [Langchain Loader](./langchain-pypdf-loader/README.md)

## TLDR

Even though it is impressive how well Claude 3 Opus can work with quite "messy" data (especially the langchain dataset if you look at it), it can only give the right answer in about 47% of the cases for the langchain PyPDF loader. If we use the Parsee Loader we can increase the accuracy to up to 71%.

![final results](final_results.png)