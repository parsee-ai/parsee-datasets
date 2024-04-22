import os

from parsee.datasets.evaluation.main import *
from parsee.cloud.api import ParseeCloud
from parsee.datasets.readers.disk_reader import SimpleCsvDiskReader
from parsee.extraction.models.helpers import *
from parsee.datasets.writers.disk_writer import CsvDiskWriter
from parsee.storage.in_memory_storage import InMemoryStorageManager
from parsee.converters.image_creation import DiskImageReader


"""
requires the following variables set in .env in order to re-run the evaluation (for new files, if not the cached answers are being used):
PARSEE_API_KEY -> api key for parsee cloud
OPENAI_KEY -> openai api key
REPLICATE_API_TOKEN -> api key for replicate.com
TOGETHER_KEY -> api key for together.xyz
"""
def run_eval_by_file(csv_file_path: str, writer_path: Optional[str], multimodal: bool, token_limit: int = 4000, use_cached_only: bool = False, images_dir: Optional[str] = None):

    custom_storage = None
    if not multimodal:
        models = [
            anthropic_config(os.getenv("ANTHROPIC_API_KEY") if not use_cached_only else "n/a", "claude-3-opus-20240229", token_limit),
            gpt_config(os.getenv("OPENAI_KEY") if not use_cached_only else "n/a", token_limit, "gpt-4-1106-preview"),
            replicate_config(os.getenv("REPLICATE_API_TOKEN") if not use_cached_only else "n/a", "meta/meta-llama-3-70b-instruct", token_limit),
            replicate_config(os.getenv("REPLICATE_API_TOKEN") if not use_cached_only else "n/a", "meta/meta-llama-3-8b-instruct", token_limit),
            #replicate_config(os.getenv("REPLICATE_API_TOKEN") if not use_cached_only else None, "mistralai/mixtral-8x7b-instruct-v0.1", token_limit),
            together_config(os.getenv("TOGETHER_KEY") if not use_cached_only else "n/a", "mistralai/Mixtral-8x22B-Instruct-v0.1", token_limit),
            together_config(os.getenv("TOGETHER_KEY") if not use_cached_only else "n/a", "databricks/dbrx-instruct", token_limit)
        ]
    else:
        models = [
            anthropic_config(os.getenv("ANTHROPIC_API_KEY") if not use_cached_only else "n/a", "claude-3-opus-20240229", token_limit, True, 1),
            gpt_config(os.getenv("OPENAI_KEY") if not use_cached_only else "n/a", token_limit, "gpt-4-1106-vision-preview", True, 1),
        ]
        custom_storage = InMemoryStorageManager(models, DiskImageReader(images_dir))

    cloud = ParseeCloud(os.getenv('PARSEE_API_KEY') if not use_cached_only else None)
    template = cloud.get_template("661bd24fb129ff2526f2af09")
    reader = SimpleCsvDiskReader(csv_file_path)
    writer = None
    writer_file_name = None
    if writer_path is not None:
        writer = CsvDiskWriter(writer_path, False)
        writer_file_name = os.path.basename(csv_file_path).split(".")[0] + "_with_answers"
    performance = evaluate_llm_performance(template, reader, models, custom_storage, writer, True, writer_file_name)
    return performance
