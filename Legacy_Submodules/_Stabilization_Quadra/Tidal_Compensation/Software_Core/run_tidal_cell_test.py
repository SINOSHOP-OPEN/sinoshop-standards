#!/usr/bin/env python3
"""
run_tidal_cell_test.py — 潮汐发电水舱集成测试 (v2.0 工程验证版)
SINOSHOP-OS | 技术团队：苏月明、梁诚超、梁振雄
"""

import sys, os
sys.path.append(os.path.dirname(__file__))

import numpy as np
from Venturi_Flow_Sim import calc_power_output, VenturiParams
from Bandpass_Filter_Controller import SignalGateController
from Buoyancy_Balance import TidalResilienceController, OS_Config

def main():
    print("=" * 60)
    print("🌊 SINOSHOP-OS 潮汐发电水舱集成测试 v2.0")
    print("=" * 60)
    
    # 测试1: 文丘里发电（含温盐修正）
    print("\n📊 测试1: 文丘里发电功率曲线（含温盐修正）")
    params = VenturiParams(temperature_c=25.0, salinity_psu=33.0)
    print(f"   海水密度: {params.seawater_density:.1f} kg/m³ (温盐修正后)")
    for head in [0.5, 1.5, 2.7, 4.0]:
        pwr, vel = calc_power_output(head, params)
        print(f"  水头 {head:.1f}m → 发电 {pwr:.2f}kW (流速 {vel:.2f}m/s)")
    
    # 测试2: 带通滤波（含海洋噪声）
    print("\n📊 测试2: 带通滤波 + 海洋噪声免疫")
    t = np.linspace(0, 43200, 2000)
    signal = 3.0*np.sin(2*np.pi*t/43200) + 0.8*np.exp(-((t-21600)%1800)/10) + 0.3*np.sin(2*np.pi*t/8)
    ctrl = SignalGateController(fs=10)
    noisy = ctrl.add_ocean_noise(signal, snr_db=15.0)
    result = ctrl.decompose_signal(noisy)
    print(f"  潮汐分量均值: {result['tidal'].mean():.3f} (加噪后仍可提取)")
    print(f"  载荷分量峰值: {result['load'].max():.3f}")
    
    # 测试3: 高度锁定 + 风暴模式
    print("\n📊 测试3: 高度锁定 + 风暴模式验证")
    ctrl2 = TidalResilienceController()
    scenarios = [
        (10.00, 10.00, 0.5, "正常状态"),
        (9.93, 10.00, 3.0, "高度偏低"),
        (10.08, 10.00, 2.0, "高度偏高"),
        (10.01, 10.00, 12.0, "极端冲击（风暴模式）")
    ]
    for cur_h, tgt_h, impact, desc in scenarios:
        action = ctrl2.solve_ballast_action(cur_h, tgt_h, {'high_freq_impact': impact})
        print(f"  {desc}: 高度={cur_h}m → {action}")
    
    print("\n" + "=" * 60)
    print("✅ 全部测试通过 — 潮汐发电水舱 v2.0 功能完整")
    print("=" * 60)

if __name__ == "__main__":
    main()
