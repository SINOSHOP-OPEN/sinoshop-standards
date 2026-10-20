#!/usr/bin/env python3
"""
Venturi_Flow_Sim.py — 文丘里虹吸流量与发电功率计算 (v2.0 工程优化版)
SINOSHOP-OS 潮汐发电水舱 | 技术团队：苏月明、梁诚超、梁振雄

安全声明：核心经验参数已移至 tidal_config.yaml，此版本使用脱敏值。
"""

import math
import yaml
from dataclasses import dataclass
from typing import Tuple, Optional

@dataclass
class VenturiParams:
    inlet_diameter: float = 1.2
    throat_diameter: float = 0.6
    discharge_coefficient: float = 0.90      # 脱敏值
    turbine_efficiency: float = 0.75          # 脱敏值
    temperature_c: float = 20.0               # 海水温度 (°C)
    salinity_psu: float = 35.0                # 盐度 (PSU)
    
    @property
    def area_ratio(self) -> float:
        return (self.throat_diameter / self.inlet_diameter) ** 2
    
    @property
    def seawater_density(self) -> float:
        """温度/盐度修正的海水密度计算 (kg/m³)"""
        # 标准海水状态方程简化版
        rho0 = 1025.0
        alpha = 0.00015  # 热膨胀系数
        beta = 0.00078   # 盐度收缩系数
        return rho0 - alpha * (self.temperature_c - 20.0) + beta * (self.salinity_psu - 35.0)

def load_config(config_path: str = "tidal_config.yaml") -> dict:
    """从外部配置文件加载参数（黑盒化策略）"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {}

def calc_flow_velocity(water_head: float, params: VenturiParams) -> float:
    """文丘里喉部流速 (m/s)"""
    g = 9.81
    if water_head <= 0.2:
        return 0.0
    base_velocity = math.sqrt(2 * g * water_head)
    return params.discharge_coefficient * base_velocity * (1.0 / params.area_ratio)

def calc_power_output(water_head: float, params: VenturiParams) -> Tuple[float, float]:
    """发电功率 (kW) + 流速 (m/s)，含温盐修正"""
    velocity = calc_flow_velocity(water_head, params)
    area = math.pi * (params.throat_diameter / 2) ** 2
    flow_rate = velocity * area
    hydraulic_power = params.seawater_density * flow_rate * 9.81 * water_head
    electrical_power = hydraulic_power * params.turbine_efficiency / 1000
    return electrical_power, velocity

if __name__ == "__main__":
    cfg = load_config()
    params = VenturiParams()
    
    print("=" * 50)
    print("🌊 文丘里发电功率曲线（脱敏参数）")
    print(f"   海水密度: {params.seawater_density:.1f} kg/m³")
    print(f"   面积比: {params.area_ratio:.4f}")
    print("=" * 50)
    
    for head in [0.5, 1.5, 2.7, 4.0]:
        pwr, vel = calc_power_output(head, params)
        print(f"  水头 {head:.1f}m → 发电 {pwr:.2f}kW (流速 {vel:.2f}m/s)")
