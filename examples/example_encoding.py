"""
SINOSHOP 编码标准使用示例

本示例展示如何在实际工程中使用 SINOSHOP 编码标准体系
基于 R23.2-REV.1 规范

作者: SINOSHOP 总架构师办公室
版本: 1.0.0
"""

from dataclasses import dataclass
from typing import Optional
import re


@dataclass
class SINOSHOPComponent:
    """SINOSHOP 物理组件数据结构"""
    project: str          # 项目码
    segment: str          # 功能段分类码
    direction: str        # 方向码
    km: int               # 公里序号
    module: int           # 27m模块序号
    orientation: str      # 空间方位码
    seq: int              # 顺序号
    component_type: str   # 部件类型码
    version: str          # 版本号

    def to_encoding(self) -> str:
        """生成完整编码字符串"""
        return (
            f"SINOSHOP-{self.project}-{self.segment}-"
            f"{self.direction}{self.km:03d}{self.module:02d}-"
            f"{self.orientation}{self.seq:03d}-"
            f"{self.component_type}-{self.version}"
        )

    @classmethod
    def from_encoding(cls, encoding: str) -> Optional["SINOSHOPComponent"]:
        """从编码字符串解析组件对象"""
        pattern = re.compile(
            r'^SINOSHOP-'
            r'(?P<project>[A-Z]{3}\d{2})-'
            r'(?P<segment>[A-Z]{2,3})-'
            r'(?P<direction>[A-Z]{3})'
            r'(?P<km>\d{3})'
            r'(?P<module>\d{2})-'
            r'(?P<orientation>[A-Z]{3})'
            r'(?P<seq>\d{3})-'
            r'(?P<type>[A-Z0-9\-]{3,8})-'
            r'(?P<version>V\d{2})$'
        )
        match = pattern.match(encoding)
        if not match:
            return None
        groups = match.groupdict()
        return cls(
            project=groups['project'],
            segment=groups['segment'],
            direction=groups['direction'],
            km=int(groups['km']),
            module=int(groups['module']),
            orientation=groups['orientation'],
            seq=int(groups['seq']),
            component_type=groups['type'],
            version=groups['version']
        )


# ============================================================
# 使用示例
# ============================================================

def example_slfs_module():
    """示例1: SLFS 300m浮降单元编码"""
    print("=" * 60)
    print("示例1: SLFS 300m浮降单元")
    print("=" * 60)

    component = SINOSHOPComponent(
        project="CHN01",
        segment="TN",
        direction="GTC",
        km=68,
        module=3,
        orientation="MMM",
        seq=1,
        component_type="SLFS-UNIT-300",
        version="V01"
    )

    encoding = component.to_encoding()
    print(f"编码: {encoding}")
    print(f"位置: 第{component.km}公里 第{component.module}个27m模块")
    print(f"类型: {component.component_type}")
    print(f"版本: {component.version}")

    # 解析验证
    parsed = SINOSHOPComponent.from_encoding(encoding)
    print(f"解析验证: {'✅ 通过' if parsed else '❌ 失败'}")
    return encoding


def example_water_anchor():
    """示例2: 水锚锤电磁耦合器编码"""
    print("\n" + "=" * 60)
    print("示例2: 水锚锤电磁耦合器")
    print("=" * 60)

    component = SINOSHOPComponent(
        project="CHN01",
        segment="TN",
        direction="GTC",
        km=68,
        module=3,
        orientation="ODU",
        seq=1,
        component_type="ANCHOR-COUPLER",
        version="V01"
    )

    encoding = component.to_encoding()
    print(f"编码: {encoding}")
    print(f"安装位置: {component.orientation}")
    print(f"部件类型: {component.component_type}")
    print(f"--- 水锚锤系统参数 ---")
    print("  总重量: 650吨")
    print("  响应时间: <0.1秒")
    print("  电磁吸力: ≥700吨")

    return encoding


def example_dsh():
    """示例3: 双对称疏水道编码"""
    print("\n" + "=" * 60)
    print("示例3: 双对称疏水系统 (DSH-L2)")
    print("=" * 60)

    component = SINOSHOPComponent(
        project="CHN01",
        segment="HYD",
        direction="GTC",
        km=68,
        module=3,
        orientation="ODU",
        seq=1,
        component_type="DSH-L2",
        version="V01"
    )

    encoding = component.to_encoding()
    print(f"编码: {encoding}")
    print(f"功能段: {component.segment}")
    print(f"疏水道: {component.component_type}")
    print(f"--- DSH-L2 参数 ---")
    print("  宽度: 9m")
    print("  功能: 主消能 (180°相位差干涉)")
    print("  相位角色: 泛音")

    return encoding


def example_traffic_platform():
    """示例4: 交通浮岛编码"""
    print("\n" + "=" * 60)
    print("示例4: 交通浮岛 (SLFS)")
    print("=" * 60)

    component = SINOSHOPComponent(
        project="CHN01",
        segment="FB",
        direction="GTC",
        km=0,
        module=0,
        orientation="MMM",
        seq=1,
        component_type="FLB-TRAFFIC",
        version="V01"
    )

    encoding = component.to_encoding()
    print(f"编码: {encoding}")
    print(f"功能段: {component.segment}")
    print(f"类型: {component.component_type}")
    print(f"--- SLFS 交通区参数 ---")
    print("  宽度: 135m")
    print("  直通管: 6 × Φ18m")
    print("  浮降单元: 300m (11×27m + 3m缓冲件)")
    print("  五层载荷抵消: 0层→4层 (0-500Hz)")

    return encoding


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(" SINOSHOP 编码标准规范体系 V23.2-REV.1")
    print(" 使用示例")
    print("=" * 60)

    example_slfs_module()
    example_water_anchor()
    example_dsh()
    example_traffic_platform()

    print("\n" + "=" * 60)
    print("✅ 示例运行完成")
    print("=" * 60)
