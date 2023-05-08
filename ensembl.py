import sys
import json
import requests
import argparse


parser = argparse.ArgumentParser(description='Process variant information')
parser.add_argument('--variants', '-v', type=str, nargs='+', help='variant ids separated by space')
parser.add_argument('--variant-directory', '-vdir', type=str, help='directory to variant file')

args = parser.parse_args()
variants = []

if args.variants is None and args.variant_directory is None:
    parser.error('At least one of --variants or --variant-directory is required')

if args.variants is not None and args.variant_directory is not None:
    parser.error('Only one of --variants or --variant-directory is allowed')

if args.variant_directory is not None:
    with open(args.variant_directory, 'r') as f:
        variants = f.readlines()
        variants = [v.strip() for v in variants]

if args.variants is not None:
    variants = args.variants


server = "https://rest.ensembl.org"
ext = "/vep/human/id"
headers = {"Content-Type": "application/json", "Accept": "application/json"}
payload_data = {"ids": variants}
response = requests.post(server + ext, headers=headers, data=json.dumps(payload_data))

if not response.ok:
    response.raise_for_status()
    sys.exit()

json_data = response.json()

header = "variant id\ttranscript id\tstart\tend\tallele(s)\tgene symbol\tgene id\tconsequence"
print(header)
for data in json_data:
    variant_id = data["input"]
    transcript_id = ""
    start = data["start"]
    end = data["end"]
    alleles = data["allele_string"]
    gene_symbol = ""
    gene_id = ""
    consequence_term = ""
    if not data["most_severe_consequence"] == "?":
        transcript_id = ""
        gene_symbol = ""
        gene_id = ""
        for consequence in data["transcript_consequences"]:
            transcript_id = consequence["transcript_id"]
            gene_symbol = consequence["gene_symbol"]
            gene_id = consequence["gene_id"]
            consequence_term = ""
            for term in consequence["consequence_terms"]:
                consequence_term = term

                print(f"{variant_id}\t{transcript_id}\t{start}\t{end}\t{alleles}\t{gene_symbol}\t{gene_id}\t{consequence_term}")
    else:
        print(f"{variant_id}\t{transcript_id}\t{start}\t{end}\t{alleles}\t{gene_symbol}\t{gene_id}\t{consequence_term}")
