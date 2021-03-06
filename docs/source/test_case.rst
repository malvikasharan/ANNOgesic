Performing a test cast
===================

Here we will guide you through a small test case using ANNOgesic. 
You will see who to run the subcommands of ANNOgesic. The test case is a public 
RNA-Seq data from NCBI GEO that was part of a work by
`Bischler et al. <http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE67564>`_.
The differential RNA-seq data is of Helicobacter pylori 26695. 
There will be several output files which are generated in different formats - 
The CSV (tabular separated plain text files) files (opened by LibreOffice or Excel), GFF3 files, TXT files and figures. 
For viewing GFF3 file, you can use a genome browser, for example `IGB <http://bioviz.org/igb/index.html>`_, 
`IGV <https://www.broadinstitute.org/igv/>`_ or `Jbrowse <http://jbrowse.org/>`_.

Before we start, please refer to the section of ``The format of filename`` and 
``The format of libraries for import to ANNOgesic`` in 
the section of ``subcommands``. All the details are also in ``subcommands``. 
Moreover, all the requirements are listed in the section of ``prerequired``.
For the command lines which we will present in the following, please refer to the ``run.sh``
in our `Github <https://github.com/Sung-Huan/ANNOgesic/tree/master/tutorial_data>`_.

Generating a project
--------------------

First of all, we need to create a working folder, we use ``create`` subcommand.

::

    annogesic create ANNOgesic

Then you will see 

::

    Created folder "ANNOgesic" and required subfolders.
    $ ls 
    ANNOgesic

Retrieving the input data
-------------------

For our test case, we can download from `NCBI <ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/bacteria/Helicobacter_pylori/reference/GCF_000008525.1_ASM852v1>`_.
We can set the ``$FTP_SOURCE`` first

::

    FTP_SOURCE=ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/bacteria/Helicobacter_pylori/reference/GCF_000008525.1_ASM852v1/

Then download fasta files(``-f``), gff files(``-g``), gbk files(``-k``), ptt files(``-p``), 
rnt files(``-r``), and converts to embl(``-e``).

::

    $ annogesic get_input_files -F $FTP_SOURCE -g -f -e -k -p -r ANNOgesic

Then you will get the following results

::

    $ ls ANNOgesic/input/reference/fasta/
    NC_000915.fa
    $ ls ANNOgesic/input/reference/annotation/
    NC_000915.1.embl  NC_000915.1.gbk  NC_000915.gff

If the fasta files and annotation files which are retrieved from NCBI is exactly the strain what you want,
you can add ``-t`` for putting the files to ``ANNOgesic/output/target``. Then you can skip running ``get_target_fasta`` 
and ``annotation_transfer``.

In fact, these fasta and gff files are exactly what we want to use for the test case.
But, in order to testing ``get_target_fasta`` and ``annotation_transfer``, we used them as reference first.
After that, we will reorganize the data again.

Putting wig, bam files and reads to proper location
------------------
For the test case, you can download files from 
`here <http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE67564>`_.

::

    $ wget ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByStudy/sra/SRP%2FSRP056%2FSRP056856/SRR1951997/SRR1951997.sra
    $ wget ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByStudy/sra/SRP%2FSRP056%2FSRP056856/SRR1951998/SRR1951998.sra

Then you need to convert the SRA files to Fasta or Fastq format for mapping. You can 
use `SRA toolkit <http://www.ncbi.nlm.nih.gov/books/NBK158900/>`_ for that.

::
  
   $ wget http://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.5.2/sratoolkit.2.5.2-ubuntu64.tar.gz
   $ tar -zxvf sratoolkit.2.5.2-ubuntu64.tar.gz
   $ rm sratoolkit.2.5.2-ubuntu64.tar.gz
   $ ./sratoolkit.2.5.2-ubuntu64/bin/fastq-dump.2.5.2 --fasta SRR1951997.sra
   $ ./sratoolkit.2.5.2-ubuntu64/bin/fastq-dump.2.5.2 --fasta SRR1951998.sra
   $ mv *.fasta ANNOgesic/input/reads
   $ rm SRR1951997.sra
   $ rm SRR1951998.sra

Now you get the reads. Then we have to download the wiggle files.

::

    wget -cP ANNOgesic/input/wigs/tex_notex ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSM1649nnn/GSM1649587/suppl/GSM1649587%5FHp26695%5FML%5FB1%5FHS1%5F%2DTEX%5Fforward%2Ewig%2Egz
    wget -cP ANNOgesic/input/wigs/tex_notex ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSM1649nnn/GSM1649587/suppl/GSM1649587%5FHp26695%5FML%5FB1%5FHS1%5F%2DTEX%5Freverse%2Ewig%2Egz
    wget -cP ANNOgesic/input/wigs/tex_notex ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSM1649nnn/GSM1649588/suppl/GSM1649588%5FHp26695%5FML%5FB1%5FHS1%5F%2BTEX%5Fforward%2Ewig%2Egz
    wget -cP ANNOgesic/input/wigs/tex_notex ftp://ftp.ncbi.nlm.nih.gov/geo/samples/GSM1649nnn/GSM1649588/suppl/GSM1649588%5FHp26695%5FML%5FB1%5FHS1%5F%2BTEX%5Freverse%2Ewig%2Egz
    cd ANNOgesic/input/wigs/tex_notex
    gunzip GSM1649587_Hp26695_ML_B1_HS1_-TEX_forward.wig.gz \
           GSM1649587_Hp26695_ML_B1_HS1_-TEX_reverse.wig.gz \
           GSM1649588_Hp26695_ML_B1_HS1_+TEX_forward.wig.gz \
           GSM1649588_Hp26695_ML_B1_HS1_+TEX_reverse.wig.gz
    cd ../../../../

Because it is a test case, we only download one replicate to reduce the running time.

Improving the reference genome
------------------

If the data which we retrieved from NCBI is exactly the strain what you want, you can skip this step. 
Please remember to put or download the fasta file to ``ANNOgesic/output/target/fasta``.

If the retrieved strain is only the closed strain of your target strain, you may need to run 
subcommand ``get_target_fasta``. However, this command need the mutation table. please refer 
to the section of ``subcommands``. 
Once you have the mutation table, you can improve the fasta files.

We use a simple example to modify our test case. The mutation table is 

===========  ============  ============  ========  =========  ====================  =============  ====  ============
 #target_id  reference_id  reference_nt  position  target_nt  impact of correction  locus tag      gene  Description
-----------  ------------  ------------  --------  ---------  --------------------  -------------  ----  ------------
 NC_test.1   NC_000915.1   a             3         c                                SAOUHSC_00002  dnaA  XXXXXX
 NC_test.1   NC_000915.1   t             6         \-          deletion                                  YYYYYY
 test_case2  NC_000915.1   \-            600       g           insertion            SAOUHSC_00132
===========  ============  ============  ========  =========  ====================  =============  ====  ============

Every column is separated by tab. You can see the new strain will be NC_test.1 and test_case2. Therefore, there will be 
two fasta files in ``ANNOgesic/output/target/fasta``.

Now, let's try it

::

     $ annogesic get_target_fasta \
        -r ANNOgesic/input/reference/fasta \
        -o test_case1:NC_test.1,test_case2:test_case2 \
        -m ANNOgesic/input/mutation_table/mutation.csv \
        ANNOgesic

``-r`` is the folder of original fasta files. In ``-o`` you can assign the filenames of output fasta files and 
the strains that you want to put in it. In our case, we call the first fasta file test_case1 and the 
second one test_case2. test_case1 stores the fasta of NC_test.1 and test_case2 stores test_case2. 
Now we can check the results.

::

    $ head ANNOgesic/input/reference/fasta/NC_000915.fa
    >NC_000915.1
    TGATTAGTGATTAGTGATTAGTGATTAGTGATTAGTGATTAGTGATTAGTGATTAGTGATTAGTGATTAG
    TGATTAGTGATTAGTGATTAGTGATTAGTGATTAGTGATTAGTGATTAGTGATTAGTGATTAGTGATTAG
    TGATTAGTGATTAGTGATTAGTGATTAGTGATTAGTGATTATAGCATCATTTTTTAAATTTAGGTATAAA
    ACACCCTCAATTCAAGGGTTTTTGAGTGAGCTTTTTGCTCAAAGAATCCAAGATAGCGTTTAAAAATTTA
    GGGGTGTTAGGCTCAGCGTAGAGTTTGCCAAGCTCTATGCATTCATTGATGATGATAGGGTTTTGCGTGG
    GCGTGAAGCCAATTTCATACGCTCCTAAGCGTAAAATCGCCTTTTCCATGCTCCCTAATCGCTTGAAATC
    CCAGTCTTTTAAATGCGGCTCGATGAGGGCGTCAATTTCATTGATTTTTTCTAACACGCCATTAAAAAGG
    CTTAAAGCGAAAGCGAGTTGGTTGTTTTTAATCTTTTTTTCTTCTAACATGCTAGAAGCGATTTTTTTAA
    TTTCTTCATTACCGCTCTCAAACGCATACAACAATTCAACCACAGCCCCCCTGGCTTGAGTTCGTGTCGC
    $ head ANNOgesic/output/target/fasta/test_case1.fa
    >NC_test.1
    TGcTTGTGATTAGTGATTAGTGATTAGTGATTAGTGATTAGTGATTAGTGATTAGTGATT
    AGTGATTAGTGATTAGTGATTAGTGATTAGTGATTAGTGATTAGTGATTAGTGATTAGTG
    ATTAGTGATTAGTGATTAGTGATTAGTGATTAGTGATTAGTGATTAGTGATTAGTGATTA
    TAGCATCATTTTTTAAATTTAGGTATAAAACACCCTCAATTCAAGGGTTTTTGAGTGAGC
    TTTTTGCTCAAAGAATCCAAGATAGCGTTTAAAAATTTAGGGGTGTTAGGCTCAGCGTAG
    AGTTTGCCAAGCTCTATGCATTCATTGATGATGATAGGGTTTTGCGTGGGCGTGAAGCCA
    ATTTCATACGCTCCTAAGCGTAAAATCGCCTTTTCCATGCTCCCTAATCGCTTGAAATCC
    CAGTCTTTTAAATGCGGCTCGATGAGGGCGTCAATTTCATTGATTTTTTCTAACACGCCA
    TTAAAAAGGCTTAAAGCGAAAGCGAGTTGGTTGTTTTTAATCTTTTTTTCTTCTAACATG

In ``test_case1.fa``, the third nucleotide replace from A to c. Moreover, The sixth nucleotide is deleted.
In ``test_case2.fa``, it is also modified by mutation table.

If you have no mutation table, you can also use the subcommand ``snp`` to detect the mutations and apply to 
reference genomoes automatically. For this subcommand, we will go through it later.

Generating annotation files
-------------------

We have the fasta files now. We can use it to generate our annotation files. If the annotaion files which 
you retrieved by ``get_input_files`` is exactly the strain what you want, you can skip this step. Please 
remember to copy or download the annotation files to ``ANNOgesic/output/target/annotation``.

Before you running it, you have to notice the environment paths of `RATT <http://ratt.sourceforge.net/>`_. 
If you are using docker container, the path is alread setup. If you setup by yourself, please refer to 
`RATT <http://ratt.sourceforge.net/>`_ to set your environment paths properly.

Now, we can try it.

::

    anngesic annotation_transfer \
        -re ANNOgesic/input/reference/annotation \
        -rf ANNOgesic/input/reference/fasta \
        -tf ANNOgesic/output/target/fasta \
        -e chromosome \
        -t Strain \
        -p NC_000915.1:NC_test.1,NC_000915.1:test_case2 \
        -g \
        ANNOgesic

``-e`` is the prefix of output embl files. ``-t`` is a program of `RATT <http://ratt.sourceforge.net/>`_.
We use ``Strain`` because the similarity is higher than 90%. For other programs, you can refer to 
`RATT <http://ratt.sourceforge.net/>`_. We assign the pairs of transfer at ``-p``. 
The names for ``-p`` are the names of strain not filenames of fasta files. ``-g`` means we want to transfer the embl files 
to GFF3 files and store in ``ANNOgesic/output/target/annotation``.

When the computation is done, you can see

::

    $ ls ANNOgesic/output/target/annotation/
    test_case1.gff  test_case1.ptt  test_case1.rnt  test_case2.gff  test_case2.ptt  test_case2.rnt
    $ ls ANNOgesic/output/annotation_transfer/
    chromosome.NC_test.1.final.embl  chromosome.test_case2.final.embl  NC_test.1.gff  ratt_log.txt  test_case2.gff

In ``ANNOgesic/output/target/annotation``, you can find ptt, rnt and gff files. In ``ANNOgesic/output/annotation_transfer``,
you can find the results of `RATT <http://ratt.sourceforge.net/>`_. ``chromosome.NC_test.1.final.embl`` and 
``chromosome.test_case2.final.embl`` are generated by `RATT <http://ratt.sourceforge.net/>`_. Gff files are 
transferred from these embl files.

TSS and processing site prediction and optimization
-----------------

Now we already knew how to update the genome fasta and annotation files. In order to 
go through the following subcommands, we need to reorganize our data.
First, we remove the fake files that we generated from previous subcommands.

::
    $ rm ANNOgesic/output/target/annotation/*
      rm ANNOgesic/output/target/fasta/*

Then put the correct files that we used as reference before into ``ANNOgesic/output/target``.

::
    $ mv ANNOgesic/input/reference/annotation/* ANNOgesic/output/target/annotation/
      mv ANNOgesic/input/reference/fasta/* ANNOgesic/output/target/fasta/

Before running the subcommands, we need to setup our libraries as a correct format.

::

    tex_notex_libs="GSM1649587_Hp26695_ML_B1_HS1_-TEX_forward.wig:notex:1:a:+,\
    GSM1649587_Hp26695_ML_B1_HS1_-TEX_reverse.wig:notex:1:a:-,\
    GSM1649588_Hp26695_ML_B1_HS1_+TEX_forward.wig:tex:1:a:+,\
    GSM1649588_Hp26695_ML_B1_HS1_+TEX_reverse.wig:tex:1:a:-"

Before running ``tsspredator``, if you want to use the optimized parameters, 
you need to run ``optimize_TSSpredator`` first. It needs to manual check some TSSs. 
In our experience, we recommand you detect more than 50 TSSs and longer than 100kb of genome. 

For test case, we prepared the manual TSS file in our `Github <https://github.com/Sung-Huan/ANNOgesic/tree/master/tutorial_data>`_, 
you can download it. 

::

    wget -cP ANNOgesic/input/manual_TSS/ https://raw.githubusercontent.com/Sung-Huan/ANNOgesic/master/tutorial_data/NC_000915_manual_TSS.gff

Now, we have a manual TSS files which store in ``ANNOgesic/input/manual_TSS``. 
we can try optimization of TSSs right now (because the manual TSS file only provide the first 200kb, 
we set the ``--le`` as 200000).

::

    annogesic optimize_tsspredator \
        -w ANNOgesic/input/wigs/tex_notex \
        -fs ANNOgesic/output/target/fasta \
        -g ANNOgesic/output/target/annotation \
        -n NC_000915.1 \
        -l $tex_notex_libs \
        -p TSS -s 25 \
        -m ANNOgesic/input/manual_TSS/NC_000915_manual_TSS.gff \
        -le 200000 \
        ANNOgesic

``optimize_TSSpredator`` will compare gff files of manual checked TSSs and predicted TSSs to find the best parameters. 
You can check the results and parameters of each step in screen. we set the steps only 25 for testing. 
When the program finished, you can find several files.

::

    $ ls ANNOgesic/output/TSS/optimized_TSSpredator/
    best.csv  log.txt  stat.csv

``best.csv`` is for the best parameters; ``stat.csv`` is for the parameters of each step.

Let's assume the best parameters are that height is 0.3, height_reduction is 0.2, factor is 2.0, factor_reduction is 0.5, 
base_height is 0.0, enrichment_factor is 1.7, processing_factor is 1.5. Now we can set the parameter set for running  
``tss``.

::

    annogesic tsspredator \
        -w ANNOgesic/input/wigs/tex_notex \
        -f ANNOgesic/output/target/fasta \
        -g ANNOgesic/output/target/annotation \
        -l $tex_notex_libs \
        -p test \
        -he 0.3 \
        -rh 0.2 \
        -fa 2.0 \
        -rf 0.5 \
        -bh 0.0 \
        -ef 1.7 \
        -pf 1.5 \
        -s \
        -v \
        -le 200000 \
        -m ANNOgesic/input/manual_TSS/NC_000915_manual_TSS.gff \
        ANNOgesic

If you import the manual checked TSSs to ``-m``, the subcommand will merge the manual checked TSSs and predicted TSSs. 
If you didn't import it, the subcommand will only produce predicted TSSs. You will get gff file, MasterTable and statistic file.

::

    $ ls ANNOgesic/output/TSS/
    configs  gffs  MasterTables  statistics
    $ ls ANNOgesic/output/TSS/configs/
    config_NC_000915.1.ini
    $ ls ANNOgesic/output/TSS/gffs/
    NC_000915.1_TSS.gff
    $ ls ANNOgesic/output/TSS/MasterTables/MasterTable_NC_000915.1/
    AlignmentStatistics.tsv  err.txt  log.txt  MasterTable.tsv  superConsensus.fa  superTSS.gff  superTSStracks.gff  test_super.fa  test_super.gff  test_TSS.gff  TSSstatistics.tsv
    $ ls ANNOgesic/output/TSS/statistics/NC_000915.1/
    stat_compare_TSSpredator_manual_NC_000915.1.csv  stat_gene_vali_NC_000915.1.csv  stat_TSS_class_NC_000915.1.csv  stat_TSS_libs_NC_000915.1.csv  TSS_class_NC_000915.1.png  TSS_venn_NC_000915.1.png
    

If you want to predict processing sites, the procedures are the same. You just need to change the program from TSS to 
processing_site (``-t``) and the parameter sets (we assume the best parameter sets are that 
height is 0.3, height_reduction is 0.2, factor is 2.0, factor_reduction is 0.5,
base_height is 0.0, enrichment_factor is 1.9, processing_factor is 5.7).

::

    annogesic tsspredator \
        -w ANNOgesic/input/wigs/tex_notex \
        -f ANNOgesic/output/target/fasta \
        -g ANNOgesic/output/target/annotation \
        -l $tex_notex_libs \
        -p test \
        -he 0.3 \
        -rh 0.2 \
        -fa 2.0 \
        -rf 0.5 \
        -bh 0.0 \
        -ef 1.9 \
        -pf 5.7 \
        -s \
        -v \
        -t processing_site \
        ANNOgesic

Performing transcript assembly
----------------

For detecting transcript boundary, transcript assembly is the basic feature. 
we can use the subcommand ``transcript_assembly`` to do it. Normally, we strongly 
recommand that user should provide fragmentation RNA-Seq. Because RNA-Seq always lose some information 
of 3'end. However, there is no fragmented libraries in the test case. 
Therefore, we only use TEX +/- to do it.

The command would be like the following.

::

    annogesic transcript_assembly \
        -g ANNOgesic/output/target/annotation \
        -tw ANNOgesic/input/wigs/tex_notex \
        -tl $tex_notex_libs \
        -rt 1 \
        -ct ANNOgesic/output/TSS/gffs \
        -cg ANNOgesic/output/target/annotation \
        ANNOgesic

It will generate gff files and tables. Because we also compared with TSSs and annotation files, it will generate statistics files.

::

    $ ls ANNOgesic/output/transcriptome_assembly/gffs
    NC_000915.1_transcript.gff
    $ ls ANNOgesic/output/transcriptome_assembly/tables
    NC_000915.1_transcript.csv
    $ ls ANNOgesic/output/transcriptome_assembly/statistics
    stat_compare_Transcriptome_assembly_CDS_NC_000915.1.csv  stat_compare_Transcriptome_assembly_TSS_NC_000915.1.csv

Prediction of terminator
----------------------

For predicting terminators, we can use subcommand ``terminator``. The command is like the following.

::

    annogesic terminator \
        -f ANNOgesic/output/target/fasta \
        -g ANNOgesic/output/target/annotation \
        -s \
        -tw ANNOgesic/input/wigs/tex_notex \
        -a ANNOgesic/output/transcriptome_assembly/gffs \
        -tl $tex_notex_libs \
        -rt 1 -tb \
        ANNOgesic

It will generate four different kinds of gff files and tables.

::

    $ ls ANNOgesic/output/terminator/gffs/
    all_candidates  best  express non_express
    $ ls ANNOgesic/output/terminator/tables
    all_candidates  best  express non_express

``all_candidates`` is for all candidates; ``express`` is for the candidates which have expression; 
``best`` is for the candidates which coverage significant decreasing. ``non_express`` is for 
the candidates which have no expression. There are a gff file or table for each folder.

::

    $ ls ANNOgesic/output/terminator/gffs/best
    NC_000915.1_term.gff
    $ ls ANNOgesic/output/terminator/gffs/express
    NC_000915.1_term.gff
    $ ls ANNOgesic/output/terminator/gffs/all_candidates
    NC_000915.1_term.gff
    $ ls ANNOgesic/output/terminator/gffs/non_express
    NC_000915.1_term.gff
    $ ls ANNOgesic/output/terminator/tables/best
    NC_000915.1_term.csv
    $ ls ANNOgesic/output/terminator/tables/express
    NC_000915.1_term.csv
    $ ls ANNOgesic/output/terminator/tables/all_candidates
    NC_000915.1_term.csv
    $ ls ANNOgesic/output/terminator/tables/non_express
    NC_000915.1_term.csv

In transtermhp folder, there are the output files from `TranstermHP <http://transterm.cbcb.umd.edu/>`_.

::

    $ ls ANNOgesic/output/terminator/transtermhp/NC_000915.1
    NC_000915.1_best_terminator_after_gene.bag  NC_000915.1_terminators.txt  NC_000915.1_terminators_within_robust_tail-to-tail_regions.t2t

Moreover, the statistics files are stored in ``statistics``.

::

    $ ls ANNOgesic/output/terminator/statistics/
    stat_NC_000915.1.csv
    stat_comparison_terminator_transcript_all_candidates.csv
    stat_comparison_terminator_transcript_best.csv
    stat_comparison_terminator_transcript_express.csv

Generating UTR
--------------

Now, we have the information of TSSs, transcripts and terminators. We can detect the 5'UTRs and 3'UTRs easily by using 
the subcommand ``utr``.

::

    annogesic utr \
        -g ANNOgesic/output/target/annotation \
        -t ANNOgesic/output/TSS/gffs \
        -a ANNOgesic/output/transcriptome_assembly/gffs \
        -e ANNOgesic/output/terminator/gffs/best \
        ANNOgesic

If your TSSs is not generated by ANNOgesic, please assign ``-s``, it will classify the TSSs for generating UTRs.
The gff files and statistics files will be stored in ``5UTR`` and ``3UTR``.

::

    $ ls ANNOgesic/output/UTR/3UTR
    gffs/       statistics/
    $ ls ANNOgesic/output/UTR/5UTR
    gffs/       statistics/
    $ ls ANNOgesic/output/UTR/3UTR/gffs
    NC_000915.1_3UTR.gff
    $ ls ANNOgesic/output/UTR/5UTR/gffs
    NC_000915.1_5UTR.gff
    $ ls ANNOgesic/output/UTR/5UTR/statistics
    NC_000915.1_all_5utr_length.png
    $ ls ANNOgesic/output/UTR/3UTR/statistics
    NC_000915.1_all_3utr_length.png

Now, you have all information for defining the transcript boundary.

Integrating to operon and suboperon
-----------------

We already had TSSs, transcripts, terminators, CDSs, UTRs. We can integrate all these information to 
detect operons and suboperons. You can use the subcommand ``operon`` to get it.

::

    annogesic operon \
        -g ANNOgesic/output/target/annotation \
        -t ANNOgesic/output/TSS/gffs \
        -a ANNOgesic/output/transcriptome_assembly/gffs \
        -u5 ANNOgesic/output/UTR/5UTR/gffs \
        -u3 ANNOgesic/output/UTR/3UTR/gffs \
        -e ANNOgesic/output/terminator/gffs/best \
        -s -c \
        ANNOgesic

``operon`` will generate three folders to store gff files, tables and statistics files.

::

    $ ls ANNOgesic/output/operons/
    gffs  statistics  tables
    $ ls ANNOgesic/output/operons/gffs/
    NC_000915.1_all_features.gff
    $ ls ANNOgesic/output/operons/tables/
    operon_NC_000915.1.csv
    $ ls ANNOgesic/output/operons/statistics/
    stat_operon_NC_000915.1.csv

Promoter motif detection
----------------

As long as you have TSSs, you can use the subcommand ``promoter`` to get promoters. It will generate the promoters
based on the classes of TSS. Therefore, if your TSSs are not computed by ``ANNOgesic``,
you need to add ``-s`` and ``-g`` (for annotation files). Then ``promoter`` will help you
to classify your TSSs.

::

    annogesic promoter \
        -t ANNOgesic/output/TSS/gffs \
        -f ANNOgesic/output/target/fasta \
        -w 45,2-10 \
        ANNOgesic

You can define the length of motifs. In our test case, we use ``50`` and ``2-10``. ``2-10`` means the
width is from 2 to 10.

Based on the classes of TSSs, it will generate different output files.

::

    $ ls ANNOgesic/output/promoter_analysis/NC_000915.1
    promoter_motifs_NC_000915.1_allstrain_all_types_2-10_nt  promoter_motifs_NC_000915.1_allstrain_internal_45_nt   promoter_motifs_NC_000915.1_allstrain_secondary_2-10_nt
    promoter_motifs_NC_000915.1_allstrain_all_types_45_nt    promoter_motifs_NC_000915.1_allstrain_orphan_2-10_nt   promoter_motifs_NC_000915.1_allstrain_secondary_45_nt
    promoter_motifs_NC_000915.1_allstrain_antisense_2-10_nt  promoter_motifs_NC_000915.1_allstrain_orphan_45_nt     promoter_motifs_NC_000915.1_allstrain_without_orphan_2-10_nt
    promoter_motifs_NC_000915.1_allstrain_antisense_45_nt    promoter_motifs_NC_000915.1_allstrain_primary_2-10_nt  promoter_motifs_NC_000915.1_allstrain_without_orphan_45_nt
    promoter_motifs_NC_000915.1_allstrain_internal_2-10_nt   promoter_motifs_NC_000915.1_allstrain_primary_45_nt
    $ ls ANNOgesic/output/promoter_analysis/NC_000915.1/promoter_motifs_NC_000915.1_allstrain_all_types_45_nt/
    logo10.eps  logo1.png  logo3.eps  logo4.png  logo6.eps  logo7.png  logo9.eps      logo_rc10.png  logo_rc2.eps  logo_rc3.png  logo_rc5.eps  logo_rc6.png  logo_rc8.eps  logo_rc9.png  meme.xml
    logo10.png  logo2.eps  logo3.png  logo5.eps  logo6.png  logo8.eps  logo9.png      logo_rc1.eps   logo_rc2.png  logo_rc4.eps  logo_rc5.png  logo_rc7.eps  logo_rc8.png  meme.html     meme.csv
    logo1.eps   logo2.png  logo4.eps  logo5.png  logo7.eps  logo8.png  logo_rc10.eps  logo_rc1.png   logo_rc3.eps  logo_rc4.png  logo_rc6.eps  logo_rc7.png  logo_rc9.eps  meme.txt

Prediction of sRNA and sORF
-----------------

Based on comparison of trascripts and CDSs information, we can detect intergenic sRNAs. Moreover, we 
have the information of TSSs and processing sites. We can detect UTR-derived sRNAs as well. You can 
get sRNAs by running subcommand ``srna``. Normally, we would recommand that you also have fragmented libraries to 
compute ``srna``. However, we can't get it in our test case right now. Therefore, we only use TEX +/- for this test case.

For running ``srna``, you can import some information to detect sRNA. There are ``tss``, ``sec_str``,
``blast_nr``, ``blast_srna``, ``promoter``, ``term``, ``sorf``. Moreover, You can also assign that the best 
candidates should contain which information. In this test case, we can try to use ``tss``, ``sec_str``,
``blast_nr``, ``blast_srna``, ``promoter``, ``term``. If you don't want to import ``blast_nr`` which take much time 
for running, you can also remove it.

Before running ``srna``, we have to get sRNA database(we use `BSRD <http://www.bac-srna.org/BSRD/index.jsp>`_) and 
`nr database <ftp://ftp.ncbi.nih.gov/blast/db/FASTA/>`_ (if you have not downloaded before). 
You can download the fasta file of `BSRD <http://www.bac-srna.org/BSRD/index.jsp>`_ from our 
`Github <https://github.com/Sung-Huan/ANNOgesic/tree/master/database>`_.

::

    wget -cP ANNOgesic/input/database/ https://raw.githubusercontent.com/Sung-Huan/ANNOgesic/master/database/sRNA_database_BSRD.fa

Then we need to download `nr database <ftp://ftp.ncbi.nih.gov/blast/db/FASTA/>`_. If you already had it, 
you can skip this step.

::

    wget -cP ANNOgesic/input/database/ ftp://ftp.ncbi.nih.gov/blast/db/FASTA/nr.gz
    gunzip ANNOgesic/input/database/nr.gz

Because the ``ANNOgesic`` will give the name of nr database - nr, we suggest the rename the nr to nr.fa.

::
    mv ANNOgesic/input/database/nr ANNOgesic/input/database/nr.fa

If you already had these databases in other folders, please change ``-sd`` and ``-od``.
If your databses are formated before, you can remove ``-sf`` and ``-nf``.
Furthermore, you can assign the best candidates should include which information. You can assign 
``--best_with_terminator``, ``--best_with_promoter``, ``--best_with_all_sRNAhit``, ``--best_without_sORF_candidate``.
Please check the details in the section of ``subcommands``.
Now we can run ``srna`` with default parameters.

::

    annogesic srna \
        -d tss,blast_srna,promoter,term,blast_nr,sec_str \
        -g ANNOgesic/output/target/annotation \
        -t ANNOgesic/output/TSS/gffs \
        -p ANNOgesic/output/processing_site/gffs \
        -a ANNOgesic/output/transcriptome_assembly/gffs \
        -tw ANNOgesic/input/wigs/tex_notex \
        -f ANNOgesic/output/target/fasta \
        -tf ANNOgesic/output/terminator/gffs/best \
        -pt ANNOgesic/output/promoter_analysis/NC_000915.1/promoter_motifs_NC_000915.1_allstrain_all_types_45_nt/meme.csv \
        -pn MOTIF_1 \
        -m \
        -u \
        -nf \
        -sf \
        -sd ANNOgesic/input/database/sRNA_database_BSRD \
        -nd ANNOgesic/input/database/nr \
        -tl $tex_notex_libs \
        -rt 1 \
        -ba \
        ANNOgesic


For getting the best candidates of sRNAs, we can assign some information for filtering.
If you already have the information of sORFs and want to import them, you can also assign 
``-d tss,blast_srna,promoter,term,blast_nr,sec_str,sorf`` and ``-O`` for the path of sORF. 
It will compare sORFs and sRNAs.

The output of ``srna`` will be like the following.

::

    $ ls ANNOgesic/output/sRNA/
    blast_result_and_misc  gffs  log.txt  mountain_plot  sec_structure  sRNA_2d_NC_000915.1  sRNA_seq_NC_000915.1  statistics  tables

``blast_result_and_misc`` will store the results of blast; ``mountain_plot`` will store the mountain plots; 
``sec_structure`` will store the plots of secondary structure of sRNA; ``statistics`` will store statistics files.

``sRNA_2d_NC_000915.1`` and ``sRNA_seq_NC_000915.1`` are text files of sequence of sRNAs and secondary structure of sRNAs.

::

    $ ls ANNOgesic/output/sRNA/blast_result_and_misc/
    nr_blast_NC_000915.1.txt  sRNA_blast_NC_000915.1.txt
    $ ls ANNOgesic/output/sRNA/mountain_plot/NC_000915/
    srna0_NC_000915.1_16651_16765_-_mountain.pdf        srna138_NC_000915.1_1496938_1497216_-_mountain.pdf  srna25_NC_000915.1_444979_445114_+_mountain.pdf  srna63_NC_000915.1_761094_761174_+_mountain.pdf
    srna100_NC_000915.1_1164252_1164295_-_mountain.pdf  srna139_NC_000915.1_1502542_1502637_+_mountain.pdf  srna26_NC_000915.1_445012_445139_-_mountain.pdf  srna64_NC_000915.1_773130_773564_+_mountain.pdf
    ...
    ls ANNOgesic/output/sRNA/sec_structure/dot_plot/NC_000915/
    srna0_NC_000915.1_16651_16765_-_dp.pdf        srna138_NC_000915.1_1496938_1497216_-_dp.pdf  srna25_NC_000915.1_444979_445114_+_dp.pdf  srna63_NC_000915.1_761094_761174_+_dp.pdf
    srna100_NC_000915.1_1164252_1164295_-_dp.pdf  srna139_NC_000915.1_1502542_1502637_+_dp.pdf  srna26_NC_000915.1_445012_445139_-_dp.pdf  srna64_NC_000915.1_773130_773564_+_dp.pdf
    ...
    $ ls ANNOgesic/output/sRNA/sec_structure/sec_plot/NC_000915/
    srna0_NC_000915.1_16651_16765_-_rss.pdf        srna138_NC_000915.1_1496938_1497216_-_rss.pdf  srna25_NC_000915.1_444979_445114_+_rss.pdf  srna63_NC_000915.1_761094_761174_+_rss.pdf
    srna100_NC_000915.1_1164252_1164295_-_rss.pdf  srna139_NC_000915.1_1502542_1502637_+_rss.pdf  srna26_NC_000915.1_445012_445139_-_rss.pdf  srna64_NC_000915.1_773130_773564_+_rss.pdf
    ...
    $ ls ANNOgesic/output/sRNA/statistics/
    stat_sRNA_blast_class_NC_000915.1.csv  stat_sRNA_class_NC_000915.1.csv

For ``gffs`` and ``tables``, they are divided by three kinds of results. ``all_candidates`` is for all candidates 
without filtering; ``best`` is for the best candidates of sRNAs after filtering; ``for_class`` is for classes which classified 
by the information that you assigned. For our test case, folding energy < -0.05(class 1), associated with TSSs(class 2),
blast to nr without homologs(class 3), associated with terminators(class 4),
blast to sRNA database(class 5 for without homologs, class 6 for with homologs), associated with promoters(class 7).

::

    $ ls ANNOgesic/output/sRNA/gffs/
    all_candidates  best  for_class
    $ ls ANNOgesic/output/sRNA/tables/
    all_candidates  best  for_class
    $ ls ANNOgesic/output/sRNA/gffs/all_candidates/
    NC_000915.1_sRNA.gff
    $ ls ANNOgesic/output/sRNA/tables/all_candidates/
    NC_000915.1_sRNA.csv
    $ ls ANNOgesic/output/sRNA/gffs/best/
    NC_000915.1_sRNA.gff
    $ ls ANNOgesic/output/sRNA/tables/best/
    NC_000915.1_sRNA.csv
    $ ls ANNOgesic/output/sRNA/gffs/for_class/NC_000915.1/
    class_1_all.gff                                          class_1_class_2_class_7_all.gff                  class_2_all.gff                                  class_3_all.gff
    class_1_class_2_all.gff                                  class_1_class_3_all.gff                          class_2_class_3_all.gff                          class_3_class_4_all.gff
    ...

    $ ls ANNOgesic/output/sRNA/tables/for_class/NC_000915.1/
    class_1_all.csv                                          class_1_class_2_class_7_all.csv                  class_2_all.csv                                  class_3_all.csv
    class_1_class_2_all.csv                                  class_1_class_3_all.csv                          class_2_class_3_all.csv                          class_3_class_4_all.csv
    ...

As we know, the sORFs is also the region which has no annotation but has expression. Therefore, the potential sRNAs
may be sORFs not sRNAs. In order to get information of sORFs, you can use subcommand ``sorf`` to get it.

::

    annogesic sorf \
        -g ANNOgesic/output/target/annotation \
        -t ANNOgesic/output/TSS/gffs \
        -a ANNOgesic/output/transcriptome_assembly/gffs \
        -tw ANNOgesic/input/wigs/tex_notex \
        -f ANNOgesic/output/target/fasta \
        -s ANNOgesic/output/sRNA/gffs/best \
        -tl $tex_notex_libs \
        -rt 1 -u \
        ANNOgesic

For generating best gff files, you can decide which information you want to use for filtering. The options 
are ribosomal binding sites, starting from TSSs and non-overlaping with sRNAs.
Then you can get the gff files, statistics files and tables. ``all_candidates`` 
is the gff files and tables without filtering; ``best`` is the gff_files and tables with filtering.

::

    $ ls ANNOgesic/output/sORF/gffs/all_candidates/
    NC_000915.1_sORF.gff
    $ ls ANNOgesic/output/sORF/gffs/best/
    NC_000915.1_sORF.gff
    $ ls ANNOgesic/output/sORF/tables/all_candidates/
    NC_000915.1_sORF.csv
    $ ls ANNOgesic/output/sORF/tables/best/
    NC_000915.1_sORF.csv
    $ ls ANNOgesic/output/sORF/statistics/
    stat_NC_000915.1_sORF.csv

Performing sRNA target prediction
------------------

Now we have the sRNA candidates. If you want to know the targets of these sRNAs, you can use ``srna_target`` 
to get these information.

::

    annogesic srna_target \
        -g ANNOgesic/output/target/annotation \
        -f ANNOgesic/output/target/fasta \
        -r ANNOgesic/output/sRNA/gffs/best \
        -q NC_000915.1:-:7249:7321 \
        -p both \
        ANNOgesic

For testing, we just do the prediction for one sRNA. You can also assign several of sRNAs like 
``NC_000915.1:-:7249:7321,NC_000915.1:-:16651:16765``. If you want to compute all sRNAs, you 
can assign ``all`` to ``-q``. However, it may take several days.

``srna_target`` will generate several folders.

::

    $ ls ANNOgesic/output/sRNA_targets/
    merge  RNAplex  RNAup  sRNA_seqs  target_seqs

``sRNA_seqs`` and ``target_seqs`` are for the sequences of sRNAs and potential targets.

::

    $ ls ANNOgesic/output/sRNA_targets/sRNA_seqs
    NC_000915.1_sRNA.fa
    $ ls ANNOgesic/output/sRNA_targets/target_seqs
    NC_000915.1_target.fa

``RNAplex`` and ``RNAup`` are for the output of `RNAplex and RNAup <http://www.tbi.univie.ac.at/RNA/>`_.

::

    $ ls ANNOgesic/output/sRNA_targets/RNAplex/NC_000915.1/
    NC_000915.1_RNAplex_rank.csv  NC_000915.1_RNAplex.txt
    $ ls ANNOgesic/output/sRNA_targets/RNAup/NC_000915.1/
    NC_000915.1_RNAup.log  NC_000915.1_RNAup_rank.csv  NC_000915.1_RNAup.txt

``merge`` is for the merged results of `RNAplex <http://www.tbi.univie.ac.at/RNA/RNAplex.1.html>`_ and 
`RNAup <http://www.tbi.univie.ac.at/RNA/RNAup.1.html>`_. ``NC_000915.1_merge.csv``  merge all the results of 
both methods. ``NC_000915.1_overlap.csv`` only stores the candidates which are top 20(default) in both methods.

::

    $ ls ANNOgesic/output/sRNA_targets/merge/NC_000915.1/
    NC_000915.1_merge.csv  NC_000915.1_overlap.csv

Mapping and detecting of circular RNA
-------------------

You may also be interested in circular RNAs. The subcommand ``circrna`` can help you to get the information. 
It apply `Segemehl <http://www.bioinf.uni-leipzig.de/Software/segemehl/>`_ to detect circular RNAs. Because 
we didn't map the reads of test case before, we can also do it by running ``circrna``. If your mapping is 
generated by `Segemehl <http://www.bioinf.uni-leipzig.de/Software/segemehl/>`_ with ``-S``, then you can 
skip ``-a`` and assign the path of bam files to ``-nb`` or ``-fb``. It can reduce the running time. However, 
if you mapped the reads by other tools or you mapped the reads by 
`Segemehl <http://www.bioinf.uni-leipzig.de/Software/segemehl/>`_ without ``-S``, Unfortunately, 
you have to re-mapping again. You can assign parallel (``-p``) to run it as well.

Since it is only a test case, we can reduce the running time by selecting the subset of reads(first 50000).

::

     head -n 50000 ANNOgesic/input/reads/SRR1951998.fasta > ANNOgesic/input/reads/SRR1951998_50000.fasta
     head -n 50000 ANNOgesic/input/reads/SRR1951997.fasta > ANNOgesic/input/reads/SRR1951997_50000.fasta
     rm ANNOgesic/input/reads/SRR1951997.fasta
     rm ANNOgesic/input/reads/SRR1951998.fasta

Now, we can try ``circrna``

::

     annogesic circrna \
         -f ANNOgesic/output/target/fasta \
         -p 10 \
         -g ANNOgesic/output/target/annotation \
         -a \
         ANNOgesic

``circrna`` will generate several folders.

::

    $ ls ANNOgesic/output/circRNA/
    circRNA_tables  gffs  segemehl_align  segemehl_splice statistics

``segemehl_align`` and ``segemehl_splice`` are for the results of 
`Segemehl <http://www.bioinf.uni-leipzig.de/Software/segemehl/>`_. ``segemehl_align`` stores the bam files of 
alignment and ``segemehl_splice`` stores the results of splice detection.

::

    $ ls ANNOgesic/output/circRNA/segemehl_align/NC_000915.1/
    SRR1951997_50000_NC_000915.1.bam  SRR1951998_50000_NC_000915.1.bam
    $ ls ANNOgesic/output/circRNA/segemehl_splice/NC_000915.1/
    splicesites_all.bed  transrealigned_all.bed    

The gff files, tables and statistics files are stored in ``gffs``, ``circRNA_tables`` and ``statistics``.

::

    $ ls ANNOgesic/output/circRNA/gffs/NC_000915.1/
    NC_000915.1_circRNA_all.gff  NC_000915.1_circRNA_best.gff
    $ ls ANNOgesic/output/circRNA/circRNA_tables/NC_000915.1/
    circRNA_NC_000915.1_all.csv  circRNA_NC_000915.1_best.csv
    $ ls ANNOgesic/output/circRNA/statistics/
    stat_circRNA_NC_000915.1.csv

``NC_000915.1_circRNA_all.gff`` and ``circRNA_NC_000915.1_all.csv`` are for all circular RNAs without filtering. 
``NC_000915.1_circRNA_best.gff`` and ``circRNA_NC_000915.1_best.csv`` 
are the circular RNAs after filering by mapping ratio and comparison of genome annotation.

SNP calling
--------------

If you want to know the SNPs or mutations of your RNA-seq data, you can use ``snp`` to get it.
``snp`` is divided by two parts. One part is for comparing with the "reference strain" which is the
closed strain of your strain("target strain"). It is useful for users who have no fasta files of their 
strain. You can refer to the section of ``Retrieving the input data``.
Because you may not have time to check the mutations between "reference strain" and "target strain",
it is a good way to detect the mutations automatically. You just need to put your bam files of 
"reference strain" in correct path. It will generate the potential sequences.
The other part is for detecting the mutations of the alignment files and "target strain". In this part, 
you can know the real mutations of "target strain". Therefore, you need to put the bam files of 
"target strain" to the correct folder.

Before running the subcommand, we must have the bam files. Because we already generated them through 
running ``circrna``, we can just use them. However, please remember that the mapping function of 
``circrna`` is only basic one. If you have other request, please do mapping by yourself.

For testing, we only discover the mutations of "target strain" because our mapping is based on the 
fasta of "target strain" - NC_000915. Therefore, we copy the bam files to ``BAMs_map_target``.

::

    cp ANNOgesic/output/circRNA/segemehl_align/NC_000915.1/SRR195199* ANNOgesic/input/BAMs/BAMs_map_target/tex_notex

Then we can run the subcommand.

::

    annogesic snp \
        -t target \
        -p 1,2,3 \
        -tw ANNOgesic/input/BAMs/BAMs_map_target/tex_notex \
        -f ANNOgesic/output/target/fasta \
        ANNOgesic

If you want to compute for comparison of "reference strain" and "target strain", you just need to change 
``-t`` to ``reference`` and assign the correct bam files.

``snp`` will generate two folders, ``compare_reference`` is for the results of comparison of "reference strain" 
and "target strain". ``validate_target`` is for the results of real mutations of "target strain".

::

    $ ls ANNOgesic/output/SNP_calling/                                                                                                      
    compare_reference  validate_target

Becaues we run ``validate_target``, you can see there are several folders under ``validate_target``.

::

    $ ls ANNOgesic/output/SNP_calling/validate_target/
    SNP_raw_outputs  SNP_table  seqs  statistics

All folders are divided by three parts - ``extend_BAQ``, ``with_BAQ`` and ``without_BAQ``.

::

    $ ls ANNOgesic/output/SNP_calling/validate_target/seqs/
    extend_BAQ/  with_BAQ/    without_BAQ/

In ``seqs``, there are the potential sequences.

::

    $ ls ANNOgesic/output/SNP_calling/validate_target/seqs/with_BAQ/NC_000915.1/
      NC_000915.1_NC_000915.1_1_1.fa

``SNP_raw_outputs`` stores the output of `Samtools and Bcftools<https://github.com/samtools>`_. 
``SNP_table`` stores the results after filtering and the indices of potential sequence(
you can see the difference between these potential sequences in ``seqs``).
``statistics`` stores the statistics and visualization files.

::

    $ ls ANNOgesic/output/SNP_calling/validate_target/SNP_raw_outputs/NC_000915.1/
    NC_000915.1_extend_BAQ.vcf  NC_000915.1_with_BAQ.vcf  NC_000915.1_without_BAQ.vcf
    $ ls ANNOgesic/output/SNP_calling/validate_target/SNP_table/NC_000915.1/
    NC_000915.1_extend_BAQ_depth_only.vcf     NC_000915.1_with_BAQ_depth_only.vcf     NC_000915.1_without_BAQ_depth_only.vcf
    NC_000915.1_extend_BAQ_depth_quality.vcf  NC_000915.1_with_BAQ_depth_quality.vcf  NC_000915.1_without_BAQ_depth_quality.vcf
    NC_000915.1_extend_BAQ_seq_reference.csv  NC_000915.1_with_BAQ_seq_reference.csv  NC_000915.1_without_BAQ_seq_reference.csv
    $ ls ANNOgesic/output/SNP_calling/validate_target/statistics/
    NC_000915.1_extend_BAQ_NC_000915.1_SNP_QUAL.png  NC_000915.1_without_BAQ_NC_000915.1_SNP_QUAL.png  stat_NC_000915.1_with_BAQ_SNP.csv
    NC_000915.1_with_BAQ_NC_000915.1_SNP_QUAL.png    stat_NC_000915.1_extend_BAQ_SNP.csv               stat_NC_000915.1_without_BAQ_SNP.csv

Mapping Gene ontology
------------------

Gene ontology is useful for understanding the function of gene products. ``go_term`` is the 
subcommand for mapping your annotations to gene ontology. Before running ``go_term``, we 
need to prepare some databases. First, please download 
`goslim.obo <http://geneontology.org/page/go-slim-and-subset-guide>`_ and 
`go.obo <http://geneontology.org/page/download-ontology>`_ and 
`idmapping_selected.tab <http://www.uniprot.org/downloads>`_.

::

    $ wget -cP ANNOgesic/input/database http://www.geneontology.org/ontology/subsets/goslim_generic.obo
    $ wget -cP ANNOgesic/input/database http://geneontology.org/ontology/go.obo
    $ wget -cP ANNOgesic/input/database ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/idmapping/idmapping_selected.tab.gz
    $ gunzip ANNOgesic/input/database/idmapping_selected.tab.gz

Now, we have all required databases. You can also import the information of transcript to 
generate the results which only included the expressed CDS.

Let's try it.

::

    annogesic go_term \
        -g ANNOgesic/output/target/annotation \
        -a ANNOgesic/output/transcriptome_assembly/gffs \
        ANNOgesic

The output of ``go_term`` will store in ``Go_term_results``. The statistics files and 
figures will store in ``statistics``.

::
    $ ls ANNOgesic/output/Go_term/
    all_CDS  expressed_CDS
    $ ls ANNOgesic/output/Go_term/all_CDS/
    Go_term_results  statistics
    $ ls ANNOgesic/output/Go_term/all_CDS/Go_term_results/NC_000915.1/
    all_strains_uniprot.csv
    $ ls ANNOgesic/output/Go_term/all_CDS/statistics/NC_000915.1/
    figs  stat_NC_000915.1.csv
    $ ls ANNOgesic/output/Go_term/all_CDS/statistics/NC_000915.1/figs/
    NC_000915.1_biological_process.png  NC_000915.1_cellular_component.png  NC_000915.1_molecular_function.png  NC_000915.1_three_roots.png

Prediction of Subcellular localization
------------------

Subcellular localization may be a useful information for analysis of protein function. For 
generating the information of subcellular localization, you can use the subcommand 
``subcellular_localization`` to get it. Like ``go_term``, you can also import the 
information of transcript to generate the results which only included the expressed CDS.

::

    annogesic subcellular_localization \
        -g ANNOgesic/output/target/annotation \
        -f ANNOgesic/output/target/fasta \
        -a ANNOgesic/output/transcriptome_assembly/gffs \
        -m -b negative \
        ANNOgesic

The output of ``subcellular_localization`` will generate two folders. ``psortb_results`` will 
store the output of `Psortb <http://www.psort.org/psortb/>`_. ``statistics`` will store 
the statistics files and figures.

::

    $ ls ANNOgesic/output/subcellular_localization/
    all_CDS  expressed_CDS
    $ ls ANNOgesic/output/subcellular_localization/all_CDS/
    psortb_results  statistics
    $ ls ANNOgesic/output/subcellular_localization/all_CDS/psortb_results/NC_000915.1/
    NC_000915.1_raw.txt  NC_000915.1_table.csv
    $ ls ANNOgesic/output/subcellular_localization/all_CDS/statistics/NC_000915.1/
    NC_000915.1_NC_000915.1.png  stat_NC_000915.1_sublocal.csv

Generating protein-protein interaction network
-------------------

Protein-protein interaction network is an important feature for analysis of regulation. 
The subcommand ``ppi_network`` combines `STRING <http://string-db.org/>`_ 
(database of protein-protein interaction) 
and `PIE <http://www.ncbi.nlm.nih.gov/CBBresearch/Wilbur/IRET/PIE/>`_ 
(text-mining for protein-protein interaction). It can generate the protein-protein 
interaction networks with supported literatures. You can refer to relevance of literatures 
and networks to find your interesting candidates.

Before running the subcommand, you need to download the 
`species.vXXXX.txt from STRING <http://string-db.org/cgi/download.pl>`_

::

    wget -cP ANNOgesic/input/database http://string-db.org/newstring_download/species.v10.txt

Now, we can try the subcommand.

::

    annogesic ppi_network \
        -s NC_000915.1.gff:NC_000915.1:'Helicobacter pylori 26695':'Helicobacter pylori' \
        -g ANNOgesic/output/target/annotation \
        -d ANNOgesic/input/database/species.v10.txt \
        -q NC_000915.1:217:633:-,NC_000915.1:2719:3402:+ \
        -n \
        ANNOgesic

We just tried to compute two proteins. If you want to get all proteins in ptt files, 
you just need to assign ``all`` in ``-q``.

``ppi_network`` will generate three folders.

::

    $ ls ANNOgesic/output/PPI/
    all_results/  best_results/ figures/

``all_results`` is for all interactions without filtering. ``best_results`` is for the interactions with 
filtering of `PIE <http://www.ncbi.nlm.nih.gov/CBBresearch/Wilbur/IRET/PIE/>`_ score. ``figures`` is for 
the figures of protein-protein interaction networks. There are two subfolders - ``with_strain`` and ``without_strain`` 
in these folders. These two folders store all information of interactions and literature scores. 
``with_strain`` is for the information with giving specific strain name for searching literatures. 
``without_strain`` is for the information without giving specific strain name for searching literatures.

::

    $ ls ANNOgesic/output/PPI/all_results/PPI_NC_000915.1/
    NC_000915.1_without_strain.csv  NC_000915.1_with_strain.csv     without_strain/               with_strain/
    $ ls ANNOgesic/output/PPI/best_results/PPI_NC_000915.1/
    NC_000915.1_without_strain.csv  NC_000915.1_with_strain.csv  without_strain  with_strain
    $ ls ANNOgesic/output/PPI/figures/PPI_NC_000915.1/
    without_strain  with_strain
    $ ls ANNOgesic/output/PPI/all_results/PPI_NC_000915.1/with_strain/NC_000915.1/
    carA_C694_01345.csv  carB_C694_01345.csv  pyrB_carB.csv        ribD_ribH.csv
    carA_carB.csv        carB_guaB.csv        pyrB_guaB.csv        rpsJ_nusB.csv
    carA_guaB.csv        guaB_C694_01345.csv  pyrD_C694_01345.csv
    carA_pyrB.csv        nusG_rpoB.csv        pyrE_pyrF.csv
    $ ls ANNOgesic/output/PPI/all_results/PPI_NC_000915.1/without_strain/NC_000915.1/
    carA_C694_01345.csv  carB_C694_01345.csv  pyrB_carB.csv        ribD_ribH.csv
    carA_carB.csv        carB_guaB.csv        pyrB_guaB.csv        rpsJ_nusB.csv
    carA_guaB.csv        guaB_C694_01345.csv  pyrD_C694_01345.csv
    carA_pyrB.csv        nusG_rpoB.csv        pyrE_pyrF.csv
    $ ls ANNOgesic/output/PPI/best_results/PPI_NC_000915.1/without_strain/NC_000915.1/
    carA_C694_01345.csv  carB_C694_01345.csv  pyrD_C694_01345.csv
    carA_carB.csv        guaB_C694_01345.csv
    $ ls ANNOgesic/output/PPI/best_results/PPI_NC_000915.1/with_strain/NC_000915.1/
      (It can't find any interactions)
    $ ls ANNOgesic/output/PPI/figures/PPI_NC_000915.1/with_strain/NC_000915.1/
    HP0001_nusB.png  HP0005_pyrF.png 
    $ ls ANNOgesic/output/PPI/figures/PPI_NC_000915.1/without_strain/NC_000915.1/
    P0001_nusB.png  HP0005_pyrF.png

Generating riboswitch
-----------------

If you want to know the riboswitchs, you can use the subcommand ``riboswitch``.
Before running ``riboswitch``, you need to get the information of known riboswitches in Rfam. 
You can download it from our `Github <https://github.com/Sung-Huan/ANNOgesic/tree/master/database>`_.

::

    $ wget -cP ANNOgesic/input/riboswitch_ID/ https://raw.githubusercontent.com/Sung-Huan/ANNOgesic/master/database/Rfam_riboswitch_ID.csv

You also need to download Rfam.

::

    $ wget -cP ANNOgesic/input/database ftp://ftp.ebi.ac.uk/pub/databases/Rfam/12.0/Rfam.tar.gz
    $ cd ANNOgesic/input/database
    $ tar -zxvf Rfam.tar.gz
    $ rm Rfam.tar.gz
    $ cd ../../../

Now we can try the subcommand.

::

    annogesic riboswitch \
        -g ANNOgesic/output/target/annotation \
        -f ANNOgesic/output/target/fasta \
        -i ANNOgesic/input/riboswitch_ID/Rfam_riboswitch_ID.csv \
        -R ANNOgesic/input/database/CMs/Rfam.cm \
        ANNOgesic

The output is the following. ``gffs`` is for gff files of riboswitchs; ``tables`` is for tables of riboswitchs; 
``scan_Rfam`` is for the output files of scanning Rfam; ``statistics`` is for the statistics files.

::

     $ ls ANNOgesic/output/riboswitch/
     gffs  scan_Rfam  statistics  tables
     $ ls ANNOgesic/output/riboswitch/gffs/
     NC_000915.1_riboswitch.gff
     $ ls ANNOgesic/output/riboswitch/scan_Rfam/NC_000915.1/
     NC_000915.1_riboswitch_prescan.txt  NC_000915.1_riboswitch_scan.txt
     $ ls ANNOgesic/output/riboswitch/tables/
     NC_000915.1_riboswitch.csv
     $ ls ANNOgesic/output/riboswitch/statistics/
     stat_NC_000915.1_riboswitch.txt


Producing the screenshots
-----------------

It is a good idea if we can get the screenshots of our interesting features. Then we can 
check them very quickly. Therefore, ANNOgesic provide a subcommand ``screenshot`` for 
generating screenshots.

Before you running it, you have to install `IGV <https://www.broadinstitute.org/software/igv/home>`_ 
for generating screenshot.

For testing, we use TSSs as main feature, sRNAs and CDSs information as side features.

::

    annogesic screenshot \
        -mg ANNOgesic/output/TSS/gffs/NC_000915.1_TSS.gff \
        -sg ANNOgesic/output/target/annotation/NC_000915.1.gff,ANNOgesic/output/sRNA/gffs/best/NC_000915.1_sRNA.gff \
        -f ANNOgesic/output/target/fasta/NC_000915.1.fa \
        -o ANNOgesic/output/TSS \
        -tl $tex_notex_libs \
        -tw ANNOgesic/input/wigs/tex_notex \
    ANNOgesic

``screenshot`` will generate two txt files and two folders.

::

    $ ls ANNOgesic/output/TSS/screenshots/NC_000915.1/
    forward/     forward.txt  reverse/     reverse.txt

``forward.txt`` and ``reverse.txt`` are batch files for `IGV <https://www.broadinstitute.org/software/igv/home>`_.
``forward`` and ``reverse`` are the folders for storing screenshots.

Now, please open `IGV <https://www.broadinstitute.org/software/igv/home>`_. Please follow the procedures: Tools -> 
Run Batch Script -> choose ``forward.txt``. When it has done, please do it again for reverse strand: Tools ->
Run Batch Script -> choose ``reverse.txt``. If you just want to test it and don't want to wait a long time for 
generating screenshots, you can delete some lines of gff files of TSSs.

After that, you can see that there are several screenshots in ``forward`` and ``reverse``.

::

    $ ls ANNOgesic/output/TSS/screenshots/NC_000915.1/forward
    ...
    NC_000915.1:1002230-1002230.png  NC_000915.1:1245705-1245705.png  NC_000915.1:1516949-1516949.png  NC_000915.1:246369-246369.png  NC_000915.1:463673-463673.png  NC_000915.1:741002-741002.png
    NC_000915.1:1002524-1002524.png  NC_000915.1:124623-124623.png    NC_000915.1:151822-151822.png    NC_000915.1:251753-251753.png  NC_000915.1:463731-463731.png  NC_000915.1:744418-744418.png
    NC_000915.1:1002728-1002728.png  NC_000915.1:1249488-1249488.png  NC_000915.1:1520156-1520156.png  NC_000915.1:255496-255496.png  NC_000915.1:464179-464179.png  NC_000915.1:744551-744551.png
    ...
    
    $ ls ANNOgesic/output/TSS/screenshots/NC_000915.1/reverse
    ...
    NC_000915.1:1002215-1002215.png  NC_000915.1:1235881-1235881.png  NC_000915.1:1481470-1481470.png  NC_000915.1:179609-179609.png  NC_000915.1:467716-467716.png  NC_000915.1:767765-767765.png
    NC_000915.1:1002707-1002707.png  NC_000915.1:1238472-1238472.png  NC_000915.1:1482537-1482537.png  NC_000915.1:181416-181416.png  NC_000915.1:46780-46780.png    NC_000915.1:769891-769891.png
    NC_000915.1:100498-100498.png    NC_000915.1:1240517-1240517.png  NC_000915.1:1482926-1482926.png  NC_000915.1:181781-181781.png  NC_000915.1:468289-468289.png  NC_000915.1:770316-770316.png
    ...


Coloring the screenshots
-----------------

If your RNA-seq data has a lot of tracks and you want to check TSSs, it will be painful for distinguish the 
tracks of TEX+ and TEX-. Therefore, we provide a subcommand ``color_png`` for coloring 
your screenshots.

::

    annogesic color_png \
        -t 2 \
        -f ANNOgesic/output/TSS \
        ANNOgesic

You will see the filenames of png files are the same as before. However, when you open them, the tracks are colored.

::

    $ ls ANNOgesic/output/TSS/screenshots/NC_000915.1/forward
    ...
    NC_000915.1:1002230-1002230.png  NC_000915.1:1245705-1245705.png  NC_000915.1:1516949-1516949.png  NC_000915.1:246369-246369.png  NC_000915.1:463673-463673.png  NC_000915.1:741002-741002.png
    NC_000915.1:1002524-1002524.png  NC_000915.1:124623-124623.png    NC_000915.1:151822-151822.png    NC_000915.1:251753-251753.png  NC_000915.1:463731-463731.png  NC_000915.1:744418-744418.png
    NC_000915.1:1002728-1002728.png  NC_000915.1:1249488-1249488.png  NC_000915.1:1520156-1520156.png  NC_000915.1:255496-255496.png  NC_000915.1:464179-464179.png  NC_000915.1:744551-744551.png
    ...
    
    $ ls ANNOgesic/output/TSS/screenshots/NC_000915.1/reverse
    ...
    NC_000915.1:1002215-1002215.png  NC_000915.1:1235881-1235881.png  NC_000915.1:1481470-1481470.png  NC_000915.1:179609-179609.png  NC_000915.1:467716-467716.png  NC_000915.1:767765-767765.png
    NC_000915.1:1002707-1002707.png  NC_000915.1:1238472-1238472.png  NC_000915.1:1482537-1482537.png  NC_000915.1:181416-181416.png  NC_000915.1:46780-46780.png    NC_000915.1:769891-769891.png
    NC_000915.1:100498-100498.png    NC_000915.1:1240517-1240517.png  NC_000915.1:1482926-1482926.png  NC_000915.1:181781-181781.png  NC_000915.1:468289-468289.png  NC_000915.1:770316-770316.png
    ...


Now you already finished your first wonderful trip of ANNOgesic. Hopefully, you enjoy it!!
