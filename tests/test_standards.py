#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SINOSHOP 编码标准规范体系 — 单元测试

测试编码验证工具的正确性
基于 R23.2-REV.1 规范

用法:
    python -m pytest tests/
    python tests/test_standards.py

作者: SINOSHOP 总架构师办公室
版本: 1.0.0
"""

import unittest
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from validate_encoding import EncodingValidator


class TestEncodingValidator(unittest.TestCase):
    """编码验证器测试类"""

    def setUp(self):
        """测试前置"""
        self.validator = EncodingValidator()

    def test_valid_slfs_module(self):
        """测试有效的 SLFS 模块编码"""
        code = "SINOSHOP-CHN01-TN-GTC06803-MMM001-SLFS-UNIT-300-V01"
        is_valid, errors, warnings = self.validator.validate(code)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_valid_water_anchor(self):
        """测试有效的水锚锤编码"""
        code = "SINOSHOP-CHN01-TN-GTC06803-ODU001-ANCHOR-WATER-V01"
        is_valid, errors, warnings = self.validator.validate(code)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_valid_dsh(self):
        """测试有效的 DSH 编码"""
        code = "SINOSHOP-CHN01-HYD-GTC06803-ODU001-DSH-L2-V01"
        is_valid, errors, warnings = self.validator.validate(code)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_valid_flb(self):
        """测试有效的浮岛编码"""
        code = "SINOSHOP-CHN01-FB-GTC06803-IUM001-FLB-LIFE-L-V01"
        is_valid, errors, warnings = self.validator.validate(code)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_invalid_format(self):
        """测试无效格式"""
        code = "INVALID-CODE-FORMAT"
        is_valid, errors, warnings = self.validator.validate(code)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)

    def test_invalid_direction(self):
        """测试无效方向码"""
        code = "SINOSHOP-CHN01-TN-XXX06803-MMM001-SLFS-UNIT-300-V01"
        is_valid, errors, warnings = self.validator.validate(code)
        self.assertFalse(is_valid)
        self.assertIn("方向码错误", "".join(errors))

    def test_module_range(self):
        """测试模块序号范围"""
        code = "SINOSHOP-CHN01-TN-GTC06837-MMM001-SLFS-UNIT-300-V01"
        is_valid, errors, warnings = self.validator.validate(code)
        self.assertTrue(is_valid)
        self.assertGreater(len(warnings), 0)

    def test_lcs_hda(self):
        """测试液压差分作动器编码"""
        code = "SINOSHOP-CHN01-TN-GTC06803-MMM001-LCS-L4-HDA-V01"
        is_valid, errors, warnings = self.validator.validate(code)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_parse_component(self):
        """测试组件解析"""
        from examples.example_encoding import SINOSHOPComponent
        code = "SINOSHOP-CHN01-TN-GTC06803-MMM001-SLFS-UNIT-300-V01"
        component = SINOSHOPComponent.from_encoding(code)
        self.assertIsNotNone(component)
        self.assertEqual(component.project, "CHN01")
        self.assertEqual(component.segment, "TN")
        self.assertEqual(component.km, 68)
        self.assertEqual(component.module, 3)
        self.assertEqual(component.component_type, "SLFS-UNIT-300")
        self.assertEqual(component.version, "V01")

    def test_roundtrip(self):
        """测试编码-解析-重新编码的一致性"""
        from examples.example_encoding import SINOSHOPComponent
        original = "SINOSHOP-CHN01-TN-GTC06803-MMM001-SLFS-UNIT-300-V01"
        component = SINOSHOPComponent.from_encoding(original)
        regenerated = component.to_encoding()
        self.assertEqual(original, regenerated)


def run_tests():
    """运行所有测试"""
    print("=" * 60)
    print(" SINOSHOP 编码标准规范体系 — 单元测试")
    print("=" * 60)
    print(f"测试用例: {len([m for m in dir(TestEncodingValidator) if m.startswith('test_')])}")
    print("=" * 60)

    # 运行测试
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == "__main__":
    run_tests()
