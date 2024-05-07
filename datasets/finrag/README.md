# finRAG

This is the official repo for the finRAG dataset and study. All the data of the [finRAG study](https://www.parsee.ai/en/blog/finrag-dataset-and-study/) published by [parsee.ai](https://parsee.ai) can be found here.

The goal of the datasets and study is to evaluate several possible ways of how financial information can be extracted from a real-world document using (M)LLMs. The study is also focusing on individual model performance using a subset of 100 filings.

## Dataset Structure & Size
The dataset was created based on 1156 publicly available annual reports for the year ending 2023 of listed companies, mostly based in the US.

From these 1156 reports, we are creating 3 sub-datasets (2 with text, 1 with images) and for each sub-dataset we are asking 3 questions (see below for details).

The datasets contain a combined total of 10,404 rows, 37,536,847 tokens and 1,156 images.

Each sub-dataset has its own folder:
* [RAG-text](data/rag-text)
* [Selection-text](data/selection-text)
* [Selection-image](data/selection-image)

### Sub-dataset Explanation
[“Selection-text”](data/selection-text): this dataset contains only the relevant profit & loss statement with the revenue numbers that we are looking for. It can be considered our “base-case”, as extracting the revenue numbers from this table only should be the easiest.

[“RAG-text”](data/rag-text): this dataset tries to simulate a real-world RAG-application, where we chunk the original document into pieces, perform a vector search based on the question that we want to solve, and present the LLMs with the most relevant chunks. We cut off all prompts at 8k tokens for this exercise, so in case the relevant table was not contained in the prompt, we inserted it at the “first position”, to simulate a “happy path” for the vector search, as the goal of this study is not to examine how good or bad vector search is working, but rather to focus on the capabilities of the LLMs if we can guarantee that all required information to solve a task is presented to the model.

[“Selection-image”](data/selection-image): this dataset is similar to the “Selection-text” dataset in the sense that we feed to the models only an image of the relevant profit & loss statement, that contains all the necessary information to solve the problem.

### Note about table formatting and chunking for RAG-text and Selection-text datasets
Converting the tables to simple strings and chunking is done with the [parsee-core](https://github.com/parsee-ai/parsee-core) library. Each cell in table is not just a dictionary (the keys being the column headers, which is what some libraries are doing), as some cells have colspans that are bigger than 1 and headers might span multiple columns and rows. The table strings are still easily readable such that a human for example can understand the table and find the right information. For details please refer to the parsee-core library.

### Prompts Explanation
For an in-depth explanation of our methodology please check out the [finRAG study](https://www.parsee.ai/en/blog/finrag-dataset-and-study/). 

## finRAG Study
The finRAG study is looking at a subset of 100 filings chosen from the 1156 reports and has its [own readme](study/README.md).