import os
from modules.url_extractor import extract_subdomains
from modules.survival_checker import run_survival_detection
from modules.scanner import do_scan
from utils.oneforall_runner import do_oneforall

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

if __name__ == '__main__':
    # 修复 __file__ 报错
    current_path = os.getcwd()
    os.chdir(current_path)
    get_url()