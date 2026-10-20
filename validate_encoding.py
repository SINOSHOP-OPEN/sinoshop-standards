#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SINOSHOP 编码标准规范体系 — 编码格式验证脚本
验证物理实体编码是否符合 R23.2-REV.1 规范

用法:
    python validate_encoding.py
    python validate_encoding.py --code "SINOSHOP-CHN01-TN-GTC06803-MMM001-SLFS-MOD-27-V01"

作者: SINOSHOP 总架构师办公室
版本: 1.0.0
日期: 2026-07-09
"""

import re
import sys
from typing import Tuple, List, Optional


class EncodingValidator:
    """
    SINOSHOP 编码格式验证器
    基于 R23.2-REV.1 编码标准规范
    """

    # 编码格式正则表达式
    # 格式: [项目码5位]-[功能段分类码2位]-[方向码3位][公里序号3位][27m模块序号2位]-[空间方位码3位][顺序号3位]-[部件类型码3-8位]-[版本号3位]
    PATTERN = re.compile(
        r'^SINOSHOP-'
        r'(?P<project>[A-Z]{3}\d{2})-'          # 项目码
        r'(?P<segment>[A-Z]{2,3})-'             # 功能段分类码
        r'(?P<direction>[A-Z]{3})'              # 方向码
        r'(?P<km>\d{3})'                        # 公里序号
        r'(?P<module>\d{2})-'                   # 27m模块序号
        r'(?P<orientation>[A-Z]{3})'            # 空间方位码
        r'(?P<seq>\d{3})-'                      # 顺序号
        r'(?P<type>[A-Z0-9\-]{3,8})-'           # 部件类型码
        r'(?P<version>V\d{2})$'                 # 版本号
    )

    # 有效功能段分类码
    VALID_SEGMENTS = {'FB', 'TN', 'AP', 'TR', 'IS', 'LB', 'HYD', 'ARC'}

    # 有效方向码
    VALID_DIRECTIONS = {'GTC', 'CFL'}

    # 有效空间方位码
    VALID_ORIENTATIONS = {
        'IUM', 'IML', 'IMR', 'OUM', 'MMM', 'IDA', 'OAF',
        'IDU', 'ODU', 'IDF', 'IDB', 'ODU-LCS', 'ODU-SLFS', 'IUM-BUF'
    }

    # 有效部件类型码（核心）
    VALID_TYPES = {
        # SLFS 核心
        'SLFS-SFT', 'SLFS-MOD-27', 'SLFS-SEG-297',
        'SLFS-UNIT-300', 'SLFS-BUF-3', 'SLFS-SHELL',
        'SLFS-BEAM', 'SLFS-PLAT-A', 'SLFS-PLAT-B',
        # DSH 系统
        'DSH-L1', 'DSH-L2', 'DSH-R2', 'DSH-R1',
        # 水锚锤系统
        'ANCHOR-WATER', 'ANCHOR-COUPLER', 'ANCHOR-ROD-A', 'ANCHOR-ROD-B',
        # 防波堤/浮岛
        'BRK-300-L', 'BRK-300-R', 'FLB-LIFE-L', 'FLB-LIFE-R', 'FLB-TRAFFIC',
        # 通用模块
        'FLB', 'SFT', 'M18-PYR-K', 'M18-PYR-KT', 'M18-MID', 'M18-INR',
        'LCS-L-1', 'LCS-L0', 'LCS-L1', 'LCS-L2', 'LCS-L3', 'LCS-L4',
        'LCS-L5a', 'LCS-L5b', 'LCS-L4-HDA',
        'ENG-W01', 'ENG-W02', 'ENG-W03', 'ENG-W04', 'ENG-W05', 'ENG-W06',
        'SHELL-065', 'HC-21', 'HC-22', 'HC-RING',
        'DFSH', 'STEG', 'THEX', 'FLXC', 'CDP', 'DPT-CORE'
    }

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.errors = []
        self.warnings = []

    def validate(self, code: str) -> Tuple[bool, List[str], List[str]]:
        """
        验证单个编码是否符合规范

        Args:
            code: 待验证的编码字符串

        Returns:
            Tuple[bool, List[str], List[str]]: (是否通过, 错误列表, 警告列表)
        """
        self.errors = []
        self.warnings = []

        # 1. 检查整体格式
        match = self.PATTERN.match(code)
        if not match:
            self.errors.append(f"编码格式不匹配: {code}")
            return False, self.errors, self.warnings

        groups = match.groupdict()

        # 2. 验证项目码 (基本检查)
        if not groups['project'].isalnum():
            self.errors.append(f"项目码格式错误: {groups['project']}")

        # 3. 验证功能段分类码
        if groups['segment'] not in self.VALID_SEGMENTS:
            self.warnings.append(
                f"功能段分类码 '{groups['segment']}' 不在标准列表中"
            )

        # 4. 验证方向码
        if groups['direction'] not in self.VALID_DIRECTIONS:
            self.errors.append(f"方向码错误: {groups['direction']}")

        # 5. 验证模块序号范围
        module_num = int(groups['module'])
        if module_num < 0 or module_num > 36:
            self.warnings.append(f"27m模块序号 {module_num} 超出范围 (00-36)")

        # 6. 验证空间方位码
        if groups['orientation'] not in self.VALID_ORIENTATIONS:
            self.warnings.append(
                f"空间方位码 '{groups['orientation']}' 不在标准列表中"
            )

        # 7. 验证部件类型码
        if groups['type'] not in self.VALID_TYPES:
            self.warnings.append(
                f"部件类型码 '{groups['type']}' 不在标准列表中"
            )

        # 8. 验证版本号
        if not groups['version'].startswith('V'):
            self.errors.append(f"版本号格式错误: {groups['version']}")

        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings


def test_encoding_examples():
    """测试编码示例"""
    validator = EncodingValidator(verbose=True)

    test_codes = [
        # SLFS 核心模块
        "SINOSHOP-CHN01-TN-GTC06803-MMM001-SLFS-UNIT-300-V01",
        "SINOSHOP-CHN01-TN-GTC06803-MMM001-SLFS-BUF-3-V01",
        "SINOSHOP-CHN01-TN-GTC06803-MMM001-SLFS-MOD-27-V01",
        # DSH 系统
        "SINOSHOP-CHN01-HYD-GTC06803-ODU001-DSH-L2-V01",
        "SINOSHOP-CHN01-HYD-GTC06803-ODU001-DSH-L1-V01",
        # 水锚锤系统
        "SINOSHOP-CHN01-TN-GTC06803-ODU001-ANCHOR-WATER-V01",
        "SINOSHOP-CHN01-TN-GTC06803-ODU001-ANCHOR-COUPLER-V01",
        # 防波堤/浮岛
        "SINOSHOP-CHN01-FB-GTC06803-IUM001-FLB-LIFE-L-V01",
        "SINOSHOP-CHN01-HYD-GTC06803-OAF001-BRK-300-R-V01",
    ]

    print("=" * 70)
    print(" SINOSHOP 编码标准规范体系 — 编码验证测试")
    print("=" * 70)

    passed = 0
    failed = 0

    for code in test_codes:
        is_valid, errors, warnings = validator.validate(code)
        status = "✅" if is_valid else "❌"
        print(f"\n{status} {code}")
        for err in errors:
            print(f"   ❌ 错误: {err}")
        for warn in warnings:
            print(f"   ⚠️ 警告: {warn}")
        if is_valid and not warnings:
            print("   ✅ 完全符合规范")
        passed += 1 if is_valid else 0
        failed += 0 if is_valid else 1

    print("\n" + "=" * 70)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 70)
    return passed, failed


def main():
    """主函数"""
    import argparse
    parser = argparse.ArgumentParser(
        description='SINOSHOP 编码标准规范验证工具'
    )
    parser.add_argument(
        '--code', type=str,
        help='要验证的单个编码字符串'
    )
    parser.add_argument(
        '--test', action='store_true',
        help='运行编码示例测试'
    )

    args = parser.parse_args()

    if args.test:
        test_encoding_examples()
        return

    if args.code:
        validator = EncodingValidator()
        is_valid, errors, warnings = validator.validate(args.code)
        print(f"编码: {args.code}")
        print(f"结果: {'✅ 通过' if is_valid else '❌ 失败'}")
        for err in errors:
            print(f"  ❌ 错误: {err}")
        for warn in warnings:
            print(f"  ⚠️ 警告: {warn}")
        return

    # 默认：显示帮助信息
    print(__doc__)


if __name__ == "__main__":
    main()
