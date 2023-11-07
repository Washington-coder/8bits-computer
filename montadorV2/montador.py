# ALUNO: WASHINGTON ANTONIO MORENO RIEGA
# MATRICULA: 22152254

import sys

byteCodeIndex = 0
lineNumber = 1

registers = {
    'r0': '00', 'r1': '01', 'r2': '10', 'r3': '11'
}

instructions = {
    "in": "0111",
    "out": "0111",
    "add": "1000",
    "shr": "1001",
    "shl": "1010",
    "not": "1011",
    "and": "1100",
    "or": "1101",
    "xor": "1110",
    "cmp": "1111",
    "ld": "0000",
    "st": "0001",
    "data": "001000",
    "jmpr": "001100",
    "jmp": "01000000",
    "jcaez": "0101",
    "clf": "01100000",
    "halt": "",
    "move": ""
}


def get_program_size(asmCode):
    programSize = 0
    for line in asmCode:
        line = line.strip()
        if not line.startswith('.') and len(line) > 0:
            if (line.find(';') != -1):
                line = line.split(';')[0]
            if (len(line) > 0):
                instruction, params = separate_params_from_instructions(
                    line)
                instruction = instruction.lower()
                if (
                    instruction == "add" or
                    instruction == "shr" or
                    instruction == "shl" or
                    instruction == "not" or
                    instruction == "and" or
                    instruction == "or" or
                    instruction == "xor" or
                    instruction == "cmp" or
                    instruction == "ld" or
                    instruction == "st" or
                    instruction == "jmpr" or
                    instruction == "clf" or
                    instruction == "in" or
                    instruction == "out"
                ):
                    programSize += 1
                elif (
                    instruction == "jmp" or
                    instruction == "halt" or
                    instruction == "data" or
                    instruction[0] == "j"
                ):
                    programSize += 2
                elif (
                    instruction == "move"
                ):
                    programSize += 3
    return programSize
                    
def separate_params_from_instructions(line):
    line = line.split()
    if (len(line) > 1):
        if len(line) == 3:
            line[1] = line[1] + line[2]
        return line[0], line[1]
    return line[0], ''


def binary_to_hex(binaryCode):
    hexCode = hex(int(binaryCode, 2)).split('x')
    hexCode = hexCode[1]
    return hexCode


def has_register(register):
    if register in registers:
        return True
    else:
        exit("Unknown register at line: " + str(lineNumber))


def has_instruction(instruction):
    if instruction in instructions:
        return True
    elif (instruction[0] == 'j'):
        return True
    else:
        exit("Unknown instruction at line: " + str(lineNumber))


def get_valid_hex_value(value):
    if (value.find('x') != -1):
        value = value.split('x')[1]
        if len(value) == 0 or len(value) > 2:
            exit("Invalid hex value at line: " + str(lineNumber))
        if (len(value) == 1):
            return '0' + value
        return value
    elif (len(value) == 0 or len(value) > 2):
        exit("Invalid hex value at line: " + str(lineNumber))
    else:
        if (len(value) == 1):
            return '0' + value
        return value


def get_data_type_hex_code(byteCode, params):
    global byteCodeIndex
    params = params.split(",")

    if has_register(params[0]):
        register = params[0]
        value = params[1]
        binaryCode = instructions["data"] + registers[register]
        hexCode = binary_to_hex(binaryCode)
        byteCode[byteCodeIndex] = hexCode
        byteCodeIndex += 1
        byteCode[byteCodeIndex] = get_valid_hex_value(value)
        byteCodeIndex += 1


def get_two_registers_instruction(byteCode, params, instruction):
    global byteCodeIndex
    register1 = params[0]
    register2 = params[1]

    if (has_register(register1) and has_register(register2)):
        binaryCode = instructions[instruction] + \
            registers[register1] + registers[register2]
        hexCode = binary_to_hex(binaryCode)

        if (len(hexCode) == 1):
            hexCode = '0' + hexCode

        byteCode[byteCodeIndex] = hexCode
        byteCodeIndex += 1


def get_jmp_type_hex_code(byteCode, params, instruction):
    global byteCodeIndex

    binaryCode = instructions[instruction]
    hexCode = binary_to_hex(binaryCode)
    byteCode[byteCodeIndex] = hexCode
    byteCodeIndex += 1
    byteCode[byteCodeIndex] = get_valid_hex_value(params)
    byteCodeIndex += 1


def get_hex_code(byteCode, instruction, params):
    global byteCodeIndex
    instruction = instruction.lower()
    params = params.lower()

    if (has_instruction(instruction)):
        if (instruction == "data"):
            get_data_type_hex_code(byteCode, params)
        elif (
                instruction == "add" or
                instruction == "shr" or
                instruction == "shl" or
                instruction == "not" or
                instruction == "and" or
                instruction == "or" or
                instruction == "xor" or
                instruction == "cmp" or
                instruction == "ld" or
                instruction == "st"
        ):
            params = params.split(",")
            get_two_registers_instruction(byteCode, params, instruction)
        elif (instruction == "clf"):
            hexCode = binary_to_hex(instructions[instruction])
            byteCode[byteCodeIndex] = hexCode
            byteCodeIndex += 1
        elif (instruction == "halt"):
            addr = str(hex(byteCodeIndex))
            get_jmp_type_hex_code(byteCode, addr, "jmp")
        elif (instruction == "move"):
            params = params.split(",")
            register1 = params[0]
            register2 = params[1]
            params[0] = register2
            params[1] = register2
            get_two_registers_instruction(byteCode, params, "xor")
            params[0] = register1
            params[1] = register2
            get_two_registers_instruction(byteCode, params, "add")
            params[0] = register1
            params[1] = register1
            get_two_registers_instruction(byteCode, params, "xor")
        elif (instruction[0] == 'j'):
            if (instruction == "jmpr"):
                register = params
                if (has_register(register)):
                    binaryCode = instructions[instruction] + \
                        registers[register]
                    hexCode = binary_to_hex(binaryCode)
                    byteCode[byteCodeIndex] = hexCode
                    byteCodeIndex += 1
            elif (instruction == "jmp"):
                get_jmp_type_hex_code(byteCode, params, instruction)
            else:
                if (len(instruction) > 5 or len(instruction) <= 1):
                    exit("Unknown instruction at line: " + str(lineNumber))

                binaryCode = instructions['jcaez']
                caezParam = ['0', '0', '0', '0']

                for item in range(1, len(instruction)):
                    if (instruction[item] == 'c'):
                        caezParam[0] = '1'
                    elif (instruction[item] == 'a'):
                        caezParam[1] = '1'
                    elif (instruction[item] == 'e'):
                        caezParam[2] = '1'
                    elif (instruction[item] == 'z'):
                        caezParam[3] = '1'
                    else:
                        exit("Unknown instruction at line: " + str(lineNumber))

                caezParam = "".join(caezParam)
                binaryCode += caezParam
                hexCode = binary_to_hex(binaryCode)
                byteCode[byteCodeIndex] = hexCode
                byteCodeIndex += 1
                byteCode[byteCodeIndex] = get_valid_hex_value(params)
                byteCodeIndex += 1


def get_byte_code(asm_file):
    byteCode = ['00' for i in range(256)]
    global lineNumber

    with open(asm_file, 'r') as file:
        asmCode = file.readlines()
        programSize = get_program_size(asmCode)
        for line in asmCode:
            line = line.strip()
            if line.startswith('.word') and len(line) > 0:
                if (line.find(';') != -1):
                    line = line.split(';')[0]
                if (len(line) > 0):
                    instruction, params = separate_params_from_instructions(
                        line)
                    byteCode[programSize] = get_valid_hex_value(params)           
                    programSize += 1

        for line in asmCode:
            line = line.strip()
            if not line.startswith('.') and len(line) > 0:
                if (line.find(';') != -1):
                    line = line.split(';')[0]
                if (len(line) > 0):
                    instruction, params = separate_params_from_instructions(
                        line)
                    get_hex_code(byteCode, instruction, params)
                    lineNumber += 1

    return byteCode


def write_in_memory_file(memory_file, byteCode):
    with open(memory_file, 'w') as f:
        f.write('v3.0 hex words plain\n')
        i = 0
        while i <= 255:
            if (i+1) % 16 != 0:
                f.write(byteCode[i]+" ")
            else:
                f.write(byteCode[i])
            if ((i+1) % 16 == 0) & (i != 255):
                f.write('\n')
            i += 1


def main(asm_file, memory_file):
    byteCode = get_byte_code(asm_file)
    write_in_memory_file(memory_file, byteCode)


if __name__ == '__main__':

    assert len(sys.argv) == 3, 'invalid number of input arguments'

    main(sys.argv[1], sys.argv[2])
