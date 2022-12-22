# NanoCount v1.1.0

![NanoCount](./docs/pictures/NanoCount.png)

[![GitHub license](https://img.shields.io/github/license/a-slide/NanoCount.svg)](https://github.com/a-slide/NanoCount/blob/master/LICENSE)
[![Language](https://img.shields.io/badge/Language-Python3.6+-yellow.svg)](https://www.python.org/)
[![DOI](https://zenodo.org/badge/142873004.svg)](https://zenodo.org/badge/latestdoi/142873004)

[![PyPI version](https://badge.fury.io/py/NanoCount.svg)](https://badge.fury.io/py/NanoCount)
[![PyPI downloads](https://pepy.tech/badge/NanoCount)](https://pepy.tech/project/NanoCount)
[![Anaconda Version](https://anaconda.org/aleg/nanocount/badges/version.svg)](https://anaconda.org/aleg/nanocount)
[![Anaconda Downloads](https://anaconda.org/aleg/nanocount/badges/downloads.svg)](https://anaconda.org/aleg/nanocount)
---

**NanoCount estimates transcript abundances from Oxford Nanopore *direct RNA sequencing* datasets, using filtering steps and an expectation-maximization approach (similar to RSEM, Kallisto, Salmon, etc) to handle the uncertainty of multi-mapping reads**

Further documentation is available at: https://a-slide.github.io/NanoCount/

---

### Installation

Install with pip from GitHub.

```
pip install git+https://github.com/a-slide/NanoCount.git
```

### Read alignment prior to NanoCount

Reads should be aligned to a transcriptome reference using minimap2. We recommend using the -N 10 option to retain at least 10 secondary mappings.

```
minimap2 -t 4 -ax map-ont -N 10 transcriptome.fasta reads.fastq | samtools view -bh > aligned_reads.bam
```

### General Command Line Usage

```
NanoCount --help
```

```
usage: NanoCount [-h] [--version] -i ALIGNMENT_FILE [-o COUNT_FILE]
                 [-b FILTER_BAM_OUT] [-l MIN_ALIGNMENT_LENGTH]
                 [-f MIN_QUERY_FRACTION_ALIGNED] [-s SEC_SCORING_VALUE]
                 [-t SEC_SCORING_THRESHOLD] [-c CONVERGENCE_TARGET]
                 [-e MAX_EM_ROUNDS] [-x] [-p PRIMARY_SCORE] [-a]
                 [-d MAX_DIST_3_PRIME] [-u MAX_DIST_5_PRIME] [-v] [-q]

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit

Input/Output options:
  -i ALIGNMENT_FILE, --alignment_file ALIGNMENT_FILE
                        Sorted and indexed BAM or SAM file containing aligned
                        ONT direct RNA reads including secondary alignments
                        (required) [str]
  -o COUNT_FILE, --count_file COUNT_FILE
                        Output file path where to write estimated counts (TSV
                        format) (default: None) [str]
  -b FILTER_BAM_OUT, --filter_bam_out FILTER_BAM_OUT
                        Optional output file path where to write filtered
                        reads selected by NanoCount to perform quantification
                        estimation (BAM format) (default: None) [str]

Misc options:
  -l MIN_ALIGNMENT_LENGTH, --min_alignment_length MIN_ALIGNMENT_LENGTH
                        Minimal length of the alignment to be considered valid
                        (default: 50) [int]
  -f MIN_QUERY_FRACTION_ALIGNED, --min_query_fraction_aligned MIN_QUERY_FRACTION_ALIGNED
                        Minimal fraction of the primary alignment query
                        aligned to consider the read valid (default: 0.5)
                        [float]
  -s SEC_SCORING_VALUE, --sec_scoring_value SEC_SCORING_VALUE
                        Value to use for score thresholding of secondary
                        alignments either "alignment_score" or
                        "alignment_length" (default: alignment_score) [str]
  -t SEC_SCORING_THRESHOLD, --sec_scoring_threshold SEC_SCORING_THRESHOLD
                        Fraction of the alignment score or the alignment
                        length of secondary alignments compared to the primary
                        alignment to be considered valid alignments (default:
                        0.95) [float]
  -c CONVERGENCE_TARGET, --convergence_target CONVERGENCE_TARGET
                        Convergence target value of the cummulative difference
                        between abundance values of successive EM round to
                        trigger the end of the EM loop. (default: 0.005)
                        [float]
  -e MAX_EM_ROUNDS, --max_em_rounds MAX_EM_ROUNDS
                        Maximum number of EM rounds before triggering stop
                        (default: 100) [int]
  -x, --extra_tx_info   Add transcript length and zero coverage transcripts
                        to the output file (required valid bam/sam header)
                        (default: False) [boolean]
  -p PRIMARY_SCORE, --primary_score PRIMARY_SCORE
                        Method to pick the best alignment for each read. By
                        default ("alignment_score") uses the best alignment
                        score (AS optional field), but it can be changed to
                        use either the primary alignment defined by the
                        aligner ("primary") or the longest alignment
                        ("alignment_length"). Choices = [primary,
                        alignment_score, alignment_length] (default:
                        alignment_score) [str]
  -a, --keep_suplementary
                        Retain any supplementary alignments and considered
                        them like secondary alignments. Discarded by default.
                        (default: False) [boolean]
  -n, --keep_neg_strand
                        Retain negative strand alignments for ONT cDNA data. 
                        Un-tested and not benchmarked. Use with caution.
  -d MAX_DIST_3_PRIME, --max_dist_3_prime MAX_DIST_3_PRIME
                        Maximum distance of alignment end to 3 prime of
                        transcript. In ONT direct RNA sequencing, reads are assumed to start
                        from the polyA tail (-1 to deactivate) (default: 50)
                        [int]
  -u MAX_DIST_5_PRIME, --max_dist_5_prime MAX_DIST_5_PRIME
                        Maximum distance of alignment start to 5 prime of
                        transcript. In conjunction with max_dist_3_prime it
                        can be used to select near full length transcript reads only
                        (-1 to deactivate). (default: -1) [int]

Verbosity options:
  -v, --verbose         Increase verbosity for QC and debugging (default:
                        False) [boolean]
  -q, --quiet           Reduce verbosity (default: False) [boolean]
```

Basic command:

```
NanoCount -i data/aligned_reads_sorted.bam -b output/aligned_reads_selected.bam --extra_tx_info -o output/tx_counts.tsv
```

### Input BAM file

NanoCount is designed for Oxford Nanopore direct RNA sequencing datasets only.

Reads should be aligned to a transcriptome reference using minimap2. We recommend using the -N 10 option to retain at least 10 secondary mappings. For highly repetitive transcriptomes, this value can be increased.

Since we use a transcriptome reference the alignment algorithm does not have to be splice aware.

NanoCount can take either BAM or SAM format and does not require reads to be sorted, although it is recommended.

### Output TSV file

NanoCount returns a file containing count data per transcript. By default only transcripts with at least one read mapped are included in the report. This behaviour can be changed to include all transcripts with the option extra_tx_info.

- **transcript_name**: Transcript name as in source bam/sam file.
- **raw**: Raw abundance estimates. The sum of all abundance values is 1.
- **est_count**: Estimated counts obtained by multiplying the raw abundance by the number of primary alignments.
- **tpm**: Estimated counts obtained by multiplying the raw abundance by 1M.
- **transcript_length**: Optional column included with the option extra_tx_info.

Tpm and estimated counts are not normalised by transcript length as usually done with short-read sequencing. The reason is that in long-read direct RNA sequencing one read is supposed to represent a single transcript molecule starting from the polyA tail, even if the fragment doesn't extend to the 5' end. If using a custom protocol allowing sequencing to start from internal RNA fragments (whole RNA tailing, degenerated custom adapter), then this prior is not verified any more.

### Output BAM file

Optionally, users can choose to dump the filtered alignments selected by NanoCount for downstream analysis such ad QC or visualisation. The alignments are written in the same order as the source BAM file.

### Citation

If you use NanoCount please cite as follows:

Josie Gleeson, Adrien Leger, Yair D J Prawer, Tracy A Lane, Paul J Harrison, Wilfried Haerty, Michael B Clark, Accurate expression quantification from nanopore direct RNA sequencing with NanoCount, Nucleic Acids Research, Volume 50, Issue 4, 28 February 2022, Page e19, https://doi.org/10.1093/nar/gkab1129

### Disclaimer

Please be aware that NanoCount is a research package that is still under development.

The API, command line interface, and implementation might change without retro-compatibility.

It was tested under Linux Ubuntu 16.04 and in an HPC environment running under Red Hat Enterprise 7.1.

### Licence

MIT (https://mit-license.org/)

Copyright © 2020 Adrien Leger

### Acknowledgements

The package was inspired from https://github.com/jts/nanopore-rna-analysis by Jared Simpson

* Jared Simpson (@jts)

### Classifiers

* Development Status :: 3 - Alpha
* Intended Audience :: Science/Research
* Topic :: Scientific/Engineering :: Bio-Informatics
* License :: OSI Approved :: MIT License
* Programming Language :: Python :: 3
