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

    @property
    def primary_hit (self):
        for hit in self.hit_list:
            if not hit.secondary:
                return hit

    @property
    def secondary_hit_list (self):
        hit_list = []
        for hit in self.hit_list:
            if hit.secondary:
                hit_list.append (hit)
        return hit_list

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
        if not self.secondary:
            return self.align_len/self.qlen
