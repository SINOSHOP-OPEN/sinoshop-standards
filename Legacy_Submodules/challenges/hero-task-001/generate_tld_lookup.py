#!/usr/bin/env python3
"""预计算 TLD 液位‑频率映射表，导出为 Solidity uint256[] 常量。"""
import numpy as np

FREQUENCIES = np.linspace(0.12, 0.18, 7)   # 归一化频率
LEVELS = np.array([10, 20, 30, 40, 50, 60, 70])  # 液位百分比
SCALE = 10**6

print("// SPDX-License-Identifier: MIT")
print("pragma solidity ^0.8.20;")
print()
print("library TLDLookup {")
print("    uint256 constant SCALE = 1e6;")
print("    uint256[] public frequencyTable = [", end="")
for f in FREQUENCIES:
    print(f"{int(f * SCALE)}, ", end="")
print("];")
print("    uint256[] public levelTable = [", end="")
for l in LEVELS:
    print(f"{int(l * SCALE)}, ", end="")
print("];")
print("}")
