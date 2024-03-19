# Revenues Dataset - Parsee Loader
parsee-core version used: 0.1.3.14

This dataset was created on the basis of 15 pages from annual/quarterly filings of major German stock-exchange listed companies (PDF files).

All PDF files are publicly accessible on parsee.ai, to access them copy the "source_identifier" (first column) and paste it in this URL (replace '{SOURCE_IDENTIFIER}' with the actual identifier):

https://app.parsee.ai/documents/view/{SOURCE_IDENTIFIER}

So for example:

https://app.parsee.ai/documents/view/a8f9dc45fc64a66a4d419ddb56399bcb79a74cb8948d35e8bfa06671f8c47318

# Methodology

The goal of this dataset was to load the files using the [Parsee PDF Reader](https://github.com/parsee-ai/parsee-pdf-reader) and to compare the results to the langchain PyPDF loader.

The dataset was created on [Parsee Cloud](https://app.parsee.ai), where all output was checked by a human and corrected prior to running this code.

All prompts were truncated to a max of 8k tokens, but this should not affect the prompts for this dataset, as the files are just single pages and thus quite small.

# LLM Evaluation

For the evaluation we are using the Claude 3 Opus model from [Anthropic](https://www.anthropic.com/api).

The results of the evaluation can be found here: [jupyter notebook](evaluation.ipynb)
