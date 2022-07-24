#!/usr/bin/env python3
# feature_mask.py

import re
import argparse
import sys

def feature_mask(fasta, gff, feat1, feat2, feat3, mask, per_line):
	gff_pat = '(\w+)\s+\w+\s+\w+\s+(\d+)\s+(\d+)'
	gff_fp = open(gff)
	del_feats = []
	for line in gff_fp.readlines():
		if re.search(feat1, line) or re.search(feat2, line) or re.search(feat3, line):
			match = re.search(gff_pat, line)
			del_feats.append({'chrom':match.group(1), 'beg':int(match.group(2)), 'end':int(match.group(3))})
	
	del_feats = sorted(del_feats, key=lambda x: x['chrom'])
	
	fa_fp = open(fasta)
	id_pat = 'TAIR10:(\w+):(\w+):(\w+)'
	fa_chrom = None
	fa_beg = None
	fa_end = None
	seq = ""
	first_time = True
	
	for line in fa_fp.readlines():
		match1 = re.search(id_pat, line)
		if match1:
			if not first_time:
				for f in del_feats:
					if f['chrom'] > fa_chrom: break    # assumes fasta is sorted by chrom
					if f['chrom'] == fa_chrom:
						if f['beg'] >= fa_beg and f['end'] <= fa_end:
							seq = mask_seq(seq, f['beg'] - fa_beg, f['end'] - fa_beg, mask)
						elif f['beg'] >= fa_beg and f['beg'] <= fa_end:
							seq = mask_seq(seq, f['beg'] - fa_beg, fa_end - fa_beg, mask)
						elif f['end'] <= fa_end and f['end'] >= fa_beg:
							seq = mask_seq(seq, 0, f['end'] - fa_beg, mask)
				sys.stdout.write('>' + fa_chrom + ' ' + str(fa_beg) + '..' + str(fa_end) + '\n')
				while len(seq) >= per_line:
					sys.stdout.write(seq[:per_line] + '\n')
					seq = seq[per_line:]
				if len(seq) > 0:
					sys.stdout.write(seq)
				sys.stdout.write('\n')
				seq = ''		
				
			fa_chrom = match1.group(1)
			fa_beg = int(match1.group(2))
			fa_end = int(match1.group(3))
			first_time = False
		else:
			seq += line.rstrip()

	if len(seq) > 0:
		for f in del_feats:
			if f['chrom'] > fa_chrom: break
			if f['chrom'] == fa_chrom:
				if f['beg'] >= fa_beg and f['end'] <= fa_end:
					seq = mask_seq(seq, f['beg'] - fa_beg, f['end'] - fa_beg, mask)
				elif f['beg'] >= fa_beg and f['beg'] <= fa_end:
					seq = mask_seq(seq, f['beg'] - fa_beg, fa_end - fa_beg, mask)
				elif f['end'] <= fa_end and f['end'] >= fa_beg:
					seq = mask_seq(seq, 0, f['end'] - fa_beg, mask)
		sys.stdout.write('>' + fa_chrom + ' ' + str(fa_beg) + '..' + str(fa_end) + '\n')
		while len(seq) >= per_line:
			sys.stdout.write(seq[:per_line] + '\n')
			seq = seq[per_line:]
		if len(seq) > 0:
			sys.stdout.write(seq)
			sys.stdout.write('\n')
			seq = ''

def mask_seq(seq, beg, end, m_type):
	if m_type == 'soft':
		masked = seq[:beg] + seq[beg:end + 1].lower() + seq[end + 1:]
	else:
		masked = seq[:beg] + ("N" * (end - beg + 1)) + seq[end + 1:]
	return masked
	
parser = argparse.ArgumentParser(description='Feature mask FASTA files for UCE project')
parser.add_argument('--fasta', required=True, type=str,
	metavar='<str>', help='required str argument')
parser.add_argument('--gff', required=True, type=str,
	metavar='<str>', help='required str argument')
parser.add_argument('--feat1', required=True, type=str,
	metavar='<str>', help='required str argument')
parser.add_argument('--feat2', required=True, type=str,
	metavar='<str>', help='required str argument')
parser.add_argument('--feat3', required=True, type=str,
	metavar='<str>', help='required str argument')
parser.add_argument('--mask_type', required=True, type=str,
	metavar='<str>', help='required str argument')
parser.add_argument('--bp_per_line', required=True, type=int,
	metavar='<int>', help='required int argument')
arg = parser.parse_args()

feature_mask(arg.fasta, arg.gff, arg.feat1, arg.feat2, arg.feat3, arg.mask_type, arg.bp_per_line)