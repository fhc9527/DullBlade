import os
import re
import threading
import requests
import time

# 存活探测核心配置
requests.packages.urllib3.disable_warnings()
requests.adapters.DEFAULT_RETRIES = 5
STATUS_CODES = [200,301,302, 403]
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