import os

import pandas as pd

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
    if answer1.class_value == "n/a" and answer2.class_value == "n/a":
        return True
    elif answer1.class_value == "n/a" or answer2.class_value == "n/a":
        return False
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
"""
def run_eval_by_file(template_id: str, csv_file_path: str, writer_path: Optional[str], models: List[MlModelSpecification], use_cached_only: bool = False, images_dir: Optional[str] = None):

    custom_storage = None if not models[0].multimodal else InMemoryStorageManager(models, DiskImageReader(images_dir))

    cloud = ParseeCloud(os.getenv('PARSEE_API_KEY') if not use_cached_only else None)
    template = cloud.get_template(template_id)
    reader = SimpleCsvDiskReader(csv_file_path)
    writer = None
    writer_file_name = None
    if writer_path is not None and not use_cached_only:
        writer = CsvDiskWriter(writer_path, False)
        writer_file_name = os.path.basename(csv_file_path).split(".")[0] + "_with_answers"
    performance = evaluate_llm_performance(template, reader, models, custom_storage, writer, True, writer_file_name, {"rev_meta": results_compare_function, "rev23_meta": results_compare_function, "rev22_meta": results_compare_function , "rev23_thousands_no_hint": results_compare_function, "rev22_millions_no_hint": results_compare_function, "rev23_thousands_hint": results_compare_function, "rev23_millions_no_hint": results_compare_function}, ["unit"], not use_cached_only)
    return performance


def make_df_single_dataset(template_id: str, dataset_path: str, models: List[MlModelSpecification]) -> pd.DataFrame:
    stats = run_eval_by_file(template_id, dataset_path, None, models, use_cached_only=True)
    all_values = []
    for model, values in stats.items():
        if model != "assigned":
            values = {"model": model, **values}
            all_values.append(values)
    return pd.DataFrame(all_values)


def make_df(template_id: str, folder_path: str, models: List[MlModelSpecification]) -> Tuple[pd.DataFrame, List[str]]:
    all_files = [x for x in os.listdir(folder_path) if x.endswith(".csv")]
    all_dataset_names = [x.replace("_with_answers.csv", "") for x in all_files]
    relevant_keys = {"total_correct_percent", "total_correct_meta_found_percent", "total_correct_percent_ex_missing", "total_correct_meta_found_percent_ex_missing", "total"}
    # collect all results
    all_results = {}
    total_by_model = {}
    for file_idx, file in enumerate(all_files):
        full_path = os.path.join(folder_path, file)
        stats = run_eval_by_file(template_id, full_path, None, models, use_cached_only=True)
        dataset_name = all_dataset_names[file_idx]

        for model_name, results in stats.items():
            # we are putting a weight to the meta info of 1/4 (3/4 to the 'main' question) as the actual numbers are more important
            results["total"] = results["total_correct_percent"] if results["total_correct_meta_found_percent"] is None else (
                        (results["total_correct_percent"]*3 + results["total_correct_meta_found_percent"]) / 4)

            if model_name not in all_results:
                all_results[model_name] = {}
                total_by_model[model_name] = 0
            for key in relevant_keys:
                final_key = f"{dataset_name}_{key}"
                all_results[model_name][final_key] = results[key]
                if key == "total":
                    total_by_model[model_name] += results[key]

    arr = []
    for model_name, values in all_results.items():
        if model_name != "assigned":
            values = {"model": model_name, "total": total_by_model[model_name] / len(all_files), **values}
            arr.append(values)

    df = pd.DataFrame(arr)
    return df, all_dataset_names