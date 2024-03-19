# Revenues Dataset - Langchain PyPDF Loader
parsee-core version used: 0.1.3.14

This dataset was created on the basis of 15 pages from annual/quarterly filings of major German stock-exchange listed companies (PDF files).

All PDF files are publicly accessible on parsee.ai, to access them copy the "source_identifier" (first column) and paste it in this URL (replace '{SOURCE_IDENTIFIER}' with the actual identifier):

https://app.parsee.ai/documents/view/{SOURCE_IDENTIFIER}

So for example:

https://app.parsee.ai/documents/view/a8f9dc45fc64a66a4d419ddb56399bcb79a74cb8948d35e8bfa06671f8c47318

# Methodology

The goal of this dataset was to load the files using the PyPDF document loader from [langchain](https://python.langchain.com/docs/modules/data_connection/document_loaders/pdf#using-pypdf) and evaluate how an LLM performs using this data compared to the Parsee.ai document loader for PDF files, which is based on the [Parsee PDF Reader](https://github.com/parsee-ai/parsee-pdf-reader).

The following code was used to create the dataset: [jupyter notebook](create_dataset.ipynb)

The correct answers for each row were loaded from Parsee Cloud, where they were checked by a human and corrected prior to running this code.


# LLM Evaluation

For the evaluation we are using the Claude 3 Opus model from [Anthropic](https://www.anthropic.com/api).

The results of the evaluation can be found here: [jupyter notebook](evaluation.ipynb)
