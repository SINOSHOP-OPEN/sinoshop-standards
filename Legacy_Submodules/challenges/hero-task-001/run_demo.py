#!/usr/bin/env python3
"""
Hero Task 001 仿真主程序 - Rev 3.2 TLD 协同版
支持 basic / twin-hull-tld 双模式，含简化非线性动力学。
"""
import argparse
import json
import hashlib
import sys
import time
from datetime import datetime, timezone

import numpy as np

try:
    from python.controller import compute
except ImportError:
    def compute(y_A, y_B, dt, state, platform_L=None, platform_R=None, tld_state=None):
        return (0.0, 0.0)


class TwinHullSimulator:
    """双体悬浮隧道 + TLD + 外侧平台简化动力学仿真器。"""

    def __init__(self, mode="basic", seed=42):
        self.mode = mode
        self.rng = np.random.RandomState(seed)

        # 归一化物理参数（公开级，脱敏后）
        self.dt = 0.1            # 采样周期 [s]
        self.steps = 1000        # 仿真步数
        self.delay_steps = 2     # 20% 时滞 (20% * 10 = 2 步)
        self.dead_zone = 0.03    # 归一化盲区 ≈ 30mm

        # 质量与阻尼
        self.mass = 1.0          # 归一化质量
        self.damping = 0.1       # 结构阻尼
        self.spring = 0.05       # 恢复刚度

        # TLD 参数 (仅 twin-hull-tld 模式)
        self.tld_freq_range = np.linspace(0.12, 0.18, 7)  # 归一化共振频带
        self.tld_level = 0.5     # 当前液位 (0-1)
        self.tld_power = 0.0     # 捕获功率

        # 外侧平台
        self.platform_freq = 0.12  # 主波浪频率
        self.platform_amplitude = 0.1

        # 历史缓冲区（用于时滞模拟）
        self.u_buffer = [(0.0, 0.0)] * self.delay_steps

    def generate_wave(self, t):
        """生成 JONSWAP 简化波浪 + 1/f 噪声。"""
        wave = self.platform_amplitude * np.sin(2 * np.pi * self.platform_freq * t)
        wave += 0.02 * self.rng.randn()  # 1/f 噪声简化
        return wave

    def step(self, y_A, y_B, t):
        """单步动力学推进。"""
        # 外侧平台位移
        platform_L = self.generate_wave(t)
        platform_R = self.generate_wave(t + 0.5)

        # TLD 重心偏移力矩（简化：假设液位变化产生线性力矩）
        tld_moment_A = 0.0
        tld_moment_B = 0.0
        tld_power = 0.0

        if self.mode == "twin-hull-tld":
            # 窄缝共振频率估计（假设检测到主要频率）
            detected_freq = self.platform_freq + 0.01 * self.rng.randn()
            # 寻找最接近的 TLD 调谐频率
            idx = np.argmin(np.abs(self.tld_freq_range - detected_freq))
            self.tld_level = 0.3 + 0.5 * (idx / len(self.tld_freq_range))
            # 反相抵消力矩（简化模型）
            tld_moment_A = -0.02 * np.sign(y_A) * self.tld_level
            tld_moment_B = -0.02 * np.sign(y_B) * self.tld_level
            tld_power = 0.1 * self.tld_level * abs(platform_L - platform_R)

        tld_state = {
            "level": self.tld_level,
            "frequency": self.tld_freq_range[idx] if self.mode == "twin-hull-tld" else 0.15,
            "power": tld_power
        }

        # 调用控制器（传入时延后的状态）
        # 时滞模拟：控制器使用延迟的历史值
        state = {}
        u_A, u_B = compute(y_A, y_B, self.dt, state, platform_L, platform_R, tld_state)

        # 死区：微小指令被抑制
        if abs(u_A) < self.dead_zone:
            u_A = 0.0
        if abs(u_B) < self.dead_zone:
            u_B = 0.0

        # 指令限幅
        u_A = max(-1.0, min(1.0, u_A))
        u_B = max(-1.0, min(1.0, u_B))

        # 一阶惯性 + 阻尼 + TLD 力矩 + 波浪力
        wave_force = 0.05 * self.generate_wave(t)
        y_A_new = y_A + self.dt * (
            -self.damping * y_A + self.mass * u_A + tld_moment_A + wave_force
        )
        y_B_new = y_B + self.dt * (
            -self.damping * y_B + self.mass * u_B + tld_moment_B + wave_force
        )

        return y_A_new, y_B_new, platform_L, platform_R, tld_state, abs(u_A) + abs(u_B) > 0

    def run(self):
        """运行完整仿真。"""
        y_A, y_B = 0.0, 0.0
        history = []

        for step in range(self.steps):
            t = step * self.dt
            y_A, y_B, pL, pR, tld_state, triggered = self.step(y_A, y_B, t)
            history.append((y_A, y_B, tld_state["power"]))

        # 指标计算
        y_A_arr = np.array([h[0] for h in history])
        y_B_arr = np.array([h[1] for h in history])
        power_arr = np.array([h[2] for h in history])

        rmsd_a = np.sqrt(np.mean(y_A_arr**2))
        rmsd_b = np.sqrt(np.mean(y_B_arr**2))
        rmsd = (rmsd_a + rmsd_b) / 2

        phase_error = np.mean(np.abs(np.diff(y_A_arr - y_B_arr)))

        tld_efficiency = np.sum(power_arr) / self.steps

        # 执行器换向次数（简化计数）
        u_signs = np.sign(np.diff(y_A_arr))
        switches = int(np.sum(np.abs(np.diff(u_signs)) > 0))

        result = {
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "rmsd": round(rmsd, 4),
            "phase_error": round(phase_error, 4),
            "tld_efficiency": round(tld_efficiency, 4),
            "actuator_switches": switches,
            "gas_estimate": 85000 + int(switches * 0.5),
        }
        result["proof"] = hashlib.sha256(
            json.dumps(result, sort_keys=True).encode()
        ).hexdigest()

        return result, history


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hero Task 001 Simulation Runner")
    parser.add_argument("--visualize", action="store_true", help="Enable real-time visualization")
    parser.add_argument("--benchmark", action="store_true", help="Output benchmark result")
    parser.add_argument("--output-json", type=str, default=None, help="Save result to JSON file")
    parser.add_argument(
        "--mode", type=str, default="basic",
        choices=["basic", "twin-hull-tld"],
        help="Simulation mode (basic or twin-hull-tld)"
    )
    args = parser.parse_args()

    sim = TwinHullSimulator(mode=args.mode)
    result, history = sim.run()

    if args.visualize:
        try:
            import matplotlib.pyplot as plt
            yA = [h[0] for h in history]
            yB = [h[1] for h in history]
            power = [h[2] for h in history]
            plt.figure(figsize=(12, 5))
            plt.subplot(2, 1, 1)
            plt.plot(yA, label="y_A")
            plt.plot(yB, label="y_B")
            plt.legend()
            plt.title(f"Twin-Hull Positions (RMSD={result['rmsd']:.4f})")
            plt.subplot(2, 1, 2)
            plt.plot(power, label="TLD Power")
            plt.legend()
            plt.title(f"TLD Energy Capture (Efficiency={result['tld_efficiency']:.4f})")
            plt.tight_layout()
            plt.show()
        except ImportError:
            print("Matplotlib not installed. Skipping visualization.")

    if args.benchmark or args.output_json is None:
        print(f"Baseline RMSD: {result['rmsd']:.4f}")
        print(f"Phase Error:  {result['phase_error']:.4f}")
        print(f"TLD Eff:      {result['tld_efficiency']:.4f}")
        print(f"Switches:     {result['actuator_switches']}")
        print(f"Gas Estimate: {result['gas_estimate']}")
        print(f"Proof:        {result['proof'][:16]}...")

    if args.output_json:
        with open(args.output_json, "w") as f:
            json.dump(result, f, indent=2)
        print(f"Results saved to {args.output_json}")
