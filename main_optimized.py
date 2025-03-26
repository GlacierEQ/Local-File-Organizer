import os
import time
from typing import List, Tuple, Generator
from functools import lru_cache

from file_utils import (
    display_directory_tree,
    separate_files_by_type,
    read_file_data
)

from data_processing_common import (
    compute_operations,
    execute_operations,
    process_files_by_date,
    process_files_by_type,
)

from text_data_processing import process_text_files
from image_data_processing import process_image_files
from output_filter import filter_specific_output
from nexa.gguf import NexaVLMInference, NexaTextInference

def ensure_nltk_data():
    import nltk
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('wordnet', quiet=True)

# Global variables for models
image_inference = None
text_inference = None

@lru_cache(maxsize=1)
def get_image_inference():
    global image_inference
    if image_inference is None:
        model_path = "llava-v1.6-vicuna-7b:q4_0"
        with filter_specific_output():
            image_inference = NexaVLMInference(
                model_path=model_path,
                local_path=None,
                stop_words=[],
                temperature=0.3,
                max_new_tokens=3000,
                top_k=3,
                top_p=0.2,
                profiling=False
            )
    return image_inference

@lru_cache(maxsize=1)
def get_text_inference():
    global text_inference
    if text_inference is None:
        model_path_text = "Llama3.2-3B-Instruct:q3_K_M"
        with filter_specific_output():
            text_inference = NexaTextInference(
                model_path=model_path_text,
                local_path=None,
                stop_words=[],
                temperature=0.5,
                max_new_tokens=3000,
                top_k=3,
                top_p=0.3,
                profiling=False
            )
    return text_inference

def collect_file_paths(input_path: str) -> Generator[str, None, None]:
    for root, _, files in os.walk(input_path):
        for file in files:
            yield os.path.join(root, file)

def process_files_in_batches(file_paths: List[str], batch_size: int = 100) -> Generator[List[dict], None, None]:
    batch = []
    for file_path in file_paths:
        batch.append(file_path)
        if len(batch) == batch_size:
            yield process_batch(batch)
            batch = []
    if batch:
        yield process_batch(batch)

def process_batch(batch: List[str]) -> List[dict]:
    image_files, text_files = separate_files_by_type(batch)
    
    text_tuples = []
    for fp in text_files:
        text_content = read_file_data(fp)
        if text_content is not None:
            text_tuples.append((fp, text_content))

    data_images = process_image_files(image_files, get_image_inference(), get_text_inference())
    data_texts = process_text_files(text_tuples, get_text_inference())

    return data_images + data_texts

# ... [rest of the helper functions remain the same] ...

def main():
    ensure_nltk_data()
    
    silent_mode = get_yes_no("Would you like to enable silent mode? (yes/no): ")
    log_file = 'operation_log.txt' if silent_mode else None

    while True:
        input_path = input("Enter the path of the directory you want to organize: ").strip()
        while not os.path.exists(input_path):
            print(f"Input path {input_path} does not exist. Please enter a valid path.")
            input_path = input("Enter the path of the directory you want to organize: ").strip()

        output_path = input("Enter the path to store organized files and folders (press Enter to use 'organized_folder' in the input directory): ").strip()
        if not output_path:
            output_path = os.path.join(os.path.dirname(input_path), 'organized_folder')

        start_time = time.time()
        file_paths = list(collect_file_paths(input_path))
        end_time = time.time()

        print(f"Time taken to load file paths: {end_time - start_time:.2f} seconds")

        mode = get_mode_selection()

        if mode == 'content':
            all_data = []
            for batch_data in process_files_in_batches(file_paths):
                all_data.extend(batch_data)

            renamed_files = set()
            processed_files = set()
            operations = compute_operations(all_data, output_path, renamed_files, processed_files)

        elif mode == 'date':
            operations = process_files_by_date(file_paths, output_path, dry_run=False, silent=silent_mode, log_file=log_file)
        elif mode == 'type':
            operations = process_files_by_type(file_paths, output_path, dry_run=False, silent=silent_mode, log_file=log_file)
        else:
            print("Invalid mode selected.")
            return

        print("Proposed directory structure:")
        simulated_tree = simulate_directory_tree(operations, output_path)
        print_simulated_tree(simulated_tree)

        if get_yes_no("Would you like to proceed with these changes? (yes/no): "):
            os.makedirs(output_path, exist_ok=True)
            execute_operations(operations, dry_run=False, silent=silent_mode, log_file=log_file)
            print("The files have been organized successfully.")
        else:
            print("Operation canceled by the user.")

        if not get_yes_no("Would you like to organize another directory? (yes/no): "):
            break

if __name__ == '__main__':
    main()
