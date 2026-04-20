import os
import subprocess

def do_oneforall(target):
    try:
        print(f"[+] 正在运行 OneForAll 信息收集：{target}")
        oneforall_path = os.path.abspath("./OneForAll/oneforall.py")
        if not os.path.exists(oneforall_path):
            print(f"[-] OneForAll 路径不存在：{oneforall_path}")
            return
        oneforall_cmd = f"python {oneforall_path} --target {target} run"
        subprocess.run(oneforall_cmd, shell=True)
        print(f"[+] OneForAll 收集完成：{target}")
    except Exception as e:
        print(f"[-] OneForAll 失败：{e}")