# NanoCount

EM based transcript abundance from nanopore reads mapped to a transcriptome with minimap2
Python package adapted from https://github.com/jts/nanopore-rna-analysis by Jared Simpson

NanoCount estimates transcript abundance from ONT direct-RNA Sequencing reads mapped to a transcriptome. It uses an expectation-maximization approach like RSEM, Kallisto, salmon, etc to handle multi-mapping reads. The reads must be mapped to the transcript set using minimap2.
