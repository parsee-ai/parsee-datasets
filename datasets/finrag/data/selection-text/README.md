# Selection-text Dataset

This dataset only contains the relevant tables (P&L statements) in text form, that contain all the relevant information to answer the questions we are asking the models.

The first column contains the unique identifier of the file, the second the Parsee extraction template ID and the third the ID of the question (for more details about the questions, please check out our study).

The fourth column contains the expected answer of the model (which is JSON) and the fifth column the full prompt, that can directly be fed to a LLM.

The dataset contains a total of 3,468 rows and 8,449,463 tokens (counted with tiktoken cl100k_base).

