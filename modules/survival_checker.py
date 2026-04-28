import os
import re
import threading
import requests
import time

# 核心配置
requests.packages.urllib3.disable_warnings()  # 禁用SSL警告
requests.adapters.DEFAULT_RETRIES = 5         # 重试5次
STATUS_CODES = [200, 403, 500, 502, 503, 301,302,401] # 存活状态码（包含常见非200成功码）
TIMEOUT = 1
URLS_PER_THREAD = 20
lock = threading.Lock() # 线程锁，防止多线程写文件冲突

def check(url):
    """核心探测函数，静音模式，不打印任何错误"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'}
        res = requests.get(url=url, headers=headers, timeout=TIMEOUT, verify=False)
        if res.status_code in STATUS_CODES:
            return url # 返回成功的URL，不返回状态码
    except:
        # 空except，捕获所有异常，直接忽略，不打印任何东西
        pass
    return None # 失败则返回None

def list_split(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)]

def checks(urls, result_list):
    """多线程探测，只收集成功的URL"""
    for url in urls:
        url = url.strip()
        if not url:
            continue
        
        # 自动拼接 http 和 https
        http_url = f"http://{url}"
        https_url = f"https://{url}"
        
        # 优先探测https
        success_url = check(https_url)
        if not success_url:
            success_url = check(http_url)
            
        if success_url:
            with lock: # 加锁保证线程安全
                result_list.append(success_url)

def run_survival_detection():
    """主函数：只输出成功的URL，完全静音"""
    urls_file = "urls.txt"
    output_file = "url.txt"
    
    # 前置检查
    if not os.path.exists(urls_file) or os.path.getsize(urls_file) == 0:
        print(f"[-] {urls_file} 不存在或为空，跳过存活探测")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("")
        return False # 无结果
    
    # 读取并去重原始URL
    with open(urls_file, 'r', encoding='utf-8') as f:
        raw_urls = list(set([line.strip() for line in f if line.strip()]))
    
    if not raw_urls:
        print("[-] 无有效URL待探测")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("")
        return False

    print(f"[+] 开始存活探测（共 {len(raw_urls)} 个目标）...")
    
    # 多线程处理
    result_list = []
    threads = []
    for url_chunk in list_split(raw_urls, URLS_PER_THREAD):
        t = threading.Thread(target=checks, args=(url_chunk, result_list))
        t.start()
        threads.append(t)
    
    # 等待所有线程结束
    for t in threads:
        t.join()
    
    # 去重最终结果
    unique_results = list(set(result_list))
    
    # 写入成功的URL
    with open(output_file, 'w', encoding='utf-8') as f:
        for url in unique_results:
            f.write(url + "\n")
    
    # 打印统计结果（只打印成功的）
    print(f"\n[+] 存活探测完成！")
    print(f"[+] 总目标：{len(raw_urls)}")
    print(f"[+] 存活URL：{len(unique_results)}")
    print(f"[+] 结果已写入：{output_file}\n")
    
    return len(unique_results) > 0 # 返回是否有存活