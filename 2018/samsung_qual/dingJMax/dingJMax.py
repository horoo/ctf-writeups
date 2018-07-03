#-*- coding: utf-8 -*-
import sys

f = open('dingJMax_note.txt', 'r')
lines = f.readlines()
f.close()

note_list = ''
num = []
v15 = 0
index = 20 * ((0x0CCCCCCCCCCCCCCCD * v15 >> 64) >> 4)

for line in lines:
	while v15 != 20 * ((0x0CCCCCCCCCCCCCCCD * v15 >> 64) >> 4):
		v15 += 1
	
	note = line.split('"')[1]
	if 'o' in note:
		num.append(v15+380)
		idx = note.find('o')
		if idx == 0:
			# sys.stdout.write('d')
			note_list += 'd'
		elif idx == 1:
			# sys.stdout.write('f')
			note_list += 'f'
		elif idx == 2:
			# sys.stdout.write('j')
			note_list += 'j'
		elif idx == 3:
			# sys.stdout.write('k')
			note_list += 'k'
	v15 += 1

print 'total len', len(num), num

src = "qN7BuRx4rElDv84dgNaaNBanZf0HSHFjqOvbkFfgTRg3r"
s = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_!"
byte_607588 = 0
byte_607568 = 0
byte_6075a0 = [i for i in range(len(s))]
dword_60756c = len(s)

def sub_401c9a(num):
	v3 = 0
	global byte_607588
	global dword_60756c
	global byte_6075a0
	global byte_607568

	for i in range(num):
		byte_607588 = (byte_607588 + 1) % dword_60756c
		byte_607568 = (byte_607568 + byte_6075a0[byte_607588]) % dword_60756c
		v1 = byte_6075a0[byte_607588]
		byte_6075a0[byte_607588] = byte_6075a0[byte_607568]
		byte_6075a0[byte_607568] = v1
		v3 = byte_6075a0[(byte_6075a0[byte_607588] + byte_6075a0[byte_607568])%dword_60756c]

	return s[v3]

def sub_401c50(a1):
	for i in range(dword_60756c):
		if a1 == s[i]:
			return i
	return -1

def sub_401db8(a1, a2):
	v2 = sub_401c50(a1)
	return s[(sub_401c50(a2) ^ v2) % dword_60756c]

def sub_400c5e():
	global src
	v4 = len(src)

	for i in range(v4):
		v1 = sub_401c9a(1)
		src = src[:i] + sub_401db8(src[i], v1) + src[i+1:]

v16 = 0

for ch in note_list:
	sub_401c9a(ord(ch) * num[v16])
	sub_400c5e()
	v16 += 1
	sys.stdout.write("\r{}/299 {}".format(v16, src))

print ''
print "result", src