import logging
import asyncio
import argparse
from ReportBuilder import FastqReportBuilder, FastaReportBuilder, AnnotationReportBuilder, IntervalMeanReportBuilder
from IOHelper import FileFinder

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


parser = argparse.ArgumentParser(description='Process some files based on mode.')

parser.add_argument('--mode', choices=['fastq', 'fasta', 'annotation', 'interval_mean'], required=True, help='Choose mode to run')
parser.add_argument('--fastq-directory', '--fq', help='Directory containing fastq files')
parser.add_argument('--fasta-directory', '--fa', help='Directory containing fasta files')
parser.add_argument('--coordinates_to_annotate_directory', '--ctoa', help='File containing coordinates to annotate')
parser.add_argument('--hg19_annotations_directory', '--hg19', help='File containing hg19 annotations')
parser.add_argument('--hs_intervals_directory', '--intvl', help='File containing hs intervals')

args = parser.parse_args()

if args.mode == 'fastq':
    if args.fastq_directory or args.fq:
        fastq_dir = args.fastq_directory or args.fq

        fastq_report_builder = FastqReportBuilder()
        fastq_file = FileFinder(input_path=fastq_dir)

        fastq_report_builder.assign_files(paths=fastq_file.find_files_by_extension(extension="fastq")) \
            .check_assigned_file_format() \
            .divide_files(lines_per_file=1000)
        asyncio.run(fastq_report_builder.map())
        fastq_report_builder.reduce().build()
    else:
        parser.error('--fastq-directory or --fq is required when --mode is fastq')

elif args.mode == 'fasta':
    if args.fasta_directory or args.fa:
        fasta_dir = args.fasta_directory or args.fa

        fasta_report_builder = FastaReportBuilder()
        fasta_file = FileFinder(input_path=fasta_dir)

        fasta_report_builder.assign_files(paths=fasta_file.list_files()) \
            .check_assigned_file_format() \
            .divide_files(lines_per_file=1000)
        asyncio.run(fasta_report_builder.map())
        fasta_report_builder.reduce() \
            .build()
    else:
        parser.error('--fasta-directory or --fa is required when --mode is fasta')

elif args.mode == 'annotation':
    if args.coordinates_to_annotate_directory or args.ctoa and args.hg19_annotations_directory or args.hg19:
        ctoa_dir = args.coordinates_to_annotate_directory or args.ctoa
        hg19_dir = args.hg19_annotations_directory or args.hg19

        annotation_report_builder = AnnotationReportBuilder()
        coordinate_file = FileFinder(input_path=ctoa_dir)
        annotation_reference = FileFinder(input_path=hg19_dir)
        annotation_report_builder.assign_files(search_candidates_file=coordinate_file.list_files()[0], annotation_reference_file=annotation_reference.list_files()[0]) \
            .divide_files()
        asyncio.run(annotation_report_builder.map())
        annotation_report_builder.reduce().build()
    else:
        parser.error('--coordinates_to_annotate_directory or --ctoa and --hg19_annotations_directory or --hg19 are required when --mode is annotation')

elif args.mode == 'interval_mean':
    if args.hs_intervals_directory or args.intvl:
        intervals_dir = args.hs_intervals_directory or args.intvl

        interval_mean_report_builder = IntervalMeanReportBuilder()
        interval_data_file = FileFinder(input_path=intervals_dir)

        interval_mean_report_builder.assign_files(paths=interval_data_file.list_files()) \
            .divide_files(lines_per_file=1000)
        asyncio.run(interval_mean_report_builder.map())
        interval_mean_report_builder.reduce() \
            .build()
    else:
        parser.error('--hs_intervals_file or --intvl is required when --mode is interval_mean')


# -----
# fastq_report_builder = FastqReportBuilder()
# fastq_file = FileFinder(input_path="./sample_files/")

# fastq_report_builder.assign_files(paths=fastq_file.find_files_by_extension(extension="fastq")) \
#     .check_assigned_file_format() \
#     .divide_files(lines_per_file=1000)
# asyncio.run(fastq_report_builder.map())
# fastq_report_builder.reduce().build()
# -----
# fasta_report_builder = FastaReportBuilder()
# fasta_file = FileFinder(input_path="./sample_files/fasta/sample.fasta")

# fasta_report_builder.assign_files(paths=fasta_file.list_files()) \
#     .check_assigned_file_format() \
#     .divide_files(lines_per_file=1000)
# asyncio.run(fasta_report_builder.map())
# fasta_report_builder.reduce() \
#     .build()
# -----
# annotation_report_builder = AnnotationReportBuilder()
# coordinate_file = FileFinder(input_path="./sample_files/annotate/coordinates_to_annotate.txt")
# annotation_reference = FileFinder(input_path="./sample_files/gtf/hg19_annotations.gtf")

# annotation_report_builder.assign_files(search_candidates_file=coordinate_file.list_files()[0], annotation_reference_file=annotation_reference.list_files()[0]) \
#     .divide_files()
# asyncio.run(annotation_report_builder.map())
# annotation_report_builder.reduce().build()
# -----
# interval_mean_report_builder = IntervalMeanReportBuilder()
# interval_data_file = FileFinder(input_path="./sample_files/Example.hs_intervals.txt")

# interval_mean_report_builder.assign_files(paths=interval_data_file.list_files()) \
#     .divide_files(lines_per_file=1000)
# asyncio.run(interval_mean_report_builder.map())
# interval_mean_report_builder.reduce() \
#     .build()
