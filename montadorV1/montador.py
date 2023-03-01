import sys

instructions = {'add':0b1000, 'shr':0b1001, 'shl':0b1010, 'not':0b1011, 'and':0b1100, 'or':0b1101, 'xor':0b1110,
 'cmp':0b1111, 'ld':0b0000, 'st':0b0001, 'data':0b0010, 'jmpr':0b0011, 'jmp':0b0100, 'jcond':0b0101, 'clf':0b0110,
 	'in':0b0111, 'out':0b0111}

hex_code = ['00' for i in range(256)]
labels = {}

register = {'r0':0b0000, 'r1':0b0001, 'r2':0b0010, 'r3':0b0011}

def in_out(line,addr,cont):
	operators = line[1].split(',')
	hex_code[addr] = str(hex(instructions[line[0]])).split('x')[1]
	bin_code = 0b0000

	
	if operators[0] == 'addr':
		bin_code += 0b0100
	elif operators[0] != 'data':
		exit("WRONG PARAMETER AT: " + str(cont + 1) )
	if line[0] == 'out':
		bin_code += 0b1000
	if register.get(operators[1],-1) != -1:
		bin_code += register.get(operators[1])
		hex_code[addr] += hex(bin_code).split('x')[1]
	else:
		exit("WRONG REGISTER AT: " + str(cont + 1) )
	return addr + 1

def complemento_2(decimal):
	if decimal.find('-') != -1:
		separados = decimal.split('-')
		num = int(separados[1])
		num2 = ~num ^ 0b11111111
		return hex(num2 * -1).split('x')[1].zfill(2)
	else:
		return hex(int(decimal)).split('x')[1].zfill(2)

def parse_input_file(asm_file):
	with open(asm_file, 'r') as f:
		line_index = 1
		for line in f.readlines():
			tester = line.lower() 
			if tester.find(":") != -1 and tester[0] == " ":
				exit("ERROR IN LABEL AT: "+str(line_index))
			line_index += 1
	with open(asm_file, 'r') as f:
		lines = [line.strip().lower().split() for line in f.readlines()]
	for i in range(0,len(lines)):
		if lines[i] == []:
			exit("ERROR BLANK LINE AT: "+ str(i+1) )
	return lines

def line_to_hex(line, addr, cont):
	operator_bits = []
	combine = 0b0000

	if line[0].find(":") != -1:
		
		labels.update({line[0].split(':')[0]:hex(addr)})
	elif line[0] == 'halt':
		hex_code[addr] = str(hex(instructions['jmp'])).split('x')[1]
		hex_code[addr] += str(hex(0b00)).split('x')[1]
		hex_code[addr+1] = hex(addr).split('x')[1].zfill(2)
		addr += 2

	elif line[0][0] == 'j':
		if line[0] == 'jmpr':
			hex_code[addr] = str(hex(instructions[line[0]])).split('x')[1]
			operator_bits = line[1]
			hex_code[addr] += str(hex(register[operator_bits])).split('x')[1]
		elif line[0] == 'jmp':
			hex_code[addr] = str(hex(instructions[line[0]])).split('x')[1]
			hex_code[addr] += str(hex(0b00)).split('x')[1]
			if line[1].find('0x') != -1:
				hex_code[addr+1] = line[1].split('x')[1]
			else:
				if labels.get(line[1],-1) != -1:
					if len(labels[line[1]]) == 3:
						label_addr = labels[line[1]].split('x')[1].zfill(2)
						hex_code[addr+1] = label_addr
					else:
						hex_code[addr+1] = labels[line[1]].split('x')[1]
				else: 
					hex_code[addr+1] = line[1]
		else:
			hex_code[addr] = str(hex(instructions['jcond'])).split('x')[1]
			second_part_ins = 0b0000
			if line[1].find('0x') != -1:
				hex_code[addr+1] = line[1].split('x')[1]
			else:
				if labels.get(line[1],-1) != -1:
					if len(labels[line[1]]) == 3:
						label_addr = labels[line[1]].split('x')[1].zfill(2)
						hex_code[addr+1] = label_addr
					else:
						hex_code[addr+1] = labels[line[1]].split('x')[1]
				else: 
					hex_code[addr+1] = line[1] 
			if line[0].find("c") != -1:
				second_part_ins += 0b1000
			if line[0].find("a") != -1:
				second_part_ins += 0b0100
			if line[0].find("e") != -1:
				second_part_ins += 0b0010
			if line[0].find("z") != -1:
				second_part_ins += 0b0001
			hex_code[addr] += str(hex(second_part_ins)).split('x')[1]
		addr += 2


	elif line[0] == "data":
		if (line[1].find(",")) == -1:
			exit('ERROR MISSING "," AT: '+ str(cont + 1) )
		hex_code[addr] = str(hex(instructions["data"])).split('x')[1]
		operator_bits = line[1].split(',')
		hex_code[addr] += str(hex(register[operator_bits[0]])).split('x')[1]
		if operator_bits[1].find('x') != -1:
			hex_code[addr+1] = str(operator_bits[1]).split('x')[1]
		else:
			hex_code[addr+1] = complemento_2(operator_bits[1])
		addr += 2	

	elif line[0] == "clf":
		hex_code[addr] = str(hex(instructions[line[0]])).split('x')[1]
		hex_code[addr] += str(hex(0b0000)).split('x')[1]
		addr += 1

	elif line[0] == "out" or line[0] == "in":
		addr = in_out(line,addr,cont)

	elif instructions.get(line[0],-1) != -1:
		hex_code[addr] = str(hex(instructions[line[0]])).split('x')[1]
		if (line[1].find(",")) != -1:
			operator_bits = line[1].split(',')
			first = 0b0000 + register[operator_bits[0]]
			second = 0b0000 + register[operator_bits[1]]
			combine = (first<<2) | (second)
			hex_code[addr] += str(hex(combine)).split('x')[1]
		else:
			exit('ERROR MISSING , AT:'+ str(cont + 1) )
		addr += 1

	elif instructions.get(line[0],-1) == -1:
		menssage = "INVALID SINTAX AT LINE " + str(cont + 1)
		exit(menssage)
	return addr

def to_hex(lines):
	cont = 0
	addr = 0
	while cont < len(lines):
		addr = line_to_hex(lines[cont],addr,cont)
		cont+=1

def fill_labels(hex_code):
	for i in range(0,len(hex_code)):
		if labels.get(hex_code[i],-1) != -1:
			hex_code[i] = labels.get(hex_code[i]).split('x')[1].zfill(2)
def write_outputfile(memory_file, hex_code):
	with open(memory_file, 'w') as f:
		f.write('v3.0 hex words plain\n')
		x = 0
		while x <= 255:
			if (x+1)%16 != 0:
				f.write(hex_code[x]+" ")
			else:
				f.write(hex_code[x])
			if ((x+1)%16 == 0) & (x != 255):
				f.write('\n')
			x += 1

def main(asm_file, memory_file):
	lines = parse_input_file(asm_file)
	to_hex(lines)
	fill_labels(hex_code)
	write_outputfile(memory_file,hex_code)

if __name__ == '__main__':

	assert len(sys.argv)==3, 'invalid number of input arguments'

	main(sys.argv[1], sys.argv[2])
	print("labels", labels)