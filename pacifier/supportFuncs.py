import time
import numpy as np


class PIDUsingE(object):
    def __init__(self, kp=1, ki=0, kd=1, limits=(-1, 1)):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.minimum = limits[0]
        self.maximum = limits[1]
        self.prev_t = time.time()
        self.prev_e = 0
        self.integral = 0

    def __call__(self, *args, **kwargs):
        err = args[0]
        dt = time.time() - self.prev_t
        self.prev_t = time.time()
        d_item = (err - self.prev_e) / dt
        self.prev_e = err
        self.integral += err * self.ki * dt
        self.integral = max(min(self.integral, self.maximum), self.minimum)
        return max(min(err * self.kp + self.integral + d_item * self.kd, self.maximum), self.minimum)


def compute_error_vector(current_heading, target_heading):  # chatGPT
    # 将方位角转换为单位向量（假设角度是从正x轴顺时针计量）
    current_vector = np.array([np.cos(np.radians(current_heading)), np.sin(np.radians(current_heading))])
    target_vector = np.array([np.cos(np.radians(target_heading)), np.sin(np.radians(target_heading))])

    # 计算叉积，得到误差方向
    cross_product = np.cross(current_vector, target_vector)

    # 计算两向量相差的距离
    angle_error = np.linalg.norm(current_vector - target_vector)

    # 如果叉积为正，说明目标角度在当前角度的顺时针方向，反之则是逆时针方向
    if cross_product > 0:
        return angle_error  # 正角度：逆时针
    else:
        return -angle_error  # 负角度：顺时针


def form_vec_description(vec: np.ndarray) -> str:
    np.set_printoptions(suppress=True)
    s = []
    for d in vec:
        s.append(str(d)[0:4])
    s = '[' + ', '.join(s) + ']'
    return s


def compute_up_vector(pitch, heading):  # chatGPT
    # Convert angles from degrees to radians
    pitch_rad = np.radians(pitch)
    heading_rad = np.radians(heading)

    # Pitch rotation matrix (around the x-axis)
    R_pitch = np.array([
        [1, 0, 0],
        [0, np.cos(pitch_rad), -np.sin(pitch_rad)],
        [0, np.sin(pitch_rad), np.cos(pitch_rad)]
    ])

    # Heading rotation matrix (around the z-axis)
    R_heading = np.array([
        [np.cos(heading_rad), -np.sin(heading_rad), 0],
        [np.sin(heading_rad), np.cos(heading_rad), 0],
        [0, 0, 1]
    ])

    # Combine both rotations (first heading, then pitch)
    R_total = np.dot(R_heading, R_pitch)

    # Initial up vector in the aircraft coordinate system (along -z axis in aircraft frame)
    up_vector_aircraft = np.array([0, 0, 1])

    # Apply the total rotation to the up vector
    up_vector_world = np.dot(R_total, up_vector_aircraft)

    return up_vector_world


def rotate_to_world(coord, roll, pitch, heading):  # chatGPT
    """
    将机体系坐标(coord)转换为世界坐标系坐标，加入roll、pitch、heading三个旋转角度，
    roll、pitch 和 heading 均以角度表示，函数内部会转换为弧度。

    :param coord: 机体系下的坐标 [x_m, y_m, z_m]
    :param roll: 横滚角（角度）
    :param pitch: 俯仰角（角度）
    :param heading: 航向角（角度）
    :return: 世界坐标系下的点 (x_w, y_w, z_w)
    """
    # 将角度转换为弧度
    roll = np.radians(roll)
    pitch = np.radians(pitch)
    heading = np.radians(heading)

    # 旋转矩阵 R_roll 对应 roll 角，绕 Y 轴旋转
    R_roll = np.array([
        [np.cos(roll), 0, np.sin(roll)],
        [0, 1, 0],
        [-np.sin(roll), 0, np.cos(roll)]
    ])

    # 旋转矩阵 R_pitch 对应 pitch 角，绕 X 轴旋转
    R_pitch = np.array([
        [1, 0, 0],
        [0, np.cos(pitch), -np.sin(pitch)],
        [0, np.sin(pitch), np.cos(pitch)]
    ])

    # 旋转矩阵 R_heading 对应 heading 角，绕 Z 轴旋转
    R_heading = np.array([
        [np.cos(heading), -np.sin(heading), 0],
        [np.sin(heading), np.cos(heading), 0],
        [0, 0, 1]
    ])

    # 合成总的旋转矩阵
    # 顺序为：先绕 Y 轴旋转，再绕 X 轴旋转，最后绕 Z 轴旋转
    # R = np.dot(R_heading, np.dot(R_pitch, R_roll))

    # 计算世界坐标系下的点
    # point_w = np.dot(R, coord)

    point_w = np.dot(R_pitch, coord)
    point_w = np.dot(R_heading, point_w)
    point_w = np.dot(R_roll, point_w)

    return point_w


def quaternion_to_vector(q, v):  # chatGPT
    """使用四元数 q 将向量 v 旋转到新的方向"""
    q_conjugate = np.array([q[0], -q[1], -q[2], -q[3]])  # 四元数共轭
    v_quat = np.array([0] + v.tolist())  # 将向量转换为四元数 (0, v)

    # 旋转公式：q * v * q^(-1)
    result = quaternion_multiply(quaternion_multiply(q, v_quat), q_conjugate)

    return result[1:]  # 取旋转后的向量部分


def quaternion_multiply(q1, q2):  # chatGPT
    """计算四元数乘积"""
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return np.array([
        w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
        w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
        w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
        w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
    ])


def rotation_matrix(heading):  # chatGPT
    """构建航向角（heading）的旋转矩阵"""
    heading_rad = np.radians(heading)  # 将航向角转换为弧度
    return np.array([
        [np.cos(heading_rad), -np.sin(heading_rad)],
        [np.sin(heading_rad), np.cos(heading_rad)]
    ])


def get_velocity_in_body_frame(vessel):  # chatGPT
    # 获取地面参考系下的速度 (单位：米/秒)
    velocity_surface = vessel.velocity(vessel.orbit.body.reference_frame)

    # 获取vessel的机体参考系方向（通过四元数）
    rotation = vessel.rotation(vessel.reference_frame)

    # 机体坐标系的x轴和y轴单位向量
    x_axis_body = np.array([1, 0, 0])  # 机体坐标系中的x轴
    y_axis_body = np.array([0, 1, 0])  # 机体坐标系中的y轴

    # 使用四元数将机体坐标系的x轴和z轴旋转到世界坐标系
    x_axis_world = quaternion_to_vector(rotation, x_axis_body)
    y_axis_world = quaternion_to_vector(rotation, y_axis_body)

    # 获取速度在地面参考系下的分量
    velocity_vector = np.array([velocity_surface[0], velocity_surface[1], velocity_surface[2]])

    # 计算速度在机体坐标系的x轴和z轴上的投影 (正交分解)
    velocity_x = np.dot(velocity_vector, x_axis_world)  # 速度在x轴上的分量
    velocity_y = np.dot(velocity_vector, y_axis_world)  # 速度在y轴上的分量

    # 获取航向角（以地面参考系为基准）
    heading = vessel.flight(vessel.orbit.body.reference_frame).heading

    # 使用航向角旋转速度分量到机体坐标系
    rotation_mat = rotation_matrix(heading)

    # 将速度分量 [velocity_x, velocity_y] 转换到机体坐标系
    velocity_body = np.dot(rotation_mat, np.array([velocity_x, velocity_y]))

    # 返回旋转后的速度分量
    velocity_body_x, velocity_body_y = velocity_body
    return velocity_body_x, velocity_body_y
