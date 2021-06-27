# Welcome to NanoCount v0.2.5 documentation

[NanoCount](pictures/NanoCount.png)

[![GitHub license](https://img.shields.io/github/license/a-slide/NanoCount.svg)](https://github.com/a-slide/NanoCount/blob/master/LICENSE)
[![Language](https://img.shields.io/badge/Language-Python3.6+-yellow.svg)](https://www.python.org/)
[![DOI](https://zenodo.org/badge/142873004.svg)](https://zenodo.org/badge/latestdoi/142873004)
[![Build Status](https://travis-ci.com/a-slide/NanoCount.svg?branch=master)](https://travis-ci.com/a-slide/NanoCount)

[![PyPI version](https://badge.fury.io/py/NanoCount.svg)](https://badge.fury.io/py/NanoCount)
[![PyPI downloads](https://pepy.tech/badge/NanoCount)](https://pepy.tech/project/NanoCount)
[![Anaconda Version](https://anaconda.org/aleg/nanocount/badges/version.svg)](https://anaconda.org/aleg/nanocount)
[![Anaconda Downloads](https://anaconda.org/aleg/nanocount/badges/downloads.svg)](https://anaconda.org/aleg/nanocount)

---

**NanoCount estimates transcripts abundance from Oxford Nanopore *direct-RNA sequencing* datasets, using an expectation-maximization approach like RSEM, Kallisto, salmon, etc to handle the uncertainty of multi-mapping reads**

---

### Quick start

#### Align reads

Reads must be aligned a transcriptome reference using minimap2 with `-p 0 -N 10` options to retain up to 10 secondary mappings without filtering.
NanoCount will take care of the low score alignments internally.

```
minimap2 -t 4 -ax map-ont -p 0 -N 10 transcriptome.fa.gz reads.fastq.gz | samtools view -bh > aligned_reads.bam
```

#### Estimate transcripts abundance with NanoCount

```
NanoCount -i aligned_reads.bam -o transcript_counts.tsv
```

### Detailed instructions

* [Installation](installation)
* [Command line Usage](NanoCount_CLI_usage)
* [Python API Usage](NanoCount_API_usage)
* [Input / Output formats](nanocount_io)

### citation

The repository is archived at Zenodo. If you use NanoCount please cite as follow:

Adrien Leger. (2020, January 28). a-slide/NanoCount. Zenodo. https://zenodo.org/badge/latestdoi/142873004

### licence

MIT (https://mit-license.org/)

Copyright © 2020 Adrien Leger

### Authors

* Adrien Leger / aleg@ebi.ac.uk / https://adrienleger.com

The package was inspired from https://github.com/jts/nanopore-rna-analysis by Jared Simpson

* Jared Simpson (@jts)
