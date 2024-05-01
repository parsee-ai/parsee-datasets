import os

from parsee.datasets.evaluation.main import *
from parsee.cloud.api import ParseeCloud
from parsee.datasets.readers.disk_reader import SimpleCsvDiskReader
from parsee.extraction.models.helpers import *
from parsee.datasets.writers.disk_writer import CsvDiskWriter
from parsee.storage.in_memory_storage import InMemoryStorageManager
from parsee.converters.image_creation import DiskImageReader
from parsee.extraction.extractor_dataclasses import ParseeAnswer

"""
We are using this custom evaluation function for the results,
where we basically multiply all results with their units and then check if the values deviate not more than 0.1%
"""
def results_compare_function(answer1: ParseeAnswer, answer2: ParseeAnswer) -> bool:
    mults = {
        "none": 1,
        "thousands": 1000,
        "millions": 1000000,
        "billions": 1000000000
    }
    unit1 = [x for x in answer1.meta if x.class_id == 'unit']
    unit_mult1 = 1 if len(unit1) == 0 else (mults[unit1[0].class_value] if unit1[0].class_value in mults else 1)
    val1 = int(float(answer1.class_value)*unit_mult1)

    unit2 = [x for x in answer2.meta if x.class_id == 'unit']
    unit_mult2 = 1 if len(unit2) == 0 else (mults[unit2[0].class_value] if unit2[0].class_value in mults else 1)
    val2 = int(float(answer2.class_value) * unit_mult2)

    diff_rel = (abs(val1-val2) / val1)
    return diff_rel < 0.001


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
            together_config(os.getenv("TOGETHER_KEY") if not use_cached_only else "n/a", "mistralai/Mixtral-8x22B-Instruct-v0.1", token_limit),
            mistral_api_config(os.getenv("MISTRAL_KEY"), "mistral-large-latest", token_limit),
            together_config(os.getenv("TOGETHER_KEY") if not use_cached_only else "n/a", "databricks/dbrx-instruct", token_limit),
            together_config(os.getenv("TOGETHER_KEY") if not use_cached_only else "n/a", "Snowflake/snowflake-arctic-instruct", token_limit),
            cohere_config(os.getenv("COHERE_KEY"), "command-r-plus", token_limit),
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
    if writer_path is not None and not use_cached_only:
        writer = CsvDiskWriter(writer_path, False)
        writer_file_name = os.path.basename(csv_file_path).split(".")[0] + "_with_answers"
    performance = evaluate_llm_performance(template, reader, models, custom_storage, writer, True, writer_file_name, {"rev_meta": results_compare_function, "rev23_meta": results_compare_function, "rev22_meta": results_compare_function}, ["unit"])
    return performance
