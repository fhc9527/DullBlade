import os
import re
import hashlib
import glob
import threading
import requests
import time
import subprocess
import sys

# ===================== 存活探测核心配置（从 cunhuo.py 迁移） =====================
requests.packages.urllib3.disable_warnings()
requests.adapters.DEFAULT_RETRIES = 5
STATUS_CODES = [200, 403]
TIMEOUT = 1
URLS_PER_THREAD = 20
res = []

def check(url):
    try:
        # 设置请求头，模拟浏览器访问
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'}
        # 发送GET请求，禁用SSL证书验证，设置超时时间
        res = requests.get(url=url, headers=headers, timeout=TIMEOUT, verify=False)
        # 检查响应状态码是否在预定义的状态码列表中
        if res.status_code in STATUS_CODES:
            return res.status_code
    except Exception as e:
        # 捕获并打印异常信息
        print(f"[-] 探测URL失败 {url}：{e.args}")
    # 默认返回0，表示探测失败或未找到匹配的状态码
    return 0

def list_split(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)]

def checks(urls):
    global res
    for url in urls:
        url = url.strip()
        if not url:
            continue
        http_url = f"http://{url}"
        https_url = f"https://{url}"
        http_status = check(http_url)
        https_status = check(https_url)
        if http_status > 0:
            res.append(f"{http_url}\n")
        if https_status > 0:
            res.append(f"{https_url}\n")

def multi_check(urls):
    global res
    res = []
    for url_chunk in list_split(urls, URLS_PER_THREAD):
        t = threading.Thread(target=checks, args=(url_chunk,))
        t.start()
    while len(threading.enumerate()) > 1:
        time.sleep(1)

def run_survival_detection():
    urls_file = "urls.txt"
    output_file = "url.txt"
    if not os.path.exists(urls_file) or os.path.getsize(urls_file) == 0:
        print(f"[-] {urls_file} 不存在或为空，跳过存活探测")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("")
        return False
    with open(urls_file, 'r', encoding='utf-8') as f:
        urls = f.readlines()
    print(f"[+] 开始存活探测，共加载 {len(urls)} 个域名")
    multi_check(urls)
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in res:
            clean_line = line.strip()
            if clean_line:
                print(f"[+] 存活URL：{clean_line}")
                f.write(clean_line + "\n")
    print(f"[+] 存活探测完成，共发现 {len(res)} 个存活URL，已写入 {output_file}")
    return len(res) > 0

# ===================== 原有核心功能 =====================
def get_url():
    if not os.path.exists('1.txt'):
        print("[-] 未找到 1.txt 文件，请检查路径")
        return
    with open('1.txt', 'r', encoding='utf-8') as f:
        urls = f.read().splitlines()
    for url in urls:
        url = url.strip()
        if not url:
            continue
        target = url
        print(f"\n[+] 开始处理目标：{target}")
        # ========== OneForAll 信息收集 ==========
        do_oneforall(target)
        # ========== 子域名提取 ==========
        extract_subdomains()
        # ========== 存活探测 ==========
        has_survival = run_survival_detection()
        # ========== Xray 扫描 ==========
        if has_survival:
            do_scan()
        else:
            print(f"[-] 无存活URL，跳过Xray扫描：{target}")
    print("\n[+] 全部任务完成：OneForAll信息收集 + 子域名提取 + 存活探测 + Xray扫描 ~")

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

def extract_subdomains():
    tmp_dir = os.path.abspath("./OneForAll/results/temp")
    output_file = "urls.txt"
    domains = set()
    try:
        txt_files = glob.glob(os.path.join(tmp_dir, "*.txt"))
        if not txt_files:
            print(f"[-] 未在 {tmp_dir} 找到任何txt文件")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("")
            return
        for file_path in txt_files:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    domain_pattern = re.compile(r'([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})')
                    match = domain_pattern.search(line)
                    if match:
                        domain = match.group(1)
                        domains.add(domain)
        with open(output_file, 'w', encoding='utf-8') as f:
            for domain in sorted(domains):
                f.write(domain + '\n')
        print(f"[+] 成功提取 {len(domains)} 个唯一域名，已写入 {output_file}")
    except Exception as e:
        print(f"[-] 提取子域名失败：{e}")


def do_scan():
    import subprocess

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

if __name__ == '__main__':
    # 修复 __file__ 报错
    current_path = os.getcwd()
    os.chdir(current_path)
    get_url()