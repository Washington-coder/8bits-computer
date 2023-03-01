import sys

# ALUNO: WASHINGTON ANTONIO MORENO RIEGA
# MATRICULA: 22152254

instrucoes = {
    'add': '1000', 'shr': '1010',
    'shl': '1001', 'not': '1011',
    'and': '1100', 'or': '1101',
    'xor': '1110', 'cmp': '1111',
    'ld': '0000', 'st': '0001',
    'data': '001000',
    'jmp': '01000000', 'jcaez': '01010111',
    'jae': '01010110','clf': '01100000',
    'halt': '01000000', 'in': '0111',
    'out': '0111'
}

registradores = {
    'r0': '00', 'r1': '01', 'r2': '10', 'r3': '11',
}

labels = {}

def separar_instrucao_de_parametro(linha):
    linha = linha.split()
    return linha

def preenche_endereco_labels(codigoAssembly):
    addr = 0
    for linha in codigoAssembly:
        linhaAssembly = separar_instrucao_de_parametro(linha)
        tipoDeInstrucao = linhaAssembly[0]

        if (tipoDeInstrucao.find(':') != -1):
            label = linhaAssembly[0].split(':')
            labels.update({label[0]:hex(addr)})
        elif (tipoDeInstrucao == 'jmp'):
            addr += 2
        elif (tipoDeInstrucao == 'jae'):
            addr += 2
        elif (tipoDeInstrucao == 'halt'):
            addr += 2
        elif (tipoDeInstrucao == 'data'):
            addr += 2
        elif (tipoDeInstrucao == 'st'):
            addr += 1
        elif (tipoDeInstrucao == 'add'):
            addr += 1
        elif (tipoDeInstrucao == 'shl'):
            addr += 1
        elif (tipoDeInstrucao == 'shr'):
            addr += 1
        elif (tipoDeInstrucao == 'not'):
            addr += 1
        elif (tipoDeInstrucao == 'and'):
            addr += 1
        elif (tipoDeInstrucao == 'or'):
            addr += 1
        elif (tipoDeInstrucao == 'xor'):
            addr += 1
        elif (tipoDeInstrucao == 'cmp'):
            addr += 1
        elif (tipoDeInstrucao == 'move'):
            addr += 2
        elif (tipoDeInstrucao == 'in'):
            addr += 1
        elif (tipoDeInstrucao == 'out'):
            addr += 1
        elif (tipoDeInstrucao == 'clf'):
            addr += 1
        elif (tipoDeInstrucao == 'ld'):
            addr += 1
        elif (tipoDeInstrucao == 'st'):
            addr += 1

def busca_endereco(endereco):
    byte = ''
    if (endereco.find('x') != -1):
        endereco = endereco.split('x')
        byte = endereco[1]
    else:
        if endereco in labels:
            byte = labels[endereco]
            byte = byte.split('x')
            byte = byte[1]
            if len(str(byte)) == 1:
                byte = '0' + str(byte)
        else:
            exit('Não existe esse label: ' + str(endereco))
    return byte

def insere_tipo_J(endereco, nomeDaInstrucao, indexCodigoHexa, codigoHexa):
    byte1 = split_hexa(hex(int(instrucoes[nomeDaInstrucao],2)))
    byte2 = busca_endereco(endereco)
    codigoHexa[indexCodigoHexa] = byte1
    indexCodigoHexa += 1
    codigoHexa[indexCodigoHexa] = byte2
    indexCodigoHexa += 1

def split_hexa(hexa):
    hexa = hexa.split('x')
    hexa = hexa[1]
    return hexa

def split_parametros(parametros):
    parametros = parametros.split(',')
    return parametros

def complemento_de_2(valor):
    separados = valor.split('-')
    num = int(separados[1])
    num2 = ~num ^ 0b11111111
    return hex(num2 * -1)

def insere_tipo_Data(parametros, nomeDaInstrucao, indexCodigoHexa, codigoHexa):
    byte1 = instrucoes[nomeDaInstrucao]
    registrador = parametros[0]
    valor = parametros[1]

    if valor.find('-') != -1:
        valor = complemento_de_2(valor)
    
    # Valida tanto o uso de registradores quanto o de enderecos
    if registrador in registradores:
        registrador = registradores[registrador]
    else:
        exit('Registrador não existe')
    
    # Valida uso de valores em hexa
    if valor in labels:
        valor = split_hexa(labels[valor])
    elif valor.find('x') != -1:
        valor = split_hexa(valor)
    else:
        valor = split_hexa(hex(int(valor)))

    if len(str(valor)) == 1:
        valor = '0' + str(valor)

    byte1 = str(byte1) + str(registrador)
    byte1 = split_hexa(hex(int(byte1,2)))
    byte2 = valor

    codigoHexa[indexCodigoHexa] = byte1
    indexCodigoHexa += 1
    codigoHexa[indexCodigoHexa] = byte2
    indexCodigoHexa += 1

def split_binary(binary):
    binary = binary.split('b')
    binary = binary[1]
    return binary

def passa_registradores_binario(parametros):
    registrador1 = registradores[parametros[0]]
    registrador2 = registradores[parametros[1]]

    registradoresBin = str(registrador1) + str(registrador2)
    return registradoresBin

def insere_tipo_St(parametros, nomeDaInstrucao, indexCodigoHexa, codigoHexa):
    
    registradoresBin= passa_registradores_binario(parametros)

    byte = instrucoes[nomeDaInstrucao] + registradoresBin
    byte = split_hexa(hex(int(byte, 2)))
    codigoHexa[indexCodigoHexa] = byte
    
def insere_tipo_aritimetico_ou_logico(parametros, nomeDaInstrucao, indexCodigoHexa, codigoHexa):
    
    registradoresBin = passa_registradores_binario(parametros)

    byte = instrucoes[nomeDaInstrucao] + registradoresBin
    byte = split_hexa(hex(int(byte, 2)))
    codigoHexa[indexCodigoHexa] = byte
    
def escrever_no_arquivo(memory_file, codigoHexa):
    with open(memory_file, 'w') as f:
        f.write('v3.0 hex words plain\n')
        x = 0
        while x <= 255:
            if (x+1)%16 != 0:
                f.write(codigoHexa[x]+" ")
            else:
                f.write(codigoHexa[x])
            if ((x+1)%16 == 0) & (x != 255):
                f.write('\n')
            x += 1

def insere_tipo_move(parametros, indexCodigoHexa, codigoHexa):
    registrador1 = parametros[0]
    registrador2 = parametros[1]

    parametrosXor = []

    parametrosXor.append(registrador2)
    parametrosXor.append(registrador2)

    insere_tipo_aritimetico_ou_logico(parametrosXor, 'xor', indexCodigoHexa, codigoHexa)
    indexCodigoHexa += 1

    parametrosAdd = []

    parametrosAdd.append(registrador1)
    parametrosAdd.append(registrador2)

    insere_tipo_aritimetico_ou_logico(parametrosAdd, 'add', indexCodigoHexa, codigoHexa)
    indexCodigoHexa += 1

def insere_tipo_in_out(parametros, nomeDaInstrucao, indexCodigoHexa, codigoHexa):
    tipo = parametros[0]
    registrador = parametros[1]

    binario = instrucoes[nomeDaInstrucao]
    if (nomeDaInstrucao == 'in'):
        binario = str(binario) + '0'
    elif(nomeDaInstrucao == 'out'):
        binario = str(binario) + '1'

    if (tipo == 'addr'):
        binario = str(binario) + '1'
    elif (tipo == 'data'):
        binario = str(binario) + '0'

    registradorBinario = registradores[registrador]

    binario = binario + registradorBinario
    byte = split_hexa(hex(int(binario, 2)))

    codigoHexa[indexCodigoHexa] = byte
    indexCodigoHexa += 1    


# main
def passa_arquivo_para_hexa(memory_file):

    codigoHexa = ['00' for i in range(256)]
    indexCodigoHexa = 0
    
    with open(memory_file, "r") as arquivo:
        codigoAssembly = arquivo.readlines()
        preenche_endereco_labels(codigoAssembly)
        for linha in codigoAssembly:
            linhaAssembly = separar_instrucao_de_parametro(linha)
            nomeDaInstrucao = linhaAssembly[0]
            if (nomeDaInstrucao == 'jmp'):
                endereco = linhaAssembly[1]
                insere_tipo_J(endereco, nomeDaInstrucao, indexCodigoHexa, codigoHexa)
                indexCodigoHexa += 2    
            elif (nomeDaInstrucao == 'jae'):
                endereco = linhaAssembly[1]
                insere_tipo_J(endereco, nomeDaInstrucao, indexCodigoHexa, codigoHexa)
                indexCodigoHexa += 2    
            elif (nomeDaInstrucao == 'data'):
                parametros = split_parametros(linhaAssembly[1])
                insere_tipo_Data(parametros, nomeDaInstrucao, indexCodigoHexa, codigoHexa)
                indexCodigoHexa += 2 
            elif (nomeDaInstrucao == 'halt'):
                codigoHexa[indexCodigoHexa] = split_hexa(hex(int(instrucoes[nomeDaInstrucao],2)))
                indexCodigoHexa += 1
                codigoHexa[indexCodigoHexa] = split_hexa(hex(indexCodigoHexa - 1))
                indexCodigoHexa += 1    
            elif (nomeDaInstrucao == 'st'):
                parametros = split_parametros(linhaAssembly[1])
                insere_tipo_St(parametros, nomeDaInstrucao, indexCodigoHexa, codigoHexa)
                indexCodigoHexa += 1    
            elif (nomeDaInstrucao == 'add'):
                parametros = split_parametros(linhaAssembly[1])
                insere_tipo_aritimetico_ou_logico(parametros, nomeDaInstrucao, indexCodigoHexa, codigoHexa)
                indexCodigoHexa += 1
            elif (nomeDaInstrucao == 'not'):
                parametros = split_parametros(linhaAssembly[1])
                insere_tipo_aritimetico_ou_logico(parametros, nomeDaInstrucao, indexCodigoHexa, codigoHexa)
                indexCodigoHexa += 1
            elif (nomeDaInstrucao == 'shl'):
                parametros = split_parametros(linhaAssembly[1])
                insere_tipo_aritimetico_ou_logico(parametros, nomeDaInstrucao, indexCodigoHexa, codigoHexa)
                indexCodigoHexa += 1
            elif (nomeDaInstrucao == 'shr'):
                parametros = split_parametros(linhaAssembly[1])
                insere_tipo_aritimetico_ou_logico(parametros, nomeDaInstrucao, indexCodigoHexa, codigoHexa)
                indexCodigoHexa += 1
            elif (nomeDaInstrucao == 'and'):
                parametros = split_parametros(linhaAssembly[1])
                insere_tipo_aritimetico_ou_logico(parametros, nomeDaInstrucao, indexCodigoHexa, codigoHexa)
                indexCodigoHexa += 1
            elif (nomeDaInstrucao == 'or'):
                parametros = split_parametros(linhaAssembly[1])
                insere_tipo_aritimetico_ou_logico(parametros, nomeDaInstrucao, indexCodigoHexa, codigoHexa)
                indexCodigoHexa += 1
            elif (nomeDaInstrucao == 'xor'):
                parametros = split_parametros(linhaAssembly[1])
                insere_tipo_aritimetico_ou_logico(parametros, nomeDaInstrucao, indexCodigoHexa, codigoHexa)
                indexCodigoHexa += 1
            elif (nomeDaInstrucao == 'cmp'):
                parametros = split_parametros(linhaAssembly[1])
                insere_tipo_aritimetico_ou_logico(parametros, nomeDaInstrucao, indexCodigoHexa, codigoHexa)
                indexCodigoHexa += 1
            elif (nomeDaInstrucao == 'move'):
                parametros = split_parametros(linhaAssembly[1])
                insere_tipo_move(parametros, indexCodigoHexa, codigoHexa)
                indexCodigoHexa += 2
            elif (nomeDaInstrucao == 'clf'):
                hexa = split_hexa(hex(int(instrucoes[nomeDaInstrucao],2)))
                codigoHexa[indexCodigoHexa] = hexa
                indexCodigoHexa += 1
            elif (nomeDaInstrucao == 'in' or nomeDaInstrucao == 'out'):
                parametros = split_parametros(linhaAssembly[1])
                insere_tipo_in_out(parametros, nomeDaInstrucao, indexCodigoHexa, codigoHexa)
                indexCodigoHexa += 1
            elif (nomeDaInstrucao == '.word'):
                parametro = linhaAssembly[1]
                if parametro.find('x') != -1:
                    parametro = split_hexa(linhaAssembly[1])
                elif parametro.find('-') != -1:
                    parametro = split_hexa(complemento_de_2(parametro))
                else:
                    parametro = split_hexa(hex(int(parametro)))

                if len(str(parametro)) == 1:
                    parametro = '0' + parametro
                
                codigoHexa[indexCodigoHexa] = parametro
                indexCodigoHexa += 1

    return codigoHexa

def main(asm_file, memory_file):
    codigoHexa = passa_arquivo_para_hexa(asm_file)
    escrever_no_arquivo(memory_file, codigoHexa)

if __name__ == '__main__':
    
	assert len(sys.argv)==3, 'invalid number of input arguments'

	main(sys.argv[1], sys.argv[2])