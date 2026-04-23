import os
import subprocess

def do_scan():
    url_file = "url.txt"
    if not os.path.exists(url_file) or os.path.getsize(url_file) == 0:
        print(f"[-] {url_file} 不存在或为空，跳过Xray扫描")
        return

    # ========== 你要的 XRAY 文件名：xray_windows_amd64.exe ==========
    xray_dir = os.path.abspath(r"xray_1.9.3")
    xray_exe = os.path.join(xray_dir, "xray.exe")  # 这里改了

    # 输出报告到当前目录：10.html
    output_file = os.path.abspath("10.html")

    if not os.path.exists(xray_exe):
        print(f"[-] Xray不存在：{xray_exe}")
        return

    try:
        # ===================== 你要的核心命令 =====================
        scan_cmd = [
            xray_exe,
            "webscan",
            "--url-file", url_file,      # 直接读取 url.txt 批量扫描
            "--html-output", output_file  # 输出 10.html
        ]

        print(f"\n[+] 开始Xray批量扫描，读取：{url_file}")
        print(f"[+] 报告将保存为：{output_file}")

        # 执行命令（切换xray目录，保证配置文件正常）
        process = subprocess.Popen(
            scan_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            cwd=xray_dir
        )

        # 实时输出扫描日志
        for line in iter(process.stdout.readline, ''):
            print(line, end='')

        process.stdout.close()
        process.wait()

        if process.returncode == 0:
            print(f"\n[+] 扫描完成！报告：{output_file}")
        else:
            print(f"\n[-] 扫描异常")

    except Exception as e:
        print(f"[-] 扫描失败：{e}")