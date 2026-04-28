import os

def get_url():
    current_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_path)

    print("="*60)
    print("[+] 开始自动化扫描（干净环境，不崩溃）")
    print("="*60)

    # ===================== 步骤1 OneForAll（改用 subprocess 干净启动）
    print("\n[1/4] 正在执行 OneForAll 批量扫描...")
    os.system("cd OneForAll && python oneforall.py --targets ../1.txt run")

    # ===================== 步骤2 提取域名
    print("\n[2/4] 提取子域名 → urls.txt")
    from modules.url_extractor import extract_subdomains
    extract_subdomains()

    # ===================== 步骤3 存活探测
    print("\n[3/4] 存活探测 → url.txt")
    from modules.survival_checker import run_survival_detection
    has_survival = run_survival_detection()

    # ===================== 步骤4 Xray（关键！）
    print("\n[4/4] Xray 扫描 → 10.html")
    if has_survival:
        from modules.scanner import do_scan
        do_scan()
    else:
        print("[-] 无存活URL")

    print("\n[+] 全部完成！")

if __name__ == '__main__':
    get_url()