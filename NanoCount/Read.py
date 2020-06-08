#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#~~~~~~~~~~~~~~IMPORTS~~~~~~~~~~~~~~#
# Standard library imports

# Third party imports
import pysam

# Local imports

#~~~~~~~~~~~~~~CLASS READ~~~~~~~~~~~~~~#
class Read (object):
    """
    Represent a read from the original fastq file associated with hits found
    by minimap2
    """

    #~~~~~~~~~~~~~~MAGIC METHODS~~~~~~~~~~~~~~#
    def __init__(self):
        """
        """
        self.hit_list = []

    def __repr__(self):
        m = ""
        for r in self.hit_list:
            m +="\t\t{}\n".format(r)
        return (m)

    #~~~~~~~~~~~~~~PROPERTY METHODS~~~~~~~~~~~~~~#
    @property
    def n_hit (self):
        return len(self.hit_list)

    def get_primary_idx (self, primary_score=""):

        idx = 0
        if not primary_score:
            for i, hit in enumerate(self.hit_list):
                if not hit.secondary:
                    idx = i

        elif primary_score == "align_score":
            best_align_score = -1
            for i, hit in enumerate(self.hit_list):
                if hit.align_score > best_align_score:
                    best_align_score = hit.align_score
                    idx = i

        elif primary_score == "align_len":
            best_align_len = -1
            for i, hit in enumerate(self.hit_list):
                if hit.align_len > best_align_len:
                    best_align_len = hit.align_len
                    idx = i

        return i

    def get_primary_hit (self, primary_score=""):
        primary_hit_idx = self.get_primary_idx(primary_score)
        return self.hit_list[primary_hit_idx]

    def get_secondary_hit_list (self, primary_score=""):
        primary_hit_idx = self.get_primary_idx(primary_score)
        return [hit for i, hit in enumerate(self.hit_list) if i != primary_hit_idx]

    #~~~~~~~~~~~~~~PUBLIC METHODS~~~~~~~~~~~~~~#
    def add_pysam_hit (self, pysam_aligned_segment, **kwargs):
        self.hit_list.append (Hit (pysam_aligned_segment))

    def add_hit (self, hit, **kwargs):
        self.hit_list.append (hit)

#~~~~~~~~~~~~~~CLASS HIT~~~~~~~~~~~~~~#
class Hit ():
    """
    Helper class to extract relevant fields from the a pysam alignedSegment object
    """

    #~~~~~~~~~~~~~~MAGIC METHODS~~~~~~~~~~~~~~#
    def __init__(self, pysam_aligned_segment):
        """
        """
        self.qname = pysam_aligned_segment.query_name
        self.rname = pysam_aligned_segment.reference_name
        self.qlen = int (pysam_aligned_segment.query_length)
        self.align_len = int (pysam_aligned_segment.query_alignment_length)
        self.align_score = int (pysam_aligned_segment.get_tag("AS"))
        self.secondary = pysam_aligned_segment.is_secondary or pysam_aligned_segment.is_supplementary

    def __repr__(self):
        return "Query:{} | Reference:{} | Query len:{} | Alignment len:{} | Align Score:{} | Secondary:{}".format(
            self.qname, self.rname, self.qlen, self.align_len, self.align_score, self.secondary)

    #~~~~~~~~~~~~~~PROPERTY METHODS~~~~~~~~~~~~~~#
    @property
    def query_fraction_aligned (self):
        return self.align_len/self.qlen
