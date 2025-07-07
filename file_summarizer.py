import argparse
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor

from file_utils import (
    collect_file_paths,
    read_file_data,
    separate_files_by_type,
)
from text_data_processing import summarize_text_content
import os


def summarize_files(file_paths: List[str], text_inference) -> Dict[str, str]:
    """Return summaries for given file paths.

    Args:
        file_paths: List of files to summarize.
        text_inference: Inference object with a ``create_completion`` method.

    Returns:
        Mapping of file path to generated summary text.
    """
    summaries: Dict[str, str] = {}
    _, text_files = separate_files_by_type(file_paths)
    for path in text_files:
        text = read_file_data(path)
        if text:
            summaries[path] = summarize_text_content(text, text_inference)
    return summaries


def summarize_files_parallel(
    file_paths: List[str], text_inference, workers: int = 4
) -> Dict[str, str]:
    """Summarize files concurrently using a thread pool."""
    summaries: Dict[str, str] = {}
    _, text_files = separate_files_by_type(file_paths)

    def process(path: str) -> None:
        text = read_file_data(path)
        if text:
            summaries[path] = summarize_text_content(text, text_inference)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(process, text_files)

    return summaries


def summarize_path(
    path: str, text_inference, *, parallel: bool = False, workers: int = 4
) -> Dict[str, str]:
    """Summarize a single file or all files in a directory.

    Args:
        path: Path to a file or directory to summarize.
        text_inference: Inference object with a ``create_completion`` method.

    Returns:
        A dictionary mapping file paths to their summaries.

    Raises:
        FileNotFoundError: If ``path`` does not exist.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    file_paths = collect_file_paths(path)
    if parallel:
        return summarize_files_parallel(file_paths, text_inference, workers=workers)
    return summarize_files(file_paths, text_inference)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch summarize documents")
    parser.add_argument("path", help="File or directory to summarize")
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Summarize files concurrently using threads",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Number of worker threads for parallel summarization",
    )
    args = parser.parse_args()

    from nexa.gguf import NexaTextInference
    from output_filter import filter_specific_output

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
            profiling=False,
        )
    for file, summary in summarize_path(
        args.path,
        text_inference,
        parallel=args.parallel,
        workers=args.workers,
    ).items():
        print(f"\n=== {file} ===\n{summary}\n")
