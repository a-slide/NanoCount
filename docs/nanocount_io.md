# NanoCount Input / Output

## Input BAM file

NanoCount is meant to be used with Oxford Nanopore **direct-RNA** sequencing datasets only.

Reads should be aligned to a **transcriptome reference** using **[minimap2](https://github.com/lh3/minimap2)**. We recommend using the `-N 10` option to retain at least 10 secondary mappings. For highly repetitive transcriptomes, this value can even be increased.

Since we use a transcriptome reference the alignment algorithm does not have to be splice aware.

Nanocount can take either BAM or SAM format and does not require reads to be sorted, although sorting the reads with samtools will make secondary sampling deterministic, so it is recommended.

Here is an example minimap2 command line with optional conversion to BAM format with samtools then sorting and indexing with samtools.

```
minimap2 -t 8 -ax map-ont -N 10 ./data/yeast_ref.fa.gz ./data/yeast_reads.fastq.gz | samtools view -bh > ./output/aligned_reads.bam

samtools sort -o ./output/aligned_sorted_reads.bam ./output/aligned_reads.bam

samtools index ./output/aligned_sorted_reads.bam
```


### Output TSV file

NanoCount returns a file containing count data per transcripts.
By default only transcripts with at least one read mapped are included in the report.
This behaviour can be changed to include all transcripts with the option `extra_tx_info`.

Here is a example tabulated count file returned by NanoCount:

```
transcript_name raw                  est_count          tpm                transcript_length
YHR174W_mRNA    0.5847481080119605   51228.61224671184  584748.1080119605  1314              
YGR192C_mRNA    0.015286737423038144 1339.2404921575258 15286.737423038145 999               
YGR254W_mRNA    0.011624369387633806 1018.3877533118225 11624.369387633806 1314              
YLR110C_mRNA    0.00945119167199341  827.9999999999986  9451.19167199341   402               
YJR009C_mRNA    0.009088112600958011 796.1913687447295  9088.112600958011  999               
YOL086C_mRNA    0.008275499954342055 724.9999999999987  8275.499954342056  1047              
YKL060C_mRNA    0.006597570998082356 577.9999999999991  6597.570998082356  1080              
YBR118W_mRNA    0.005222125833257228 457.49999999999926 5222.125833257228  1377              
YPR080W_mRNA    0.005222125833257228 457.49999999999926 5222.125833257228  1377    
```

**Description of fields**

* transcript_name : Transcript name as in source Bam/Sam file.
* raw: Raw abundance estimates. The sum of all abundance values is 1.
* est_count: Estimated counts obtained by multiplying the raw abundance by the number of primary alignments.
* tpm: Estimated counts obtained by multiplying the raw abundance by 1M.
* transcript_length: Optional column included with the option `extra_tx_info`.

tpm and estimated counts are not normalised by transcript length as it is usually done with Illumina data.
The reason is that in dRNA-Seq one read is supposed to represent a single transcript molecule starting from the polyA tail, even if the fragment doesn't extend to the 5' end.
If using a custom protocol allowing to sequence from internal RNA fragments (whole RNA tailing, degenerated custom adapter), then this prior is not verified any more.

### Output BAM file

Optionally, users can choose to dump the alignments selected by Nanocount for the transcripts
estimate step, for QC or visualisation purpose. The alignments are written in the same order
as the source BAM file.
