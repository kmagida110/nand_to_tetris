@256
D=A
@SP
M=D
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@1
D=M+D
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
(LOOP_START)
@0
D=A
@2
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@1
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
M=M+D
@0
D=A
@1
D=M+D
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@0
D=A
@2
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
A=A-1
M=M-D
@0
D=A
@2
D=M+D
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@0
D=A
@2
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@LOOP_START
D;JNE
@0
D=A
@1
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1