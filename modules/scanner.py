import os
import subprocess
import hashlib

def do_scan():
    url_file = "url.txt"
    xray_dir = os.path.abspath(r"xray-1.9.11")
    xray_exe = os.path.join(xray_dir, "xray.exe")

    # ===================== 输出目录：main.py 同级 xray_results
    result_dir = os.path.abspath("xray_results")
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    # 检查文件
    if not os.path.exists(url_file):
        print("[-] url.txt 不存在")
        return
    if not os.path.exists(xray_exe):
        print("[-] xray.exe 不存在")
        return

    # 读取域名
    with open(url_file, "r", encoding="utf-8") as f:
        domains = [line.strip() for line in f if line.strip()]

    if not domains:
        print("[-] 无存活域名")
        return

    print(f"[+] 共 {len(domains)} 个域名，开始扫描…\n")

    for url in domains:
        # MD5 文件名
        md5_name = hashlib.md5(url.encode("utf-8")).hexdigest()
        # 最终路径：xray_results/xxx.html
        output_file = os.path.join(result_dir, f"{md5_name}.html")

        print(f"▶ 扫描：{url}")
        print(f"▶ 报告：{output_file}\n")

        # 执行 Xray
        cmd = [
            xray_exe,
            "webscan",
            "--browser-crawler",
            url,
            "--html-output",
            output_file
        ]

        # 稳定不崩溃
        subprocess.Popen(
            cmd,
            cwd=xray_dir,
            stdout=None,
            stderr=None,
            stdin=None
        ).wait()

        print(f"✅ 完成：{url}\n")

if __name__ == "__main__":
    do_scan()