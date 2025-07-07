import os
import hashlib
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import List, Dict, Callable, Any
from functools import lru_cache
import random
import multiprocessing
from database import Database
from config import Config


class PerformanceOptimizer:
    """Handles performance optimization for file operations"""

    def __init__(self, config: Config, database: Database):
        self.config = config
        self.database = database
        self.max_workers = multiprocessing.cpu_count()
        self._file_hash_cache = {}

    def compute_file_hash(self, file_path: str) -> str:
        """Compute hash of file for caching purposes"""
        if file_path in self._file_hash_cache:
            return self._file_hash_cache[file_path]

        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)

        file_hash = hasher.hexdigest()
        self._file_hash_cache[file_path] = file_hash
        return file_hash

    @lru_cache(maxsize=1000)
    def get_file_metadata(self, file_path: str) -> Dict:
        """Get file metadata with caching"""
        file_hash = self.compute_file_hash(file_path)

        # Check database cache first
        with self.database.connect() as cursor:
            cursor.execute(
                """
                SELECT metadata FROM files 
                WHERE hash = ? AND original_path = ?
            """,
                (file_hash, file_path),
            )
            result = cursor.fetchone()

            if result:
                return result[0]

        # If not in cache, compute metadata
        metadata = self._compute_file_metadata(file_path)

        # Store in database
        self.database.add_file(
            file_path=file_path,
            file_type=os.path.splitext(file_path)[1],
            metadata=metadata,
            hash=file_hash,
        )

        return metadata

    def _compute_file_metadata(self, file_path: str) -> Dict:
        """Compute file metadata"""
        stats = os.stat(file_path)
        return {
            "size": stats.st_size,
            "created": stats.st_ctime,
            "modified": stats.st_mtime,
            "accessed": stats.st_atime,
            "extension": os.path.splitext(file_path)[1],
            "filename": os.path.basename(file_path),
        }

    def parallel_process_files(
        self,
        files: List[str],
        process_func: Callable[[str], Any],
        use_processes: bool = False,
    ) -> List[Any]:
        """Process files in parallel using either threads or processes"""
        executor_class = ProcessPoolExecutor if use_processes else ThreadPoolExecutor

        with executor_class(max_workers=self.max_workers) as executor:
            results = list(executor.map(process_func, files))

        return results

    def batch_process_files(
        self,
        files: List[str],
        process_func: Callable[[List[str]], List[Any]],
        batch_size: int = 1000,
    ) -> List[Any]:
        """Process files in batches to manage memory usage"""
        results = []
        for i in range(0, len(files), batch_size):
            batch = files[i : i + batch_size]
            batch_results = process_func(batch)
            results.extend(batch_results)
        return results

    def optimize_file_operations(self, operations: List[Dict]) -> List[Dict]:
        """Optimize file operations to minimize disk I/O"""
        # Group operations by source directory
        dir_groups = {}
        for op in operations:
            source_dir = os.path.dirname(op["source"])
            if source_dir not in dir_groups:
                dir_groups[source_dir] = []
            dir_groups[source_dir].append(op)

        # Reorder operations to minimize directory switches
        optimized_ops = []
        for dir_path, dir_ops in dir_groups.items():
            # Sort operations within each directory group
            dir_ops.sort(key=lambda x: x["destination"])
            optimized_ops.extend(dir_ops)

        return optimized_ops

    def evolutionary_optimize_file_order(
        self,
        operations: List[Dict],
        generations: int = 50,
        population_size: int = 50,
    ) -> List[Dict]:
        """Use a genetic algorithm to optimize file operation ordering."""

        def fitness(order: List[int]) -> int:
            switches = 0
            last_dir = os.path.dirname(operations[order[0]]["source"])
            for idx in order[1:]:
                current_dir = os.path.dirname(operations[idx]["source"])
                if current_dir != last_dir:
                    switches += 1
                last_dir = current_dir
            return -switches

        population = [
            random.sample(range(len(operations)), len(operations))
            for _ in range(population_size)
        ]
        for _ in range(generations):
            scored = sorted(
                ((fitness(ind), ind) for ind in population),
                key=lambda x: x[0],
                reverse=True,
            )
            population = [ind for _, ind in scored[: population_size // 2]]
            while len(population) < population_size:
                parent1, parent2 = random.sample(population[: population_size // 4], 2)
                cut = random.randint(1, len(operations) - 2)
                child = parent1[:cut] + [i for i in parent2 if i not in parent1[:cut]]
                if random.random() < 0.2:
                    i, j = random.sample(range(len(operations)), 2)
                    child[i], child[j] = child[j], child[i]
                population.append(child)

        best_order = max(population, key=fitness)
        return [operations[i] for i in best_order]

    def get_cached_ai_result(
        self, file_path: str, model_version: str, processing_type: str
    ) -> Dict:
        """Get cached AI processing result"""
        file_hash = self.compute_file_hash(file_path)

        # Check database cache
        cached_result = self.database.get_cached_result(
            file_hash, model_version, processing_type
        )

        return cached_result

    def cache_ai_result(
        self, file_path: str, model_version: str, processing_type: str, result: Dict
    ):
        """Cache AI processing result"""
        file_hash = self.compute_file_hash(file_path)

        self.database.cache_ai_result(file_hash, model_version, processing_type, result)

    def clear_file_cache(self, file_path: str):
        """Clear cache for a specific file"""
        if file_path in self._file_hash_cache:
            del self._file_hash_cache[file_path]
        self.get_file_metadata.cache_clear()

    def clear_all_caches(self):
        """Clear all caches"""
        self._file_hash_cache.clear()
        self.get_file_metadata.cache_clear()
        # Optionally clear database caches
        self.database.cleanup_old_cache()


class MemoryManager:
    """Manages memory usage during file operations"""

    def __init__(self, max_memory_percent: float = 75.0):
        self.max_memory_percent = max_memory_percent
        self.batch_sizes = {"small": 1000, "medium": 500, "large": 100}

    def get_memory_usage(self) -> float:
        """Get current memory usage percentage"""
        import psutil

        process = psutil.Process(os.getpid())
        return process.memory_percent()

    def get_batch_size(self, file_sizes: List[int]) -> int:
        """Determine appropriate batch size based on file sizes"""
        avg_size = sum(file_sizes) / len(file_sizes)

        if avg_size < 1024 * 1024:  # < 1MB
            return self.batch_sizes["small"]
        elif avg_size < 10 * 1024 * 1024:  # < 10MB
            return self.batch_sizes["medium"]
        else:
            return self.batch_sizes["large"]

    def check_memory_threshold(self) -> bool:
        """Check if memory usage is below threshold"""
        return self.get_memory_usage() < self.max_memory_percent

    def wait_for_memory(self):
        """Wait until memory usage is below threshold"""
        import time

        while not self.check_memory_threshold():
            time.sleep(1)
