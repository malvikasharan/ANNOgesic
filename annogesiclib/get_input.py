import os
import csv
import shutil
from subprocess import call
from annogesiclib.seq_editer import SeqEditer


def wget(input_folder, ftp, files_type):
    os.system(" ".join(["wget", "-cP", input_folder, ftp + "/*" + files_type]))


def deal_detect(input_file, file_path, change, input_folder):
    if change:
        shutil.move(input_file, file_path)
        change = False
    SeqEditer().modify_header(file_path)
    with open(os.path.join(file_path)) as fh:
        for line in fh:
            line = line.strip()
            if line.startswith(">"):
                seq_name = line[1:]
    shutil.move(file_path,
                os.path.join(input_folder, seq_name + ".fa"))
    return change, seq_name


def get_file(ftp, input_folder, files_type, target):
    detect = False
    filename = None
    wget(input_folder, ftp, files_type)
    for file_ in os.listdir(input_folder):
        input_file = os.path.join(input_folder, file_)
        if (file_[-3:] == "fna"):
            filename = file_[0:-3] + "fa"
            detect = True
            change = True
        elif (file_[-5:] == "fasta"):
            filename = file_[0:-5] + "fa"
            detect = True
            change = True
        elif (file_[-2:] == "fa"):
            filename = file_[0:-2] + "fa"
            detect = True
            change = False
        elif (file_[-6:] == "fna.gz") and ("_genomic" in file_):
            if ("_cds_from_genomic" in file_) or (
                    "_rna_from_genomic" in file_):
                os.remove(input_file)
            else:
                filename = file_[0:-6] + "fa"
                detect = True
                change = True
                call(["gunzip", input_file])
                input_file = input_file[:-3]
        elif (file_[-6:] == "gff.gz") or (file_[-3:] == "gff"):
            if ("_genomic" in file_) and (file_[-6:] == "gff.gz"):
                call(["gunzip", input_file])
                input_file = input_file[:-3]
            fh = open(input_file, "r")
            for row in csv.reader(fh, delimiter='\t'):
                if not row[0].startswith("#"):
                    gff_name = row[0]
                    break
            os.rename(input_file, os.path.join(input_folder,
                                               gff_name + ".gff"))
            fh.close()
        elif (file_[-3:] == "gbk") or (file_[-7:] == "gbff.gz") or (
                file_[-4:] == "gbff"):
            if (file_[-7:] == "gbff.gz") and ("_genomic" in file_):
                call(["gunzip", input_file])
                input_file = input_file[:-3]
            with open(input_file, "r") as g_f:
                for line in g_f:
                    if line[0:7] == "VERSION":
                        data = line[12:].split(" ")
                        break
            os.rename(input_file, os.path.join(input_folder, data[0] + ".gbk"))
        if detect:
            detect = False
            change, seq_name = deal_detect(input_file, filename,
                                           change, input_folder)
