#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# ~~~~~~~~~~~~~~IMPORTS~~~~~~~~~~~~~~ #
# Standard library imports

# Third party imports
import pysam

# Local imports

# ~~~~~~~~~~~~~~CLASS READ~~~~~~~~~~~~~~ #
class Read(object):
    """
    Represent a read from the original fastq file associated with alignments found
    by minimap2
    """

    # ~~~~~~~~~~~~~~MAGIC METHODS~~~~~~~~~~~~~~ #
    def __init__(self):
        self.alignment_list = []

    def __repr__(self):
        m = ""
        for r in self.alignment_list:
            m += "\t\t{}\n".format(r)
        return m

    # ~~~~~~~~~~~~~~PROPERTY METHODS~~~~~~~~~~~~~~ #
    @property
    def n_alignment(self):
        return len(self.alignment_list)

    # ~~~~~~~~~~~~~~PUBLIC METHODS~~~~~~~~~~~~~~ #
    def get_best_alignment(self, primary_score="alignment_score"):
        primary_alignment_idx = self._get_primary_idx(primary_score=primary_score)
        return self.alignment_list[primary_alignment_idx]

    def get_secondary_alignments_list(self, primary_score="alignment_score"):
        primary_alignment_idx = self._get_primary_idx(primary_score=primary_score)
        return [
            alignment
            for i, alignment in enumerate(self.alignment_list)
            if i != primary_alignment_idx
        ]

    def add_pysam_alignment(self, pysam_aligned_segment, read_idx, **kwargs):
        self.alignment_list.append(Alignment(pysam_aligned_segment, read_idx))

    def add_alignment(self, alignment, **kwargs):
        self.alignment_list.append(alignment)

    # ~~~~~~~~~~~~~~PRIVATE METHODS~~~~~~~~~~~~~~ #
    def _get_primary_idx(self, primary_score="alignment_score"):
        idx = 0
        if primary_score == "alignment_score":
            best_align_score = -1
            for i, alignment in enumerate(self.alignment_list):
                if alignment.align_score > best_align_score:
                    best_align_score = alignment.align_score
                    idx = i
        elif primary_score == "primary":
            for i, alignment in enumerate(self.alignment_list):
                if not alignment.secondary:
                    idx = i
        elif primary_score == "alignment_length":
            best_align_len = -1
            for i, alignment in enumerate(self.alignment_list):
                if alignment.align_len > best_align_len:
                    best_align_len = alignment.align_len
                    idx = i
        return idx


# ~~~~~~~~~~~~~~CLASS HIT~~~~~~~~~~~~~~ #
class Alignment:
    """
    Helper class to extract relevant fields from the a pysam alignedSegment object
    """

    # ~~~~~~~~~~~~~~MAGIC METHODS~~~~~~~~~~~~~~ #
    def __init__(self, pysam_aligned_segment, read_idx):
        """"""
        self.qname = pysam_aligned_segment.query_name
        self.rname = pysam_aligned_segment.reference_name
        qlen = int(pysam_aligned_segment.query_length)
        if qlen == 0:
            self.qlen = int(pysam_aligned_segment.infer_query_length())
        else:
            self.qlen = qlen
        self.align_len = int(pysam_aligned_segment.query_alignment_length)
        self.align_score = int(pysam_aligned_segment.get_tag("AS"))
        self.secondary = (
            pysam_aligned_segment.is_secondary or pysam_aligned_segment.is_supplementary
        )
        self.read_idx = read_idx

    def __repr__(self):
        return "Query:{} | Reference:{} | Query len:{} | Alignment len:{} | Align Score:{} | Secondary:{}".format(
            self.qname,
            self.rname,
            self.qlen,
            self.align_len,
            self.align_score,
            self.secondary,
        )

    # ~~~~~~~~~~~~~~PROPERTY METHODS~~~~~~~~~~~~~~ #
    @property
    def query_fraction_aligned(self):
        if self.qlen == 0:
            return 0
        else:
            return self.align_len / self.qlen
