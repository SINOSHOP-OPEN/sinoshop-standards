#!/usr/bin/env python3
"""一键脱敏检查脚本：扫描提交目录中是否包含受限参数。"""
import sys
import os
import re

PATTERNS = [
    r'natural_frequency\s*=\s*\d+\.\d+',
    r'damping_ratio\s*=\s*\d+\.\d+',
    r'tld_frequency_map\s*=\s*\d+',
    r'anchor_stiffness_real\s*=\s*',
    r'ballast_volume_exact\s*=\s*',
]

def check_path(target):
    found = False
    for root, _, files in os.walk(target):
        for f in files:
            if f.endswith(('.py', '.sol', '.md', '.txt', '.json')):
                path = os.path.join(root, f)
                with open(path, 'r', errors='ignore') as fh:
                    content = fh.read()
                for pat in PATTERNS:
                    if re.search(pat, content):
                        print(f"RESTRICTED_LEAK: {path} matches pattern: {pat}")
                        found = True
    if not found:
        print("CLEAN")
    return found

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    sys.exit(1 if check_path(target) else 0)
