# Invoice Dataset - Parsee Loader
parsee-core version used: 0.1.3.11

This dataset was created on the basis of 15 sample invoices (PDF files).

All PDF files are publicly accessible on parsee.ai, to access them copy the "source_identifier" (first column) and paste it in this URL (replace '{SOURCE_IDENTIFIER}' with the actual identifier):

https://app.parsee.ai/documents/view/{SOURCE_IDENTIFIER}

So for example:

https://app.parsee.ai/documents/view/1fd7fdbd88d78aa6e80737b8757290b78570679fbb926995db362f38a0d161ea

# Methodology

The goal of this dataset was to load the files using the [Parsee PDF Reader](https://github.com/parsee-ai/parsee-pdf-reader) and to compare the results to the langchain PyPDF loader.

The invoices were selected randomly and are in either German or English.

The dataset was created on [Parsee Cloud](https://app.parsee.ai), where all output was checked by a human and corrected prior to running this code.

# LLM Evaluation
For the evaluation we are using the mistralai/mixtral-8x7b-instruct-v0.1 model from [replicate](https://replicate.com/).

The results of the evaluation can be found here: [jupyter notebook](evaluation.ipynb)
