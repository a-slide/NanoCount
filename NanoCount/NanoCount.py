#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#~~~~~~~~~~~~~~IMPORTS~~~~~~~~~~~~~~#
# Standard library imports
from collections import *

# Third party imports
import pysam
import pandas as pd

# Local imports
from NanoCount.Read import Read
from NanoCount.common import *

#~~~~~~~~~~~~~~MAIN FUNCTION~~~~~~~~~~~~~~#
class NanoCount ():

    #~~~~~~~~~~~~~~MAGIC METHODS~~~~~~~~~~~~~~#
    def __init__ (self,
        alignment_file,
        min_read_length = 50,
        min_query_fraction_aligned = 0.5,
        equivalent_threshold = 0.9,
        scoring_value = "alignment_score",
        convergence_target = 0.005,
        verbose = False):
        """
        * alignment_file
            BAM or SAM file containing aligned ONT dRNA-Seq reads including
            secondary and supplementary alignment
        * min_read_length INT
            Minimal length of the read to be considered valid
        * min_query_fraction_aligned FLOAT
            Minimal fraction of the primary hit query aligned to consider the
            read valid
        * equivalent_threshold FLOAT
            Fraction of the alignment score or the alignment length of secondary
            hits compared to the primary hit to be considered valid hits
        * scoring_value STR
            Value to use for score thresholding of secondary hits
            Either "alignment_score" or "alignment_length"
        * convergence_target FLOAT
            Convergence target value of the cummulative difference between
            abundance values of successive EM round to trigger the end of the
            EM loop.
        """
        # Save args in self variables
        self.alignment_file = alignment_file
        self.min_read_length = min_read_length
        self.min_query_fraction_aligned = min_query_fraction_aligned
        self.equivalent_threshold = equivalent_threshold
        self.scoring_value = scoring_value
        self.convergence_target = convergence_target
        self.verbose = verbose

        if self.verbose:
            stderr_print ("Run parameters\n")
            stderr_print ("\tMinimal read length:{}\n".format(min_read_length))
            stderr_print ("\tMinimal aligned fraction of query read:{}\n".format(min_query_fraction_aligned))
            stderr_print ("\tEquivalent threshold:{}\n".format(equivalent_threshold))
            stderr_print ("\tScoring value:{}\n".format(scoring_value))
            stderr_print ("\tConvergence target:{}\n".format(convergence_target))

        # Collect all hits grouped by read name
        stderr_print ("Parse Bam file and filter low quality hits\n")
        self.read_dict = self._parse_bam ()

        # Generate compatibility dict grouped by reads
        stderr_print ("Generate initial read/transcript compatibility index\n")
        self.compatibility_dict = self._get_compatibility ()

        # EM loop to calculate abundance and update read-transcript compatibility
        stderr_print ("Start EM abundance estimate\n")
        em_round = 0

        while True:
            em_round += 1
            stderr_print (".")

            # Calculate abundance from compatibility assignments
            self.abundance_dict = self._calculate_abundance (em_round)

            # Trigger stop if convergence reached
            if self.convergence <= self.convergence_target:
                if self.verbose:
                    stderr_print ("\nConvergence target reached after {} rounds\n".format (em_round))
                    stderr_print ("Convergence value = {}\n".format(self.convergence))
                break

            # Failsafe if convergence not reached
            if em_round == 100:
                if self.verbose:
                    stderr_print ("\nCannot reach convergence after 100 rounds\n")
                    stderr_print ("Convergence value = {}\n".format(self.convergence))
                break

            # Update compatibility assignments
            self.compatibility_dict = self._update_compatibility ()

        # Final line
        stderr_print("\n")

    #~~~~~~~~~~~~~~PROPERTY METHODS~~~~~~~~~~~~~~#
    @property
    def count_df (self):
        """
        Transform abundance dict to a Dataframe contaning the estimated count and TPM per transcripts
        """
        df = pd.DataFrame (self.abundance_dict.most_common(), columns=["transcript_name","raw"])
        df.set_index("transcript_name", inplace=True, drop=True)
        df["est_count"] = df["raw"]*len(self.read_dict)
        df["tpm"] = df["est_count"] * 1000000
        return df

    #~~~~~~~~~~~~~~PUBLIC METHODS~~~~~~~~~~~~~~#
    def write_count_file (self, count_file):
        """
        Write the final count results to a given file
        """
        if self.verbose:
            stderr_print ("Write output count file")
        self.count_df.to_csv (count_file, sep="\t")

    #~~~~~~~~~~~~~~PRIVATE METHODS~~~~~~~~~~~~~~#
    def _parse_bam (self):
        """
        Parse Bam/Sam file, group hits per reads, filter reads based on
        selection criteria and return a dict of valid read/hits
        """
        # Parse bam files
        c = Counter()
        read_dict = defaultdict (Read)
        with pysam.AlignmentFile (self.alignment_file) as bam:
            for hit in bam:
                if hit.is_unmapped:
                    c["Unmapped hits"] +=1
                elif hit.is_reverse:
                    c["Wrong strand hits"] +=1
                else:
                    c["Mapped hits"] +=1
                    read_dict [hit.query_name].add_pysam_hit (hit)

        # Filter hits
        filtered_read_dict = defaultdict (Read)

        for query_name, read in read_dict.items ():
            # Check if best hit is valid
            best_hit = read.primary_hit

            # In case the primary hit was removed by filters
            if best_hit:
                if best_hit.qlen < self.min_read_length:
                    c["Read too short"] +=1
                elif best_hit.query_fraction_aligned < self.min_query_fraction_aligned:
                    c["Best hit with low query fraction aligned"] +=1
                else:
                    filtered_read_dict [query_name].add_hit (best_hit)
                    c["Valid best hit"] +=1
                    for hit in read.secondary_hit_list:

                        # Filter out secondary hits based on minimap alignment score
                        if self.scoring_value == "alignment_score" and hit.align_score/best_hit.align_score < self.equivalent_threshold:
                            c["Invalid secondary hit"] += 1

                        # Filter out secondary hits based on minimap alignment length
                        elif self.scoring_value == "alignment_length" and hit.align_len/best_hit.align_len < self.equivalent_threshold:
                            c["Invalid secondary hit"] += 1

                        # Select valid secondary hits
                        else:
                            c["Valid secondary hit"] += 1
                            filtered_read_dict [query_name].add_hit (hit)

        # Write filtered reads counters
        if self.verbose:
            for i, j in c.items():
                stderr_print ("\t{}:{}\n".format(i,j))

        return filtered_read_dict

    def _get_compatibility (self):
        """
        """
        compatibility_dict = defaultdict(dict)
        for read_name, read in self.read_dict.items ():
            for hit in read.hit_list:
                compatibility_dict[read_name][hit.rname] = score=1.0/read.n_hit

        return compatibility_dict

    def _calculate_abundance (self, em_round):
        """
        Calculate the abundance of the transcript set based on read-transcript compatibilities
        """
        abundance_dict = Counter()
        total = 0
        convergence = 0

        for read_name, comp in self.compatibility_dict.items ():
            for ref_name, score in comp.items():
                abundance_dict [ref_name] += score
                total += score

        for ref_name in abundance_dict.keys():
            abundance_dict [ref_name] = abundance_dict[ref_name] / total

            if em_round > 1:
                convergence += abs (self.abundance_dict [ref_name] - abundance_dict [ref_name])

        if em_round == 1:
            self.convergence = 1
        else:
            self.convergence = convergence

        return abundance_dict

    def _update_compatibility (self):
        """
        Update read-transcript compatibility based on transcript abundances
        """
        compatibility_dict = defaultdict (dict)

        for read_name, comp in self.compatibility_dict.items ():
            total=0
            for ref_name in comp.keys ():
                total += self.abundance_dict [ref_name]

            for ref_name in comp.keys ():
                compatibility_dict[read_name][ref_name] = self.abundance_dict [ref_name] / total

        return compatibility_dict
