from __future__ import annotations
import os
import shutil
from typing import Callable, Dict, List

from file_utils import collect_file_paths, read_file_data
from file_summarizer import summarize_files
from smart_filename import generate_smart_filename


class ForensicOrganizer:
    """Advanced file organizer that categorizes and renames files."""

    def __init__(
        self,
        sorted_dir: str,
        classifier: Callable[[str], str],
        summarizer,
    ) -> None:
        self.sorted_dir = sorted_dir
        self.classifier = classifier
        self.summarizer = summarizer

    def organize_directory(self, directory: str) -> Dict[str, str]:
        """Organize files in ``directory`` and return summaries."""
        file_paths = collect_file_paths(directory)
        summaries: Dict[str, str] = {}
        for path in file_paths:
            content = read_file_data(path) or ""
            category = self.classifier(content)
            snippet = content[:30].replace("\n", " ")
            new_name = generate_smart_filename(
                os.path.basename(path), category, snippet
            )
            dest_dir = os.path.join(self.sorted_dir, category)
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, new_name)
            shutil.move(path, dest_path)
            summaries[dest_path] = content
        if summaries:
            summaries = summarize_files(list(summaries.keys()), self.summarizer)
        return summaries


if __name__ == "__main__":
    import argparse
    from file_organizer import classify_document
    from nexa.gguf import NexaTextInference
    from output_filter import filter_specific_output

    parser = argparse.ArgumentParser(description="Forensic file organizer")
    parser.add_argument("source", help="Directory with files to organize")
    parser.add_argument(
        "--dest", default="Sorted_Files", help="Destination base directory"
    )
    args = parser.parse_args()

    with filter_specific_output():
        text_inference = NexaTextInference(
            model_path="Llama3.2-3B-Instruct:q3_K_M",
            local_path=None,
            stop_words=[],
            temperature=0.5,
            max_new_tokens=3000,
            top_k=3,
            top_p=0.3,
            profiling=False,
        )

    organizer = ForensicOrganizer(args.dest, classify_document, text_inference)
    summaries = organizer.organize_directory(args.source)
    for path, summary in summaries.items():
        print(f"\n=== {path} ===\n{summary}\n")
