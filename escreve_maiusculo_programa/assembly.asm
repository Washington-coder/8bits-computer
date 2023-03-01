    data r0,0xc8
    data r2,0x00
    data r1,0x81
    data r3,0x01
    out addr,r1
inicio:
    in data,r1
    st r0,r1
    add r3,r0
    cmp r1,r2
    je guarda
    jmp inicio
guarda:
   data r1,0x20
   not r1,r1
   add r3,r1
   data r0,0xfa 
   st r0,r1
   data r0,0xc8
compara:
    ld r0,r1
    data r2,0x00
    cmp r1,r2
    je escrita
    clf
    data r2,0x60
    cmp r2,r1
    ja minusculo
    jmp maiusculas
maiusculas:
    data r2,0xfa
    ld r2,r2
    add r2,r1
minusculo:
    st r0,r1
    data r3,0x01
    clf
    add r3,r0
    jmp compara
escrita:
    data r0,0xc8
looping:
    data r1,0x80
    ld r0,r2
    out addr,r1
    out data,r2
    data r3,0x01
    clf
    add r3,r0
    data r3,0x00
    clf
    cmp r2,r3
    je fim
    jmp looping
fim:
    halt
