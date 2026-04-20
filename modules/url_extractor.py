import os
import re
import glob

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