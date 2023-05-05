import re
import logging
import asyncio
from decimal import Decimal
from typing import List
from pathlib import Path
from functools import wraps
from collections import defaultdict

from IOHelper import lazy_file_reader


def show_running_info(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        logging.info(f"starting function {func.__name__} ...")
        decorated_func = func(*args, **kwargs)
        return decorated_func
    return with_logging


class ReportBuilder:
    def __init__(self) -> None:
        self.assigned_files = None
        self.divided_files = None
        self.mapped_results = None
        self.reduced_results = None
        self.assign_files_finished = False
        self.divide_files_finished = False
        self.map_finished = False
        self.reduce_finished = False

    def assign_files(self):
        pass

    def check_assigned_file_format(self):
        pass

    def divide_files(self):
        pass

    def map(self):
        pass

    def reduce(self):
        pass

    def build(self):
        pass


class FastqReportBuilder(ReportBuilder):
    @show_running_info
    def assign_files(self, *, paths: List[Path]) -> ReportBuilder:
        self.assigned_files = paths

        self.assign_files_finished = True
        return self

    @show_running_info
    def check_assigned_file_format(self) -> ReportBuilder:
        if not self.assign_files_finished:
            logging.error("\n\nYou must finish assign_files before checking file format.\n\n")

        def check_chunk(chunk: List[str]) -> None:
            if chunk[0][0] != "@" or chunk[2][0] != "+" or len(chunk[1]) != len(chunk[3]):
                raise Exception(f"Wrong input fastq data.\n{chunk}")

        for file in self.assigned_files:
            for chunk in lazy_file_reader(filename=file, chunk_size=4):
                check_chunk(chunk)

        return self

    @show_running_info
    def divide_files(self, *, lines_per_file: int = 0) -> ReportBuilder:
        if not self.assign_files_finished:
            logging.error("\n\nYou must finish assign_files before dividing them into smaller files.\n\n")

        if lines_per_file <= 0:
            self.divided_files = [self.assigned_files]
            self.divide_files_finished = True
            return self

        self.divided_files = []
        for file in self.assigned_files:
            index = 0
            divided_files = []
            for subfile in lazy_file_reader(filename=file, chunk_size=lines_per_file):
                index += 1
                temp_file_path = Path("temp/fastq/" + file.stem + "_" + str(index) + file.suffix)
                temp_file_path.parent.mkdir(parents=True, exist_ok=True)
                temp_file_path.write_text("\n".join(subfile).rstrip(), encoding="utf-8")
                divided_files.append(temp_file_path)
            self.divided_files.append(divided_files)

        self.divide_files_finished = True
        return self

    @show_running_info
    async def map(self) -> ReportBuilder:
        if not self.divide_files_finished:
            logging.error("\n\nYou must finish divide_files before mapping a funcion on them.\n\n")

        async def get_long_sequence_count(file: Path):
            long_sequence_count = 0
            total_count = 0
            for chunk in lazy_file_reader(filename=file, chunk_size=4):
                total_count += 1
                if len(chunk[1]) > 30:
                    long_sequence_count += 1
            return (long_sequence_count, total_count)

        tasks = [get_long_sequence_count(file)
                 for file_group in self.divided_files
                 for file in file_group]
        self.mapped_results = await asyncio.gather(*tasks, return_exceptions=True)

        self.map_finished = True
        return self

    @show_running_info
    def reduce(self) -> ReportBuilder:
        if not self.map_finished:
            logging.error("\n\nYou must finish map before reducing the results.\n\n")

        pointer_of_map_results = 0
        self.reduced_results = []
        for file_group in self.divided_files:
            sum_of_long_sequence = 0
            total_sequence_count = 0
            for _ in file_group:
                sum_of_long_sequence += self.mapped_results[pointer_of_map_results][0]
                total_sequence_count += self.mapped_results[pointer_of_map_results][1]
                pointer_of_map_results += 1
            self.reduced_results.append(sum_of_long_sequence / total_sequence_count)

        self.reduce_finished = True
        return self

    @show_running_info
    def build(self, *, show_path: bool = False, clean_temp_files: bool = True) -> ReportBuilder:
        if not self.reduce_finished:
            logging.error("\n\nYou must finish reduce before generating a report.\n\n")

        if clean_temp_files:
            for path in Path(".").glob("temp/fastq/*"):
                path.unlink()
            for path in Path(".").glob("temp/fastq/"):
                path.rmdir()

        report_data = list(zip(self.assigned_files, self.reduced_results))

        print("\nThe percent of sequences are greater than 30 nucleotides long for each file:")
        for datum in report_data:
            file = datum[0] if show_path else datum[0].name
            percentage = f"{datum[1]:.4%}"
            print(f"{file}: {percentage}")

        return self


class FastaReportBuilder(ReportBuilder):
    @show_running_info
    def assign_files(self, *, paths: List[Path]) -> ReportBuilder:
        self.assigned_files = paths

        self.assign_files_finished = True
        return self

    @show_running_info
    def check_assigned_file_format(self) -> ReportBuilder:
        if not self.assign_files_finished:
            logging.error("\n\nYou must finish assign_files before checking file format.\n\n")

        def check_chunk(chunk: List[str]) -> None:
            if chunk[0][0] != ">":
                raise Exception(f"Wrong input fasta data.\n{chunk}")

        for file in self.assigned_files:
            for chunk in lazy_file_reader(filename=file, chunk_size=2):
                check_chunk(chunk)

        return self

    @show_running_info
    def divide_files(self, *, lines_per_file: int = 0) -> ReportBuilder:
        if not self.assign_files_finished:
            logging.error("\n\nYou must finish assign_files before dividing them into smaller files.\n\n")

        if lines_per_file <= 0:
            self.divided_files = [self.assigned_files]
            self.divide_files_finished = True
            return self

        self.divided_files = []
        for file in self.assigned_files:
            index = 0
            divided_files = []
            for subfile in lazy_file_reader(filename=file, chunk_size=lines_per_file):
                index += 1
                temp_file_path = Path("temp/fasta/" + file.stem + "_" + str(index) + file.suffix)
                temp_file_path.parent.mkdir(parents=True, exist_ok=True)
                temp_file_path.write_text("\n".join(subfile).rstrip(), encoding="utf-8")
                divided_files.append(temp_file_path)
            self.divided_files.append(divided_files)

        self.divide_files_finished = True
        return self

    @show_running_info
    async def map(self) -> ReportBuilder:
        if not self.divide_files_finished:
            logging.error("\n\nYou must finish divide_files before mapping a funcion on them.\n\n")

        async def get_sequence_occurrence(file: Path):
            sequence_occurrence = defaultdict(int)
            for chunk in lazy_file_reader(filename=file, chunk_size=2):
                sequence_occurrence[chunk[1]] += 1
            return sequence_occurrence

        tasks = [get_sequence_occurrence(file)
                 for file_group in self.divided_files
                 for file in file_group]
        self.mapped_results = await asyncio.gather(*tasks, return_exceptions=True)

        self.map_finished = True
        return self

    @show_running_info
    def reduce(self) -> ReportBuilder:
        if not self.map_finished:
            logging.error("\n\nYou must finish map before reducing the results.\n\n")

        pointer_of_map_results = 0
        self.reduced_results = []
        for file_group in self.divided_files:
            merged_results = defaultdict(int)
            for _ in file_group:
                mapped_result = self.mapped_results[pointer_of_map_results]
                for key in mapped_result:
                    merged_results[key] += mapped_result[key]
                pointer_of_map_results += 1
            [self.reduced_results.append((sequence, occurrence)) for sequence, occurrence in merged_results.items()]

        self.reduce_finished = True
        return self

    @show_running_info
    def build(self, *, clean_temp_files: bool = True) -> ReportBuilder:
        if not self.reduce_finished:
            logging.error("\n\nYou must finish reduce before generating a report.\n\n")

        if clean_temp_files:
            for path in Path(".").glob("temp/fasta/*"):
                path.unlink()
            for path in Path(".").glob("temp/fasta/"):
                path.rmdir()

        report_data = sorted(self.reduced_results, reverse=True, key=lambda x: (x[1], x[0]))[0:10]

        print("\n10 most frequent sequences and their counts in the file:")
        for datum in report_data:
            print(f"{datum[0]}: {datum[1]}")

        return self


class AnnotationReportBuilder(ReportBuilder):
    @show_running_info
    def assign_files(self, *, search_candidates_file: Path, annotation_reference_file: Path) -> ReportBuilder:
        self.assigned_files = [search_candidates_file, annotation_reference_file]

        self.assign_files_finished = True
        return self

    @show_running_info
    def check_assigned_file_format(self) -> ReportBuilder:
        logging.info("\nNo format check applied.\n")
        return self

    @show_running_info
    def divide_files(self) -> ReportBuilder:
        if not self.assign_files_finished:
            logging.error("\n\nYou must finish assign_files before dividing them into smaller files.\n\n")

        self.divided_files = defaultdict(list)
        for file in self.assigned_files:
            divided_files = defaultdict(set)
            for subfile in lazy_file_reader(filename=file, chunk_size=1):
                chromosome = subfile[0].split("\t")[0]
                temp_file_path = Path("temp/lookup/" + chromosome + "/" + file.name)
                temp_file_path.parent.mkdir(parents=True, exist_ok=True)
                temp_file_path.open(mode="a+", encoding="utf-8").write(subfile[0] + "\n")
                divided_files[chromosome].add(temp_file_path)
            [self.divided_files[key].append(path) for key, path in divided_files.items()]

        self.divide_files_finished = True
        return self

    @show_running_info
    async def map(self) -> ReportBuilder:
        if not self.divide_files_finished:
            logging.error("\n\nYou must finish divide_files before mapping a funcion on them.\n\n")

        pattern = r'gene_id\s+"([\w_-]+)";'

        def scan(candidate: str, annotation: str):
            candidate_coordinate = candidate.strip().split("\t")[1]
            annotation_split = annotation.strip().split("\t")
            annotation_starting_coordinate = annotation_split[3]
            annotation_ending_coordinate = annotation_split[4]

            if int(candidate_coordinate) < int(annotation_starting_coordinate) or int(candidate_coordinate) >= int(annotation_ending_coordinate):
                return

            match = re.search(pattern, annotation)
            return match.group(1)

        async def get_annotation(search_candidates_file: Path, annotation_reference_file: Path):
            # 05/04/2023 both coordinates_to_annotate.txt and hg19_annotations.gtf file has a lot of duplicated data,
            # using set can clean duplicated output
            annotated_candidates = set()
            for candidate in lazy_file_reader(filename=search_candidates_file, chunk_size=1):
                for annotation in lazy_file_reader(filename=annotation_reference_file, chunk_size=1):
                    # 05/04/2023: lazy_file_reader generates list of strings, so "[0]" is needed here to get chromosome
                    annotation = scan(candidate[0], annotation[0])
                    chromosome, coordinate = candidate[0].split("\t")
                    if annotation:
                        annotated_candidates.add(f"{chromosome}\t{coordinate}\t{annotation}")
                    else:
                        annotated_candidates.add(f"{chromosome}\t{coordinate}\tnot matched")

            return "\n".join(list(annotated_candidates))

        tasks = []
        for files in self.divided_files.values():
            if len(files) < 2:
                continue
            # 05/04/2023 when dividing files, used set to avoid duplicate records. now we must unpack them
            search_candidates_file = list(files[0])[0]
            annotation_reference_file = list(files[1])[0]
            tasks.append(get_annotation(search_candidates_file, annotation_reference_file))
        self.mapped_results = await asyncio.gather(*tasks, return_exceptions=True)

        self.map_finished = True
        return self

    @show_running_info
    def reduce(self) -> ReportBuilder:
        if not self.map_finished:
            logging.error("\n\nYou must finish map before reducing the results.\n\n")

        self.reduced_results = "\n".join(self.mapped_results)

        self.reduce_finished = True
        return self

    @show_running_info
    def build(self, *, clean_temp_files: bool = True) -> ReportBuilder:
        if not self.reduce_finished:
            logging.error("\n\nYou must finish reduce before generating a report.\n\n")

        if clean_temp_files:
            for path in Path(".").glob("temp/lookup/*/*"):
                path.unlink()
            for path in Path(".").glob("temp/lookup/*"):
                path.rmdir()

        Path("./annotated_file").write_text(self.reduced_results)
        print("\nA file \"annotated_file\" is created, it shows distinct pairs of chromosome, coordinate and annotation.")
        return self


class IntervalMeanReportBuilder(ReportBuilder):
    @show_running_info
    def assign_files(self, *, paths: List[Path]) -> ReportBuilder:
        self.assigned_files = paths

        self.assign_files_finished = True
        return self

    @show_running_info
    def check_assigned_file_format(self) -> ReportBuilder:
        logging.info("\nNo format check applied.\n")
        return self

    @show_running_info
    def divide_files(self, *, lines_per_file: int = 0) -> ReportBuilder:
        if not self.assign_files_finished:
            logging.error("\n\nYou must finish assign_files before dividing them into smaller files.\n\n")

        if lines_per_file <= 0:
            self.divided_files = [self.assigned_files]
            self.divide_files_finished = True
            return self

        self.divided_files = []
        for file in self.assigned_files:
            index = 0
            divided_files = []
            for subfile in lazy_file_reader(filename=file, chunk_size=lines_per_file):
                index += 1
                temp_file_path = Path("temp/interval_mean/" + file.stem + "_" + str(index) + file.suffix)
                temp_file_path.parent.mkdir(parents=True, exist_ok=True)
                temp_file_path.write_text("\n".join(subfile).rstrip(), encoding="utf-8")
                # 05/04/2023 since we can have a very big file as input, clean file head at here can save us time and memory
                if index == 1:
                    with temp_file_path.open("r+") as f:
                        # Move the file pointer to the start of the second line
                        f.seek(f.readline().__len__())
                        # Overwrite the file with the remaining contents
                        remaining_content = f.read()
                        f.seek(0)
                        f.write(remaining_content)
                        f.truncate()
                divided_files.append(temp_file_path)
            self.divided_files.append(divided_files)

        self.divide_files_finished = True
        return self

    @show_running_info
    async def map(self) -> ReportBuilder:
        if not self.divide_files_finished:
            logging.error("\n\nYou must finish divide_files before mapping a funcion on them.\n\n")

        async def get_interval_mean(file: Path):
            interval_data = [[Decimal(0), Decimal(0)] for _ in range(0, 10)]
            for data_line in lazy_file_reader(filename=file, chunk_size=1):
                # 05/04/2023 found pattern "\t\t" makes program die, solve it here
                data_line = data_line[0].strip().replace("\t\t", "\t").split("\t")
                # 05/04/2023 gc values range from 0 to 1 and we want 10 groups,
                # so the digit after float point can match the bin identifier
                bin_identifier = int(Decimal(data_line[5]) * 10)
                mean_coverage = Decimal(data_line[6])
                interval_data[bin_identifier][0] += mean_coverage
                interval_data[bin_identifier][1] += Decimal(1)
            return interval_data

        tasks = [get_interval_mean(file)
                 for file_group in self.divided_files
                 for file in file_group]
        self.mapped_results = await asyncio.gather(*tasks, return_exceptions=True)

        self.map_finished = True
        return self

    @show_running_info
    def reduce(self) -> ReportBuilder:
        if not self.map_finished:
            logging.error("\n\nYou must finish map before reducing the results.\n\n")

        self.reduced_results = [[Decimal(0), Decimal(0)] for _ in range(0, 10)]
        for data_group in self.mapped_results:
            pointer_of_map_results = 0
            for data in data_group:
                self.reduced_results[pointer_of_map_results][0] += data[0]
                self.reduced_results[pointer_of_map_results][1] += data[1]
                pointer_of_map_results += 1

        pointer_of_reduced_results = 0
        for data in self.reduced_results:
            sum_of_mean_target_coverage = data[0]
            number_of_mean_target_coverage = data[1]
            if not number_of_mean_target_coverage == Decimal("0"):
                self.reduced_results[pointer_of_reduced_results] = sum_of_mean_target_coverage / number_of_mean_target_coverage
            else:
                self.reduced_results[pointer_of_reduced_results] = Decimal("0")
            pointer_of_reduced_results += 1

        self.reduce_finished = True
        return self

    @show_running_info
    def build(self, *, show_path: bool = False, clean_temp_files: bool = True) -> ReportBuilder:
        if not self.reduce_finished:
            logging.error("\n\nYou must finish reduce before generating a report.\n\n")

        if clean_temp_files:
            for path in Path(".").glob("temp/interval_mean/*"):
                path.unlink()
            for path in Path(".").glob("temp/interval_mean/"):
                path.rmdir()

        print("\nThe mean target coverage for the intervals grouped by GC% bins:")
        pointer_of_reduced_results = 0
        for data in self.reduced_results:
            print(f"GC% bin {pointer_of_reduced_results}0-{pointer_of_reduced_results+1:2}0%: {data:>4.4f}")
            pointer_of_reduced_results += 1

        return self
