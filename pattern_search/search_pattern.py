from __future__ import print_function
from subprocess import Popen, PIPE
import subprocess
import os
import re
import glob
import shutil
from Bio import Entrez
#from Bio import SeqIO
import pandas as pd
from pyfaidx import Fasta
from  more_itertools import unique_everseen
from subprocess import check_output
from http.client import HTTPException
import time
Entrez.email = "Your email id"
species_name = "mus musculus"

#variables
all_accession = []

#opening files to write
all_geneids_file = open('all_gene_ids.txt', 'w')
all_genename_geneid = open('all_genename_geneid.txt', 'w')
gene_information_file = open('gene_information_file.txt','w')
gene_information_file.write('Genename,Chromosome,nc_accession,Start_End,GeneID'+"\n")
fuzz_run_output_file = open('fuzz_run_output_file.txt', 'w')

patterns = ['CTTTGTTAT[GT][TC][TA][ATC]AT','CATTGTGAT[GT][TC][TA][ATC]AT','CAGGACGAT[GT][TC][TA][ATC]AT','CAGGGTGAT[GT][TC][TA][ATC]AT',
'TTTTGTAAT[GT][TC][TA][ATC]AT','GATTGTCAT[GT][TC][TA][ATC]AT','CATTACGAT[GT][TC][TA][ATC]AT','ATTTGTAAT[GT][TC][TA][ATC]AT']


# Given gene name (eg; ADAM28) and species name (mus musculus) it fetches their gene ids
def fetch_gene_ids(gene_name, species_name):
        print ("fetching the gene name:", gene_name)
        search_string = gene_name + "[Gene] AND " + species_name
        handle = Entrez.esearch(db="gene", term=search_string)
        record = Entrez.read(handle)
        ids = record['IdList']
        single_id = ', '.join(ids[0:1])
        return single_id


def extract_gene_information(gene_id):
        "This takes the gene id and fetches their fasta sequence"
        print ("Extracting the fasta sequence for the gene id:", gene_id)
        handle = Entrez.efetch(db="gene", id=gene_id, rettype="fasta", retmode="text")
        gene_information = handle.read()
        return gene_information


def format_gene_record(gene_information):
    lines = gene_information.split('\n')
    for line in lines:
        try:
            if line.startswith('Annotation:'):
                match = re.search('\Chromosome\s[\w+](.*)', line)
                match = match.group(0)
                match = match.replace(', complement', '')
                match = match.replace('(','')
                match = match.replace(')', '')
                match = match.split()
                chromosome = match[1]
                nc_accession = match[2]
                start_end = match[3]
                return nc_accession, chromosome, start_end

        except Exception as e:
            print (e)
            pass

def check_length_gene_record(nc_accession,chromosome,start_end):
    if nc_accession == 'None' and \
       chromosome == 'None' and \
        start_end == 'None':
        return False
    else:
        return True


def check_unique(nc_accession):
    if nc_accession in all_accession:
        print ("This NC accession number downloaded already")
        return False
    else:
        all_accession.append(nc_accession)
        print("This NC accession number is new")
        return True


def extract_fasta_sequence(nc_accession):
    while True:
        try:
            "This takes the gene id and fetches their fasta sequence"
            print("Extracting the fasta sequence for the nc_accession:", nc_accession)
            handle = Entrez.efetch(db="nucleotide", id=nc_accession, rettype="fasta", retmode="text")
            record = handle.read()
            return record
        except HTTPException as e:
            print("Trying again ...")
            continue


def save_nc_accession(nc_accession, record):
    filename = nc_accession.rstrip() + ".txt"
    with open(filename, 'w') as nc_accession:
        nc_accession.write("%s" % record)

def split_fasta_file(gene, geneid, nc_accession, chromosome, start_end):
    try:
        start, end = start_end.split("..")
        filename = start + "_" + end
        filename = filename + ".fasta"
        start = int(start)
        end = int(end)
        new_start = start
        start = start - 50000
        end = end + 10000

        if start < 0:
            start = new_start
            end = end
        writefile = open(filename, 'w')
        genes = Fasta(nc_accession + ".txt")
        title = list(genes.keys())
        save_file = genes[(title[0])][start:end]
        start_sequence = genes[title[0]][start:end].start
        end_sequence = genes[title[0]][start:end].end
        save_title = ">" + gene + "|" + geneid + "|" + nc_accession + "|" + chromosome + "|" \
                     + str(start_sequence) + "|" + str(end_sequence) + "\n"
        writefile.write(save_title)
        writefile.write(str(save_file))
        return True
    except:
        data = open(filename, 'r').read()
        print ("There is some problem in this file", filename)
        print ("filename,starting sequence,ending sequence", filename, start, end)
        print("Total number of nucletoides are:", len(data))
        return False


def fetch_name_by_pattern(pattern):
    patterns_dictionary = {'CTTTGTTAT[GT][TC][TA][ATC]AT': 'FGF4_OCT4',
                           'CATTGTGAT[GT][TC][TA][ATC]AT': 'SOX2_OCT4',
                           'CAGGACGAT[GT][TC][TA][ATC]AT': 'MUTANT_GGAC_OCT4',
                           'CAGGGTGAT[GT][TC][TA][ATC]AT': 'MUTANT_GG_OCT4',
                           'TTTTGTAAT[GT][TC][TA][ATC]AT': 'MUTANT_TT_OCT4',
                           'GATTGTCAT[GT][TC][TA][ATC]AT': 'MUTANT_GA_OCT4',
                           'CATTACGAT[GT][TC][TA][ATC]AT': 'MUTANT_AC_OCT4',
                           'ATTTGTAAT[GT][TC][TA][ATC]AT': 'DPPA4_OCT4'}

    return patterns_dictionary[pattern]


def run_fuzz(filename,pattern):
    fasta_filename = filename+".fasta"
    name = fetch_name_by_pattern(str(pattern))
    out_name =  name + '_' + filename + '_fuzz_output' + '.txt'
    cmd = ['fuzznuc', '-sequence', fasta_filename, '-pattern',  pattern, '-outfile', out_name]
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    (out, err) = p.communicate()
    return out_name


def filename_with_hits(filename):
        textfile = open(filename, 'r')
        lines = textfile.read()
        textfile.close()
        matches = re.findall("\# Sequence", lines)
        matches1 = re.findall("\# HitCount", lines)

        if matches and matches1:
            return True
        else:
            return False

def format_fuzz_results(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            line = line.rstrip('\r\n')
            if line.startswith('# Sequence'):
                match = re.search(r'\sfrom\:\s\d\s+to\:\s\d+', line)
                match = match.group(0)
                match = re.findall(r'\d+', match)
                start_sequence = match[0]
                end_sequence = match[1]

            elif line.startswith('# HitCount'):
                match = re.search(r'\d+', line)
                hitcount = match.group(0)

            elif 'Start' in line:
                line = line[index]
                next_line = lines[index+1]
                next_line = next_line.split()
                next_line[3] = next_line[3].replace('pattern:', '')
                start = next_line[0]
                end = next_line[1]
                pattern1 = next_line[3]
                pattern2 = next_line[5]

        return start_sequence,end_sequence, hitcount, start,end, pattern1,pattern2


with open("gene.txt") as genes:
    for gene in genes:
        gene = gene.strip()
        geneid = fetch_gene_ids(gene, species_name)
        if geneid is not None:
            gene_information = extract_gene_information(geneid)
        if_data = format_gene_record(gene_information)
        if if_data is not None:
            nc_accession, chromosome, start_end = format_gene_record(gene_information)

        check_any_empty_values = check_length_gene_record(nc_accession,chromosome,start_end)

        if check_any_empty_values:
            check_repeat = check_unique(nc_accession)
            if check_repeat:
                record = extract_fasta_sequence(nc_accession)
                if record:
                    save_nc_accession(nc_accession, record)

            data = split_fasta_file(gene, geneid, nc_accession, chromosome, start_end)
            if data:
                for pattern in patterns:
                    filename = start_end.replace('..', '_')
                    print ("Running fuzz now for the pattern", pattern)
                    out_name = run_fuzz(filename, pattern)
                    if filename_with_hits(out_name):
                        print ("This is having some results",out_name)
                        start_sequence, end_sequence, hitcount, start, end, pattern1, pattern2 = format_fuzz_results(
                                out_name)
                        pattern1 = fetch_name_by_pattern(pattern1)
                        print (gene, geneid, nc_accession, chromosome, start_end, \
                             hitcount, start, end, pattern1, pattern2 + "\n")

                        gene_information_file.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}".format \
                                                        (gene, geneid, nc_accession, chromosome, start_end, \
                                                         hitcount, start, end, pattern1, pattern2 + "\n"))
