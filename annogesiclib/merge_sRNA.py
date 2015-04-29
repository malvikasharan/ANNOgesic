#!/usr/bin/python

import os	
import sys
import csv
import math
from annogesiclib.gff3 import Gff3Parser
from annogesiclib.coverage_detection import coverage_comparison, replicate_comparison
from annogesiclib.lib_reader import read_wig, read_libs

def modify_attributes(pre_srna, srna, srna_type, input_type):
    if srna_type == "UTR":
        if pre_srna.attributes["UTR_type"] != srna.attributes["UTR_type"]:
            if input_type == "pre":
                if "&" not in pre_srna.attributes["UTR_type"]:
                    pre_srna.attributes["UTR_type"] = \
                           "&".join([srna.attributes["UTR_type"], 
                                     pre_srna.attributes["UTR_type"]])
            else:
                if "&" not in pre_srna.attributes["UTR_type"]:
                    srna.attributes["UTR_type"] = \
                           "&".join([srna.attributes["UTR_type"],
                                     pre_srna.attributes["UTR_type"]])
                else:
                    srna.attributes["UTR_type"] = pre_srna.attributes["UTR_type"]

def detect_overlap(srna, pre_srna, srna_type, overlap):
    if (srna.seq_id == pre_srna.seq_id) and \
       (srna.strand == pre_srna.strand):
        if (pre_srna.start >= srna.start) and \
           (pre_srna.end <= srna.end):
            modify_attributes(pre_srna, srna, srna_type, None)
            overlap = True
        elif (pre_srna.start >= srna.start) and \
             (pre_srna.start <= srna.end) and \
             (pre_srna.end >= srna.end):
            modify_attributes(pre_srna, srna, srna_type, None)
            overlap = True
        elif (pre_srna.start <= srna.start) and \
             (pre_srna.end >= srna.start) and \
             (pre_srna.end <= srna.end):
            modify_attributes(pre_srna, srna, srna_type, None)
            overlap = True
        elif (pre_srna.start <= srna.start) and \
             (pre_srna.end >= srna.end):
            overlap = True
            modify_attributes(pre_srna, srna, srna_type, "pre")
    return overlap

def modify_overlap(pre_srna, srna):
    if (pre_srna.attributes["with_TSS"] == "NA") and \
       (srna.attributes["with_TSS"] != "NA"):
        pre_srna.attributes["with_TSS"] = srna.attributes["with_TSS"]
    elif (srna.attributes["with_TSS"] not in pre_srna.attributes["with_TSS"]) and \
         (srna.attributes["with_TSS"] != "NA"):
        pre_srna.attributes["with_TSS"] = "&".join([pre_srna.attributes["with_TSS"],
                                                    srna.attributes["with_TSS"]])
    if "UTR_type" in srna.attributes.keys():
        if (pre_srna.attributes["with_cleavage"] == "NA") and \
           (srna.attributes["with_cleavage"] != "NA"):
            pre_srna.attributes["with_cleavage"] = srna.attributes["with_cleavage"]
        elif (srna.attributes["with_cleavage"] not in pre_srna.attributes["with_cleavage"]) and \
             (srna.attributes["with_cleavage"] != "NA"):
            pre_srna.attributes["with_cleavage"] = \
            "&".join([pre_srna.attributes["with_cleavage"], srna.attributes["with_cleavage"]])
    if (srna.start < pre_srna.start):
            pre_srna.start = srna.start
    if (srna.end > pre_srna.end):
            pre_srna.end = srna.end
    return pre_srna

def merge_srna(srnas, final_srnas, srna_type):
    first = True
    for srna in srnas:
        if srna_type == "UTR":
            srna.source = "UTR_derived"
            srna.feature = "sRNA"
        else:
            srna.attributes["lib_type"] = srna.source.replace("_and_", "&")
            srna.source = "intergenic"
            if srna.attributes["with_TSS"] == "False":
                srna.attributes["with_TSS"] = "NA"
        overlap = False
        insist = False
        if first:
            first = False
            pre_srna = srna
        else:
            overlap = detect_overlap(srna, pre_srna, srna_type, overlap)
            if overlap:
                pre_srna = modify_overlap(pre_srna, srna)
            if overlap is not True:
                final_srnas.append(pre_srna)
                pre_srna = srna
    if overlap is not True:
        final_srnas.append(srna)

def read_gff(sRNA_file):
    datas = []
    for entry in Gff3Parser().entries(open(sRNA_file)):
        datas.append(entry)
    datas = sorted(datas, key=lambda k: (k.seq_id, k.start))
    return datas

def read_table(table_file, file_type):
    fh = open(table_file, "r")
    datas = []
    for row in csv.reader(fh, delimiter='\t'):
        datas.append(import_data(row, file_type))
    return datas

def merge_srna_gff(sRNA_utr, sRNA_inter, out_file):
    srnas = []
    out = open(out_file, "w")
    out.write("##gff-version 3\n")
    utrs = read_gff(sRNA_utr)
    inters = read_gff(sRNA_inter)
    num_srna = 0
    merge_srna(utrs, srnas, "UTR")
    merge_srna(inters, srnas, "inter")
    sort_srnas = sorted(srnas, key = lambda x: (x.seq_id, x.start))
    for srna in sort_srnas:
        srna.attributes["ID"] = "srna" + str(num_srna)
        name = '%0*d' % (5, num_srna)
        srna.attributes["Name"] = "sRNA_candidate_" + str(name)
        del srna.attributes["best_high_coverage"]
        del srna.attributes["best_low_coverage"]
        del srna.attributes["best_avg_coverage"]
        attribute_string = ";".join(
                          ["=".join(items) for items in srna.attributes.items()])
        srna.info_without_attributes = "\t".join([str(field) for field in [
                        srna.seq_id, srna.source, srna.feature, srna.start,
                        srna.end, srna.score, srna.strand, srna.phase]])
        out.write(srna.info_without_attributes + "\t" + attribute_string + "\n")
        num_srna += 1

def import_data(row, type_):
    if type_ == "inter":
        detail = row[11]
    elif type_ == "utr":
        detail = row[10]
    return {"strain": row[0], "name": row[1],
            "start": int(row[2]), "end": int(row[3]),
            "strand": row[4], "libs": row[5],
            "detect": row[6], "avg": row[7],
            "high": row[8], "low": row[9],
            "detail": detail}

def compare_table(srna, tables, type_, wigs_f, wigs_r, template_texs, 
                  table_best, out, tex_notex, replicates):
    detect = False
    tss_pro = get_tss_pro(type_, srna)
    for table in tables:
        if (srna.seq_id == table["strain"]) and \
           (srna.strand == table["strand"]) and \
           (srna.start == table["start"]) and \
           (srna.end == table["end"]):
            detect = True
            out.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\n".format(
                      srna.seq_id, srna.attributes["Name"], srna.start, srna.end,
                      srna.strand, table["libs"], table["detect"], tss_pro,
                      table["avg"], table["high"], table["low"], table["detail"]))
            break
    if detect is not True:
        if srna.strand == "+":
            covers = get_coverage(wigs_f, srna.seq_id, srna.strand, srna.start, srna.end)
        else:
            covers = get_coverage(wigs_r, srna.seq_id, srna.strand, srna.start, srna.end)
        srna_datas = replicate_comparison(covers, template_texs, srna.strand,
                                  None, tex_notex, replicates, 
                                  "merge_sRNA", None, None, None)
        if srna_datas is not None:
            out.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t".format(
                       srna.seq_id, srna.attributes["Name"], srna.start, srna.end,
                       srna.strand, ";".join(srna_datas["conds"].keys()),
                       ";".join(srna_datas["conds"].values()), tss_pro,
                       srna_datas["best"], srna_datas["high"], srna_datas["low"]))
            if table_best is False:
                first = True
                for data in srna_datas["detail"]:
                    if first:
                        out.write("{0}(avg={1};high={2};low={3})".format(
                                  data["track"], data["avg"], data["high"], data["low"]))
                        first = False
                    else:
                        out.write(";{0}(avg={1};high={2};low={3})".format(
                                  data["track"], data["avg"], data["high"], data["low"]))
            else:
                out.write("{0}(avg={1};high={2};low={3})".format(
                          srna_datas["track"], srna_datas["best"],
                          srna_datas["high"], srna_datas["low"]))
        out.write("\n")

def get_coverage(wigs, strain, strand, start, end):
    cover_sets = {"high": -1, "low": -1, "total": 0, "diff": 0}
    poss = {"high": 0, "low": 0, "pos": 0}
    srna_covers = {}
    for wig_strain, conds in wigs.items():
        if wig_strain == strain:
            for cond, tracks in conds.items():
                srna_covers[cond] = []
                for track, covers in tracks.items():
                    cover_sets["total"] = 0
                    cover_sets["diff"] = 0
                    first = True
                    if strand == "+":
                        covers = covers[start-2:end+1]
                    elif strand == "-":
                        covers = reversed(covers[start-2:end+1])
                    for cover in covers:
                        if (cover["strand"] == strand):
                            if (start <= cover["pos"]) and \
                               (end >= cover["pos"]):
                                cover_sets["total"] = cover_sets["total"] + cover["coverage"]
                                first = coverage_comparison(
                                        cover, cover_sets, poss, first, strand)
                            else:
                                if (strand == "+") and (cover["pos"] > end):
                                    cover_sets["pos"] = cover["pos"]
                                    break
                                elif (strand == "-") and (cover["pos"] < start):
                                    cover_sets["pos"] = cover["pos"]
                                    break
                    avg = cover_sets["total"] / float(end - start + 1)
                    srna_covers[cond].append({"track": track, "high": cover_sets["high"],
                                              "low": cover_sets["low"], "avg": avg,
                                              "pos": poss["pos"], "type": cover["type"]})
    return srna_covers

def get_tss_pro(type_, srna):
    if type_ == "utr":
        if (srna.attributes["with_TSS"] != "NA") and \
           (srna.attributes["with_cleavage"] != "NA"):
            tss_pro = ";".join([srna.attributes["with_TSS"], srna.attributes["with_cleavage"]])
        elif (srna.attributes["with_TSS"] != "NA"):
            tss_pro = srna.attributes["with_TSS"]
        elif srna.attributes["with_cleavage"] != "NA":
            tss_pro = srna.attributes["with_cleavage"]
        else:
            tss_pro = "None"
        tss_pro = tss_pro.replace("&", ";")
    elif type_ == "inter":
        if (srna.attributes["with_TSS"] != "NA"):
            tss_pro = srna.attributes["with_TSS"].replace("&", ";")
        else:
            tss_pro = "None"
    return tss_pro

def merge_srna_table(sRNA_file, inter_table, utr_table, wig_f_file, wig_r_file,
                     wig_folder, input_libs, tex_notex, replicates, table_best,
                     out_file):
    wigs_f = {}
    wigs_r = {}
    libs = []
    texs = {}
    read_libs(libs, texs, input_libs, wig_folder)
    read_wig(wigs_f, wig_f_file, "+", libs)
    read_wig(wigs_r, wig_r_file, "-", libs)
    srnas = read_gff(sRNA_file)
    inters = read_table(inter_table, "inter")
    utrs = read_table(utr_table, "utr")
    out = open(out_file, "w")
    for srna in srnas:
        if srna.source == "UTR_derived":
            compare_table(srna, utrs, "utr", wigs_f, wigs_r, texs,
                          table_best, out, tex_notex, replicates)
        elif srna.source == "intergenic":
            compare_table(srna, inters, "inter", wigs_f, wigs_r, texs,
                          table_best, out, tex_notex, replicates)