# finRAG Dataset

This is the official repo for the finRAG dataset. All the data of the [finRAG study](TO INSERT) published by [parsee.ai](https://parsee.ai) can be found here.

The goal of this dataset is to present several possible ways of how financial information can be extracted from a real-world document using (M)LLMs.

## Dataset Structure & Size
The dataset was created based on 1116 publicly available annual reports for the year ending 2023 of listed companies, mostly based in the US.

From these 1116 reports, we are creating 3 sub-datasets (2 with text, 1 with images) and for each sub-dataset we are asking 6 questions (see below for details), resulting in a total of 20088 rows (1116 * 3 * 6).

All the 1116 "raw" reports (which are HTML files) can be found in the folder [data/raw](data/raw). These can simply be viewed in the browser.

Each sub-dataset has its own folder:
* [RAG-text](data/rag-text)
* [Selection-text](data/selection-text)
* [Selection-image](data/selection-image)

### Sub-dataset Explanation
#### RAG-text
The RAG-text sub-dataset tries to simulate the real-world RAG case where we don't know where in the entire report the relevant information for answering the question is located.
As such, we follow the classic RAG-approach of splitting the document into chunks, running a vector search (using FAISS) and presenting the model only the text-pieces which we think are the most relevant for answering the question, and then applying a cut-off after reaching a maximum of 4,000 tokens for the entire prompt (this amount of tokens was chosen to make sure that we can also test some smaller open source models with a context window of e.g. max 4k tokens).
The goal of this dataset (and study) is not to explore how good (or bad) vector search is performing. As a consequence, as we know which chunks contain the relevant information for answering the question (courtesy of [SimFin](https://simfin.com) for providing the labeled data), in case the vector search did not contain the relevant pieces of information (after applying the token limit of 4k), we are inserting the relevant element at the first position "manually", simulating a "happy path" where the vector search correctly finds the most relevant piece of information and puts it at the first position.

#### Selection-text
The Selection-text dataset contains only the tables that actually contain the 2023 revenue numbers, that is the income statement for the year 2023. This dataset should be in theory the "easiest", as only the relevant table is presented in text form, and serves therefore as the base-case for comparing results to the other sub-datasets.

#### Selection-image
The Selection-image dataset is similar to the Selection-text dataset in the sense that it only contains the relevant table for answering the questions, with the difference being that this dataset is not text-based but rather made for multimodal models that are supposed to answer the questions based on the prompt (which is adapted for the image-case) and the image of the table.
As such, in the sub-folder [data/selection-image/images] there are 1116 images of the tables in JPEG format.

### Prompts
For creating the prompts, we are asking essentially the same question in 6 different ways, some with the same expected output, some with a different expected output.

This question is in essence: What are the revenues of the company?

Now, since an annual report typically contains more than just one revenue number, there is no "one" answer which is correct.
For this reason we are asking for 4 of the 6 questions from the models to just return the revenue number of a specific year.
The years we are interested in are 2023 and 2022 (both times the 12 month period since we are dealing with annual reports).

The questions we are asking (note: these are not the full prompts, as these are created with the [parsee-core library](https://github.com/parsee-ai/parsee-core)) in this case are the following (each question has an ID, which will be also the folder name of the sub-datasets):

* What are the revenues for the 12 month period ending december 2023 (in thousand USD)? (id: rev23_thousands_no_hint)
* What are the revenues for the 12 month period ending december 2023 (in thousand USD)? Hint: Please double check your answer and make sure the unit of the number is in thousands, format the number if necessary (add or remove digits). (id: rev23_thousands_hint)
* What are the revenues for the 12 month period ending december 2023 (in million USD)? (id: rev23_millions_no_hint)
* What are the revenues for the 12 month period ending december 2022 (in million USD)? (id: rev22_millions_no_hint)

These 4 questions essentially require a single number as response, formatted to the correct unit as requested by the user.
The other 2 questions leave the extraction of the unit (and currency) to the model (for details, see the functioning of the [parsee-core library](https://github.com/parsee-ai/parsee-core)):

* What are the revenues for the 12 month period ending december 2023? (id: rev23_meta)
* What are the revenues of the company? (id: rev_meta)

The last question (rev_meta) is the hardest, as it requires the model to not just extract a single number, but instead ALL the revenue numbers that can be found in the table, along with the correct time-information (ending date and number of months in period).

# finRAG Study
The finRAG study is looking at a subset of 50 filings chosen from the 1116 reports and has its [own readme](study/README.md).