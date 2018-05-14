from pwn import *
import os

head = open('../h', 'r')
tail = open('../t', 'r')
f1 = open('../fragment_1.dat', 'r')
f2 = open('../fragment_2.dat', 'r')
f3 = open('../fragment_3.dat', 'r')
f4 = open('../fragment_4.dat', 'r')
f5 = open('../fragment_5.dat', 'r')
f6 = open('../fragment_6.dat', 'r')
f7 = open('../fragment_7.dat', 'r')
f8 = open('../fragment_8.dat', 'r')

r1 = f1.read()
r2 = f2.read()
r3 = f3.read()
r4 = f4.read()
r5 = f5.read()
r6 = f6.read()
r7 = f7.read()
r8 = f8.read()
hd = head.read()
tl = tail.read()

rd = [r1, r2, r3, r4, r5, r6, r7, r8]
cnt = 0

for a in range(8):
	for b in range(8):
		for c in range(8):
			for d in range(8):
				for e in range(8):
					for f in range(8):
						for g in range(8):
							for h in range(8):
								if a != b and a != c and a != d and a != e and a != f and a != g and a != h and b != c and b != d and b != e and b != f and b != g and b != h and c != d and c != e and c != f and c != g and c != h and d != e and d != f and d != g and d != h and e != f and e != g and e != h and f != g and f != h and g != h:
									print a, b, c, d, e, f, g, h
									op = hd + rd[a]+rd[b]+rd[c]+rd[d]+rd[e]+rd[f]+rd[g]+rd[h] + tl
									filename = str(cnt) + 'th'
									elf = open(filename, 'w')
									elf.write(op)
									elf.close()
									cnt += 1
