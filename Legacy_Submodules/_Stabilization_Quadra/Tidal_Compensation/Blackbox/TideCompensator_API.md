# TideCompensator API (Public Interface)

## get_compensation(tide_level, wave_height, platform_angle)
返回 1.7m 水舱的目标容积调节指令。

| 参数 | 类型 | 单位 | 说明 |
|---|---|---|---|
| tide_level | float | m | 当前潮位 |
| wave_height | float | m | 有效波高 |
| platform_angle | float | rad | 平台倾斜角 |

## 内部黑盒参数（不公开）
- 非线性气动扭矩系数
- 文丘里喉部空化阈值
- 1:1.03 负浮力动态补偿曲线
