# BandpassFilter API (Public Interface)

## get_filter_coefficients()
返回带通滤波器的占位系数（实际参数由 Blackbox 动态注入）。

| 参数 | 类型 | 说明 |
|---|---|---|
| low_cutoff | float | 低频截止频率 (Hz) — 潮汐通道 |
| high_cutoff | float | 高频截止频率 (Hz) — 载荷通道 |

## apply_filter(signal, coefficients)
对输入信号应用带通滤波，返回分离后的低频/高频分量。
