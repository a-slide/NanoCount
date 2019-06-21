# NanoCount

[![GitHub license](https://img.shields.io/github/license/a-slide/NanoCount.svg)](https://github.com/a-slide/NanoCount/blob/master/LICENSE)
[![PyPI version](https://badge.fury.io/py/NanoCount.svg)](https://badge.fury.io/py/NanoCount)
[![Downloads](https://pepy.tech/badge/NanoCount)](https://pepy.tech/project/NanoCount)

EM based transcript abundance from nanopore reads mapped to a transcriptome with minimap2
Python package adapted from https://github.com/jts/nanopore-rna-analysis by Jared Simpson

NanoCount estimates transcript abundance from ONT direct-RNA Sequencing reads mapped to a transcriptome. It uses an expectation-maximization approach like RSEM, Kallisto, salmon, etc to handle multi-mapping reads. The reads must be mapped to the transcript set using minimap2.

* Author: Adrien Leger - aleg {at} ebi.ac.uk (based on a prototype written by Jared Simpson)
* Licence: MIT
* Python version: 3.5 +

# Installation

Ideally, before installation, create a clean python3 virtual environment to deploy the package, using virtualenvwrapper for example (see http://www.simononsoftware.com/virtualenv-tutorial-part-2/).

### To install the package

```bash
pip3 install git+https://github.com/a-slide/NanoCount.git
```

### To update the package:

```bash
pip3 install git+https://github.com/a-slide/NanoCountbash.git --upgrade
```

# Usage

### Command line interface
```
usage: NanoCount [-h][--version] -i ALIGNMENT_FILE -o COUNT_FILE
                 [--min_read_length MIN_READ_LENGTH]
                 [--min_query_fraction_aligned MIN_QUERY_FRACTION_ALIGNED]
                 [--equivalent_threshold EQUIVALENT_THRESHOLD]
                 [--scoring_value SCORING_VALUE]
                 [--convergence_target CONVERGENCE_TARGET] [--verbose]

Calculate transcript abundance for a dRNA-Seq dataset from a BAM/SAM alignment file generated by minimap2

optional arguments:
  -h, --help            show this help message and exit
  --version, -v         show program's version number and exit
  -i ALIGNMENT_FILE, --alignment_file ALIGNMENT_FILE
                        BAM or SAM file containing aligned ONT dRNA-Seq reads including secondary and supplementary alignment
  -o COUNT_FILE, --count_file COUNT_FILE
                        Output count file
  --min_read_length MIN_READ_LENGTH
                        Minimal length of the read to be considered valid
  --min_query_fraction_aligned MIN_QUERY_FRACTION_ALIGNED
                        Minimal fraction of the primary hit query aligned to consider the read valid
  --equivalent_threshold EQUIVALENT_THRESHOLD
                        Fraction of the alignment score or the alignment
                        length of secondary hits compared to the primary hit to be considered valid hits
  --scoring_value SCORING_VALUE
                        Value to use for score thresholding of secondary hits. Either alignment_score or alignment_length
  --convergence_target CONVERGENCE_TARGET
                        Convergence target value of the cummulative difference between abundance values of successive EM round to trigger the end of the EM loop
  --verbose             If True will be chatty
```

Output file exemple

```
transcript_name	raw	est_count	tpm
ENSDART00000023156|ENSDARG00000020850	0.009360321697698902	277.0000000000036	277000000.0000036
ENSDART00000093609|ENSDARG00000063908	0.0075017740681919	222.0000000000029	222000000.0000029
ENSDART00000052511|ENSDARG00000036161	0.0063190619403238075	187.00000000000244	187000000.00000244
ENSDART00000093606|ENSDARG00000063905	0.00615010306491408	182.00000000000236	182000000.00000235
ENSDART00000146211|ENSDARG00000020504	0.006076357615676965	179.81765092072843	179817650.92072842
ENSDART00000028885|ENSDARG00000028335	0.005410518932099315	160.11348675761502	160113486.75761503
ENSDART00000058715|ENSDARG00000040141	0.005237725137701552	155.00000000000202	155000000.00000203
ENSDART00000074787|ENSDARG00000052856	0.004385241613334473	129.77245506340708	129772455.06340708
ENSDART00000093613|ENSDARG00000063912	0.0036495117088501134	108.0000000000014	108000000.0000014
```

### Interactive Python environment (jupyter, ipython...)

The same options as for the command line are available, but it allows to use the package as an API and access more internal information

```python3
from NanoCount.NanoCount import NanoCount_main
n = NanoCount_main (alignment_file="transcriptome_aligned_reads.bam", verbose=True)
```

```
Parse Bam file and filter low quality hits
    Mapped hits:118237
    Wrong strand hits:1139
    Unmapped hits:38325
    Valid best hit:72427
    Valid secondary hit:31298
    Invalid secondary hit:12695
    Best hit with low query fraction aligned:1066
Generate initial read/transcript compatibility index
Start EM abundance estimate
........
Convergence target reached after 8 rounds
Convergence value = 0.004801809595549253
```

The count results are stored in a Pandas Dataframe that can be conveniently rendered in Jupyter
```python3
display(n.count_df)
```

| **transcript_name**                        | **raw**     | **est_count** | **tpm**    |
| ------------------------------------------ | ----------- | ------------- | ---------- |
| **ENSDART00000010144\|ENSDARG00000002768** | 0.0319356   | 2313          | 2313000000 |
| **ENSDART00000055062\|ENSDARG00000037789** | 0.02688224  | 1947          | 1947000000 |
| **ENSDART00000055136\|ENSDARG00000037840** | 0.01905367  | 1380          | 1380000000 |
| **ENSDART00000093609\|ENSDARG00000063908** | 0.01818383  | 1317          | 1317000000 |
| **ENSDART00000023156\|ENSDARG00000020850** | 0.01186022  | 859           | 859000000  |
| **ENSDART00000093612\|ENSDARG00000063911** | 0.008146133 | 590           | 590000000  |
| **ENSDART00000123003\|ENSDARG00000067990** | 0.007874959 | 570.3596      | 570359600  |
| **ENSDART00000012644\|ENSDARG00000017624** | 0.007097575 | 514.0561      | 514056100  |
| **ENSDART00000093613\|ENSDARG00000063912** | 0.006862082 | 497           | 497000000  |

# Note to power-users and developers

Please be aware this package is experimental . It was tested under Linux Ubuntu 16.04 and in an HPC environment running under Red Hat Enterprise 7.1.

You are welcome to contribute by requesting additional functionalities, reporting bugs or by forking and submitting patches or updates pull requests

Thank you
