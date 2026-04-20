import os
import hashlib
import subprocess

def do_scan():
    url_file = "url.txt"
    if not os.path.exists(url_file) or os.path.getsize(url_file) == 0:
        print(f"[-] {url_file} 不存在或为空，跳过Xray扫描")
        return

    with open(url_file, 'r', encoding='utf-8') as f:
        survival_urls = [line.strip() for line in f.readlines() if line.strip()]
    if not survival_urls:
        print("[-] 无有效存活URL，跳过Xray扫描")
        return

    # ========== 核心：XRAY 目录，自动切换 ==========
    xray_dir = os.path.abspath(r"xray_1.9.3")
    xray_exe = os.path.join(xray_dir, "xray.exe")

    # 输出到当前脚本目录，不是xray目录
    output_dir = os.path.abspath("./xray_results")
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(xray_exe):
        print(f"[-] Xray不存在：{xray_exe}")
        return

    for idx, target_url in enumerate(survival_urls, 1):
        try:
            file_md5 = hashlib.md5(target_url.encode()).hexdigest()
            html_output = os.path.join(output_dir, f"{file_md5}_{idx}.html")

            # === 核心命令 ==
            scan_cmd = [
                xray_exe,
                "webscan",
                "--basic-crawler", target_url,
                "--html-output", html_output
            ]

            print(f"\n[+] 开始Xray扫描 {idx}/{len(survival_urls)}：{target_url}")

            # ========== 最关键：切换工作目录到 xray.exe 所在文件夹 ==========
            process = subprocess.Popen(
                scan_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                cwd=xray_dir  # 切换目录！解决找不到配置文件问题
            )

            # 实时输出（和命令行完全一样）
            for line in iter(process.stdout.readline, ''):
                print(line, end='')

            process.stdout.close()
            process.wait()

            if process.returncode == 0:
                print(f"\n[+] 扫描完成：{html_output}")
            else:
                print(f"\n[-] 扫描异常")

        except Exception as e:
            print(f"[-] 扫描失败：{e}")

    print(f"\n[+] 全部 URL 扫描完成！报告在 xray_results 文件夹")