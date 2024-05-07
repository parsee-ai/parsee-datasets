# Rag-text Dataset

This dataset tries to simulate a real-world RAG-application, where we chunk the original document into pieces, perform a vector search based on the question that we want to solve, and present the LLMs with the most relevant chunks. We cut off all prompts at 8k tokens for this exercise, so in case the relevant table was not contained in the prompt, we inserted it at the “first position”, to simulate a “happy path” for the vector search, as the goal of this study is not to examine how good or bad vector search is working, but rather to focus on the capabilities of the LLMs if we can guarantee that all required information to solve a task is presented to the model.

The first column contains the unique identifier of the file, the second the Parsee extraction template ID and the third the ID of the question (for more details about the questions, please check out our study).

The fourth column contains the expected answer of the model (which is JSON) and the fifth column the full prompt, that can directly be fed to a LLM.

The dataset contains a total of 3,468 rows and 27,956,793 tokens (counted with tiktoken cl100k_base).

