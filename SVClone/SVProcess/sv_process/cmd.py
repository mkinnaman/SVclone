#!/usr/bin/env python

'''
Commandline input for running SV post-processing script
'''

import argparse
from . import process

parser = argparse.ArgumentParser(prefix_chars='--')
parser.add_argument("-i","--input",dest="svin",required=True,
        help="Structural variants input file. See README for input format")
parser.add_argument("-b","--bam",dest="bam",required=True,
        help="Corresponding indexed BAM file")
parser.add_argument("-o","--out",dest="out",required=True,
        help="Output base name. May contain directories. " + \
             "Will create processed output as <name>.txt and database output as <name>.db")
parser.add_argument("-d","--depth",dest="mean_dp",type=float,default=50,
        help="Average coverage for BAM file in covered region. May be calculated across binned intervals " + \
             "and may be approximate")
parser.add_argument("-sc","--softclip_bp",dest="sc_len",default=25,type=int,
        help="Optional: minimum number of basepairs by which reads spanning the break are considered support " + \
             "the breakpoint. Also affects number of base-pairs a normal read must overlap the break to be " + \
             "counted. Default = 25")
parser.add_argument("-cn","--max_cn",dest="max_cn",default=10,type=int,
        help="Optional: maximum expected copy-number. Will skip the processing of any areas where" + \
             "# reads > average coverage * max_cn")
parser.add_argument("-r","--read_len",dest="rlen",default=-1,type=int,
        help="Read length. If not specified, will be inferred")
parser.add_argument("-v","--insert_mean",dest="insert_mean",default=-1.,type=float,
        help="Mean insert length between paired reads. If not specified, will be inferred")
parser.add_argument("--insert_std",dest="insert_std",default=-1.,type=float,
        help="Standard deviation of insert length. If not specified, will be inferred")
parser.add_argument("--simple",dest="simple_svs",action="store_true",
        help="Whether sv input is in a simple format (see README), otherwise VCF format is assumed.")
parser.add_argument("--socrates",dest="socrates",action="store_true",
        help="Whether sv input is 'Socrates' SV caller input.")
parser.add_argument("--use_dir",dest="use_dir",action="store_true",
        help="Whether to use breakpoint direction in input file (must be supplied).")
parser.add_argument("--filter_repeats",dest="filt_repeats",default="",
        help="Comma-separated repeat types to filter, if found at both sides of the breakpoint). SOCRATES INPUT ONLY.")
parser.add_argument("--sv_class_field",dest="class_field",default="",
        help="Use existing classification field, specify the field name")

args = parser.parse_args()
if __name__ == '__main__':
    process.proc_svs(args)
