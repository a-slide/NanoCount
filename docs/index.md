# Welcome to NanoCount v1.1.0.post1 documentation

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

Reads should be aligned to a **transcriptome reference** using **[minimap2](https://github.com/lh3/minimap2)**.
We recommend using the `-N 10` option to retain at least 10 secondary mappings.

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

Josie Gleeson, Adrien Leger, Yair D J Prawer, Tracy A Lane, Paul J Harrison, Wilfried Haerty, Michael B Clark, Accurate expression quantification from nanopore direct RNA sequencing with NanoCount, Nucleic Acids Research, 2021;, gkab1129, https://doi.org/10.1093/nar/gkab1129

### licence

MIT (https://mit-license.org/)

Copyright © 2020 Adrien Leger

### Authors

* Adrien Leger / aleg@ebi.ac.uk / https://adrienleger.com

The package was inspired from https://github.com/jts/nanopore-rna-analysis by Jared Simpson

* Jared Simpson (@jts)
