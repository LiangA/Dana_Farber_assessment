from typing import List
from pathlib import Path


class FileFinder:
    def __init__(self, *, input_path: str):
        self.path = Path(input_path)
        self.files_in_path = self.list_files()

    def list_files(self) -> List[Path]:
        """
        Recursively make a list of all file paths found in a directory.
        If the input is a file, output a list with only one file path.
        """
        files = []
        if self.path.is_file():
            return [self.path]
        else:
            for file in self.path.iterdir():
                files += FileFinder(input_path=str(file)).files_in_path
            return files

    def find_files_by_extension(self, *, extension: str, case_insensitive: bool = True) -> List[Path]:
        """
        Find all file paths with a given extension in a list of filenames.
        Returns a list of the matching filenames.
        """
        extension = extension.lstrip(".")

        if case_insensitive:
            extension = extension.lower()

        return list(Path(self.path).glob(f"**/*.{extension}"))


def lazy_file_reader(filename: Path, chunk_size: int):
    with open(filename, "r") as file:
        while True:
            lines = [file.readline().strip() for _ in range(chunk_size)]
            if not any(lines):
                break
            yield lines
