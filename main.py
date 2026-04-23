import os
from modules.url_extractor import extract_subdomains
from modules.survival_checker import run_survival_detection
from modules.scanner import do_scan

def get_url():
    # 脚本目录固定
    current_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_path)

    print("="*60)
    print("[+] 开始自动化扫描流程")
    print("="*60)

    # ===================== 步骤1：OneForAll 批量扫描 1.txt
    print("\n[1/4] 正在执行 OneForAll 批量扫描...")
    os.system("cd OneForAll && python oneforall.py --targets ../1.txt run")

    # ===================== 步骤2：提取子域名到 urls.txt
    print("\n[2/4] 正在提取子域名 → urls.txt")
    extract_subdomains()

    # ===================== 步骤3：存活探测 → url.txt
    print("\n[3/4] 正在存活探测 → url.txt")
    has_survival = run_survival_detection()

    # ===================== 步骤4：XRAY 扫描 url.txt
    print("\n[4/4] 正在 Xray 扫描 → 10.html")
    if has_survival:
        do_scan()
    else:
        print("[-] 无存活URL，跳过Xray")

    print("\n[+] 所有流程全部完成！")

if __name__ == '__main__':
    get_url()
