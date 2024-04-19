import os

from parsee.datasets.evaluation.main import *
from parsee.cloud.api import ParseeCloud
from parsee.datasets.readers.disk_reader import SimpleCsvDiskReader
from parsee.extraction.models.helpers import *
from parsee.datasets.writers.disk_writer import CsvDiskWriter


"""
requires the following variables set in .env:
PARSEE_API_KEY -> api key for parsee cloud
OPENAI_KEY -> openai api key
REPLICATE_API_TOKEN -> api key for replicate.com
TOGETHER_KEY -> api key for together.xyz
"""
def run_eval_by_file(csv_file_path: str, writer_path: str, multimodal: bool, token_limit: int = 4000):

    if not multimodal:
        models = [
            anthropic_config(os.getenv("ANTHROPIC_API_KEY"), "claude-3-opus-20240229", token_limit),
            gpt_config(os.getenv("OPENAI_KEY"), token_limit, "gpt-4-1106-preview"),
            replicate_config(os.getenv("REPLICATE_API_TOKEN"), "meta/meta-llama-3-70b-instruct", token_limit),
            replicate_config(os.getenv("REPLICATE_API_TOKEN"), "meta/meta-llama-3-8b-instruct", token_limit),
            replicate_config(os.getenv("REPLICATE_API_TOKEN"), "mistralai/mixtral-8x7b-instruct-v0.1", token_limit),
            together_config(os.getenv("TOGETHER_KEY"), "mistralai/Mixtral-8x22B-Instruct-v0.1", token_limit),
            together_config(os.getenv("TOGETHER_KEY"), "databricks/dbrx-instruct", token_limit)
        ]
    else:
        models = []

    cloud = ParseeCloud(os.getenv('PARSEE_API_KEY'))
    template = cloud.get_template("661bd24fb129ff2526f2af09")
    reader = SimpleCsvDiskReader(csv_file_path)
    writer = CsvDiskWriter(writer_path, False)
    performance = evaluate_llm_performance(template, reader, models, None, writer, True, os.path.basename(csv_file_path).split(".")[0]+"_with_answers")
    return performance
