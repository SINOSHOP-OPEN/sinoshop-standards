# 🔐 Blackbox 接口层

本目录提供预编译的核心控制库的**公共 API 头文件**。

## 使用方式

\\\python
from sinoshop_blackbox import BandpassFilter, TideCompensator

filter = BandpassFilter(low_cutoff=0.0001, high_cutoff=0.1)
command = TideCompensator.get_compensation(tide_level=3.2, wave_height=8.0, platform_angle=0.03)
\\\

## 二进制库获取

核心 .so / .dll 文件需通过 SINOSHOP-Core 技术团队授权获取。
联系：standards@sinoshop.org
