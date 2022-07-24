import sys

count = {}
out = {}
with open(sys.argv[1]) as fp:
	for line in fp.readlines():
		if line.startswith('#'): continue
		f = line.split()
		if len(f) < 7: continue
		c1 = f[0]
		c2 = f[1]
		pct = f[2]
		length = f[4]
		qb = f[6]
		qe = f[7]
		sb = int(f[8])
		se = int(f[9])
		
		if c2 == '3' and sb > 14200000 and sb < 14204000: continue
		if c2 == '2' and sb > 5000 and sb < 9999: continue
		if c2 == '2' and sb >= 11327936 and sb <= 11328527: continue
		
		# c. sativa modifications
		if c2 == '1' and sb >= 16057000 and sb <= 16059000: continue
		if c2 == '1' and sb >= 16196000 and sb <= 16198000: continue


		if c2 == '3' and sb >= 13956400 and sb <= 13959000: continue
		if c2 == '3' and sb >= 11685000 and sb <= 11687000: continue
		if c2 == '3' and sb >= 11338000 and sb <= 11341000: continue
		
		if c2 == '4' and sb >= 5081000 and sb <= 5083000: continue
		
		if c2 == '5' and sb >= 19891000 and sb <= 19893000: continue
		if c2 == '5' and sb >= 12423000 and sb <= 12426000: continue

		if int(length) < 50: continue
		if float(pct) < 87: continue
		
		if se < sb: sb, se = se, sb
		coor = (c2, sb, se)
		if coor not in count: count[coor] = 0
		count[coor] += 1
		out[coor] = line


for coor in count:
	if count[coor] == 1:
		print(out[coor], end='')
"""
import sys

count = {}
out = {}
with open(sys.argv[1]) as fp:
	for line in fp.readlines():
		if line.startswith('#'): continue
		f = line.split()
		if len(f) < 7: continue
		c1 = f[0]
		c2 = f[1]
		pct = f[2]
		length = f[4]
		qb = f[6]
		qe = f[7]
		sb = int(f[8])
		se = int(f[9])
		
		# brassica
		if c2 == '3' and sb > 14200000 and sb < 14204000: continue
		if c2 == '2' and sb > 5000 and sb < 9999: continue
		if c2 == '2' and sb > 11327900 and sb < 11328100: continue
		# very hardcoded masking
		if c2 == '2' and sb >= 3403490 and sb <=3404168: continue

		# oryza
		if c2 == '2' and sb > 3240000 and sb < 3420000: continue
		if c2 == '3' and sb > 13250000 and sb < 13280000: continue
		if c2 == '3' and sb > 14353000 and sb < 14356010: continue
		# populus
		if c2 == '3' and sb > 13530000 and sb < 13542000: continue
		
		if int(length) < 50: continue
		if float(pct) < 88: continue
		
		if se < sb: sb, se = se, sb
		coor = (c2, sb, se)
		if coor not in count: count[coor] = 0
		count[coor] += 1
		out[coor] = line


for coor in count:
	if count[coor] == 1:
		print(out[coor], end='')
"""