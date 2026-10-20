"""
Hero Task 001 控制器模板 - 基线 PID + 简单低通滤波
您可以完全重写 compute() 函数，只需保持接口一致。
"""

def compute(y_A: float, y_B: float, dt: float, state: dict,
            platform_L: float = None, platform_R: float = None,
            tld_state: dict = None) -> tuple[float, float]:
    """
    姿态稳定主算法

    参数:
        y_A, y_B: 双体位移 [归一化单位]
        dt: 采样间隔 [s]
        state: 持久化状态字典，可自由存储任何变量
        platform_L, platform_R: 两侧平台位移 [归一化单位] (可选)
        tld_state: TLD 水舱状态 (可选，需 L3 审核)

    返回:
        (u_A, u_B): 双体执行器指令，范围 [-1.0, 1.0]
    """
    # 初始化持久化状态
    if 'init' not in state:
        state['init'] = True
        state['integral_A'] = 0.0
        state['integral_B'] = 0.0
        state['prev_error_A'] = 0.0
        state['prev_error_B'] = 0.0

    # 控制参数（可根据需要调整）
    Kp = 0.4
    Ki = 0.05
    Kd = 0.1

    # 计算误差
    error_A = -y_A
    error_B = -y_B

    # 积分项（带限幅）
    state['integral_A'] += error_A * dt
    state['integral_B'] += error_B * dt
    state['integral_A'] = max(-10.0, min(10.0, state['integral_A']))
    state['integral_B'] = max(-10.0, min(10.0, state['integral_B']))

    # 微分项
    if dt > 1e-6:
        deriv_A = (error_A - state['prev_error_A']) / dt
        deriv_B = (error_B - state['prev_error_B']) / dt
    else:
        deriv_A = 0.0
        deriv_B = 0.0

    state['prev_error_A'] = error_A
    state['prev_error_B'] = error_B

    # PID 输出
    u_A = Kp * error_A + Ki * state['integral_A'] + Kd * deriv_A
    u_B = Kp * error_B + Ki * state['integral_B'] + Kd * deriv_B

    # 限幅
    u_A = max(-1.0, min(1.0, u_A))
    u_B = max(-1.0, min(1.0, u_B))

    return (u_A, u_B)
