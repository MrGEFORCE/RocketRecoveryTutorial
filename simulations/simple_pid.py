"""

这段代码定义了一个名为PID的类，它包含了一个构造函数和一个__call__方法。构造函数用于初始化PID控制器的参数，如比例系数（Kp）、积分系数（Ki）、微分系数（Kd）、设定点（setpoint）、输出限制（output_limits）以及是否在测量值上使用微分（differential_on_measurement）。__call__方法用于计算控制器的输出，它接收当前测量值和时间间隔（dt）作为输入，并返回控制信号。

（内容由讯飞星火AI生成）
"""

class PID:
    def __init__(self, Kp, Ki, Kd, setpoint, output_limits=(0, 1), differential_on_measurement=False):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.output_limits = output_limits
        self.differential_on_measurement = differential_on_measurement
        self.integral = 0
        self.previous_error = 0

    def __call__(self, measurement, dt):
        error = self.setpoint - measurement
        self.integral += error * dt
        derivative = (error - self.previous_error) / dt if self.differential_on_measurement else 0
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        output = max(self.output_limits[0], min(self.output_limits[1], output))
        self.previous_error = error
        return output

    def reset(self):
        self.integral = 0
        self.previous_error = 0