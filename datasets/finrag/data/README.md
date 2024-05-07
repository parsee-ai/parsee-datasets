# finRAG Datasets

This is the official repo of the finRAG datasets published by [parsee.ai](https://parsee.ai).

We wanted to investigate how good the current state of the art (M)LLMs are at solving the relatively simple problem of extracting revenue figures from publicly available financial reports. To test this, we created 3 different datasets, all based on the same selection of 100 randomly selected annual reports for the year 2023 of publicly listed US companies. The 3 datasets are the following:

[“Selection-text”](selection-text): this dataset contains only the relevant profit & loss statement with the revenue numbers that we are looking for. It can be considered our “base-case”, as extracting the revenue numbers from this table only should be the easiest.

[“RAG-text”](rag-text): this dataset tries to simulate a real-world RAG-application, where we chunk the original document into pieces, perform a vector search based on the question that we want to solve, and present the LLMs with the most relevant chunks. We cut off all prompts at 8k tokens for this exercise, so in case the relevant table was not contained in the prompt, we inserted it at the “first position”, to simulate a “happy path” for the vector search, as the goal of this study is not to examine how good or bad vector search is working, but rather to focus on the capabilities of the LLMs if we can guarantee that all required information to solve a task is presented to the model.

[“Selection-image”](selection-image): this dataset is similar to the “Selection-text” dataset in the sense that we feed to the models only an image of the relevant profit & loss statement, that contains all the necessary information to solve the problem.

The datasets contain a combined total of 10,404 rows, 37,536,847 tokens and 1,156 images.