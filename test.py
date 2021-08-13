import os
from sys import stdin
Isa= open("isa.txt",'r') # opening text file containing assembly code
binary= open("binary.txt",'a+')# writing output into this file
'''
instructions is a dict storing op codes and binary codes
types is storing op code and instruction type
registers is mapping register name to address
used_instr keeps track of which opcodes were used or attempted to use
variables stores any var declarations
error msg is a string that prints out the error
'''
instructions = {"hlt":"10011","je":'10010',"jgt":'10001',"jlt":'10000',"jmp":'01111',"cmp":'01110',"not":'01101'}
types = {"hlt":"F","je":'E',"jgt":'E',"jlt":'E',"jmp":'E',"cmp":'C',"not":'C'}
registers={'R0':"000",'R1':"001",'R2':"010",'R3':"011",'R4':"100",'R5':"101",'R6':"110",'flags':"111"}
used_instr=[]
variables=[]
error_msg=""
# most print commands here are debug statements
for line in stdin:
   
    words= line.split()
    print(words)
    print(len(used_instr))

    if(words[0] in instructions):#if the 1st element in input belongs to the set of keys of instructions ie the valid opcodes
        used_instr=words[0]# add to used instr
        opcode = instructions.get(words[0])#get binary value of instruction
        instr_type = types.get(words[0])#get the type
        print(opcode,instr_type)#debug statement
        if instr_type=='C':
            if(len(words)==3):# the expected length for this instruction type
                reg1 = registers.get(words[1])# the ssecond statement should have reg1
                reg2 =registers.get(words[2])
                print(reg1)
                print(reg2)
                if ((len(reg1) and len(reg2))==3):# checking whether registern naming was correct or not, for some reason the len is 3 not 2 
                    binary_code= opcode+('0'*5)+reg1+reg2+"\n"
                    binary.write(binary_code)
                else:
                    error_msg+="Invalid Register naming"
                    break
            else:
                error_msg+="Invalid Syntax for "+words[0]+"\n"
                break
        # similar to the above one the following 2 types follow the same pattern
        elif instr_type=='E':
            if(len(words)==2):  
                mem_address = words[1]# storing the memory address
                if(len(mem_address)==8):
                    binary_code=opcode+("0"*3)+mem_address+"\n"
                    binary.write(binary_code)
                else:
                    error_msg+="Syntax Error\n"
                    break
            else:
                error_msg+="Invalid Syntax for "+words[0]+"\n"
                break
        elif instr_type=="F":
            if(len(words)==1):
                binary_code= opcode+("0"*11)+"\n"
                binary.write(binary_code)
            else:
                error_msg+="Invalid Syntax for "+words[0]+"\n"
                break
        if opcode==None:
            error_msg+="invalid instruction name\n"
            break
# now if the above code doesn't run then its either a variable declaration or typo in instruction name
    elif (words[0]=='var' and len(used_instr)==0):# len(used_instr) ensures that no other instr was used before a var declaration
        if (words[0].isalnum() ):
            if('_' in words[0]):
                variables.append(words[1])
        else:
            error_msg+="Improper variable naming"
            break
    elif(words[0]=='var' and len(used_instr)>0):
        error_msg+="variables not declared at the top"
        break
    elif(words[0] not in instructions):
        error_msg+="Typo in instruction name"
        break
# hlt error check is done at the end, assuming there are no error msg's prior to this halt errors are the only one left    
if(error_msg==""):   
    if("hlt" not in used_instr):# if halt was never called
        error_msg+="hlt instruction is not used\n"
    elif ("hlt" in used_instr): # halt was called but was not the last one to be called
        if (used_instr.index("hlt")!= len(used_instr)-1):
                error_msg+= "hlt instruction is not the last instruction\n"
binary.write(error_msg)
#     cmp R4 R6
# jmp 10001000
# hlt
