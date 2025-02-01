import sys
import krpc
import simple_pid
import numpy as np

import pyqtgraph.opengl as gl
from PySide6 import QtTest
from PySide6.QtCore import QThread
from PySide6.QtWidgets import QApplication, QWidget

from ui_form import Ui_Widget
import pacifier.settings as settings
import pacifier.supportFuncs as supportFuncs


class ExteriorThread(QThread):
    def __init__(self, main):
        super(ExteriorThread, self).__init__()
        self.main = main

    def run(self) -> None:
        while True:
            self.main.tick()
            QtTest.QTest.qWait(50)


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())

        # widget signal connection
        self.ui.pushButton_start.clicked.connect(self.btn_start)
        self.ui.pushButton_stop.clicked.connect(self.btn_stop)
        self.ui.pushButton_forward.pressed.connect(self.btn_forward_press)
        self.ui.pushButton_back.pressed.connect(self.btn_back_press)
        self.ui.pushButton_forward.released.connect(self.btn_forward_release)
        self.ui.pushButton_back.released.connect(self.btn_back_release)
        self.ui.pushButton_stopVessel.released.connect(self.btn_stop_vessel)

        # graph part
        self.exteriorThread = ExteriorThread(self)
        self.orientationGraph = gl.GLViewWidget()

        self.orientationGraph.opts['distance'] = 10  # init
        gl_axis = gl.GLAxisItem()  # add xyz axis
        gl_axis.glOptions = 'opaque'
        gl_axis.setSize(20, 20, 30)

        gl_grid = gl.GLGridItem()
        gl_grid.setSize(20, 20)
        gl_grid.setSpacing(1, 1)

        self.arrow = gl.GLLinePlotItem(pos=np.array([[0, 0, 0], [1, 1, 1]]), color=(1, 1, 0, 1), width=2)
        self.engPosCloud = gl.GLScatterPlotItem()
        self.engPosCloudProj = gl.GLScatterPlotItem()

        self.orientationGraph.addItem(gl_axis)
        self.orientationGraph.addItem(gl_grid)
        self.orientationGraph.addItem(self.arrow)
        self.orientationGraph.addItem(self.engPosCloud)
        self.orientationGraph.addItem(self.engPosCloudProj)

        self.ui.verticalLayout_orienMainGraph.addWidget(self.orientationGraph)
        self.conn = krpc.connect(name='pacifier')
        self.space_center = self.conn.space_center
        self.vessel = self.space_center.active_vessel

        self.engList: [list | None] = None
        self.motorList: [list | None] = []
        self.engPosList = None
        self.engRotList = None
        self.engNums = 0

        self.heightPid = simple_pid.PID(Kp=0.3, Ki=0.0001, Kd=0.6, differential_on_measurement=False, output_limits=(0.1, 0.8))
        self.headingPidWheel = supportFuncs.PIDUsingE(kp=0.8, ki=0.0, kd=1.5)
        self.headingPidEngine = supportFuncs.PIDUsingE(kp=1.0, ki=0.001, kd=3)
        self.pidControllerList = []
        for i in range(4):
            self.pidControllerList.append(simple_pid.PID(Kp=0.1, Kd=0.3, differential_on_measurement=False, output_limits=(-0.2, 0.2)))

        self.flyingMode = settings.FLYING_MODE_STOP
        self.flyingDirection = settings.FLYING_DIR_FORWARD

        # bind engines
        self.engList = self.vessel.parts.engines
        self.motorList = self.vessel.parts.robotic_rotations
        self.engNums = len(self.engList)
        for eng in self.engList:
            tag = eng.part.tag[1:]
            for motor in self.motorList:
                if motor.part.tag[1:] == tag:
                    self.motorList.append(motor)
                    break
        self.motor_lb = self.select_eng_or_rot("rot", "lb")
        self.motor_rb = self.select_eng_or_rot("rot", "rb")
        self.motor_lf = self.select_eng_or_rot("rot", "lf")
        self.motor_rf = self.select_eng_or_rot("rot", "rf")

        # graph
        self.sizeList = np.ndarray([self.engNums], dtype=float)
        self.colorList = np.ndarray([self.engNums, 4], dtype=float)
        self.colorListProj = np.ndarray([self.engNums, 4], dtype=float)
        for i in range(self.engNums):
            self.sizeList[i] = 0.3
            self.colorListProj[i] = np.array([0, 1, 0, 1])
        for i in range(self.engNums):
            if i == 0:
                self.colorList[i] = np.array([1, 0, 0, 1])  # 红
            elif i == 1:
                self.colorList[i] = np.array([0, 1, 1, 1])  # 浅蓝
            elif i == 2:
                self.colorList[i] = np.array([0, 0, 1, 1])  # 蓝
            else:
                self.colorList[i] = np.array([1, 0, 1, 1])  # 紫

    def reset_motors(self):
        for motor in self.motorList:
            motor.target_angle = 0

    def select_eng_or_rot(self, cate: str, label: str):
        if cate == "eng":
            for eng in self.engList:
                tag = eng.part.tag[1:]
                if tag == label:
                    return eng
        if cate == "rot":
            for motor in self.motorList:
                tag = motor.part.tag[1:]
                if tag == label:
                    return motor
        return None

    def tick(self) -> None:
        # show up vector
        upVec = supportFuncs.compute_up_vector(self.vessel.flight().pitch, self.vessel.flight().heading)
        self.ui.label_upVec_value.setText(supportFuncs.form_vec_description(upVec))
        self.arrow.setData(pos=np.array([np.array([0, 0, 0]), upVec]))

        # height control
        targetHeight = self.ui.horizontalSlider_height.value() * 0.01 * 200
        self.heightPid.setpoint = targetHeight
        self.ui.label_height_value.setText("current target:" + str(targetHeight)[0:5] + "m")
        self.vessel.control.throttle = self.heightPid(self.vessel.flight().surface_altitude)

        # heading control
        targetHeading = self.ui.horizontalSlider_heading.value() * 0.01 * 360
        self.ui.label_heading_value.setText("current heading:" + str(targetHeading)[0:5])
        deltaHeading = supportFuncs.compute_error_vector(self.vessel.flight().heading, targetHeading)
        headingMotorCtrl = 0
        if settings.HEADING_CONTROL == settings.HEADING_CONTROL_WHEEL:
            self.vessel.control.yaw = self.headingPidWheel(deltaHeading)
        elif settings.HEADING_CONTROL == settings.HEADING_CONTROL_ENGINE:
            headingMotorCtrl = 4 * self.headingPidEngine(deltaHeading)
        else:
            pass

        # engine thrust control
        self.engPosList = np.ndarray([self.engNums, 3], dtype=float)
        # self.engRotList = np.ndarray([self.engNums, 4], dtype=float)  # 先不考虑旋转问题（这是四元数表示的）

        r, p, h = self.vessel.flight().roll, self.vessel.flight().pitch, self.vessel.flight().heading
        for i in range(self.engNums):
            eng = self.engList[i]
            self.engPosList[i] = eng.part.position(self.vessel.reference_frame)
            # self.engRotList[i] = eng.part.rotation(self.vessel.reference_frame)
            self.engPosList[i] = supportFuncs.rotate_to_world(self.engPosList[i], r, p, h)
            surfPos = eng.part.position(self.vessel.surface_reference_frame)
            ctrl = self.pidControllerList[i](surfPos[0])  # dt暂时用电脑时间，游戏不卡
            eng.thrust_limit = 0.3 + ctrl

        self.engPosCloud.setData(pos=self.engPosList, size=self.sizeList, color=self.colorList, pxMode=False)
        proj = np.zeros([self.engNums, 3], dtype=float)
        proj[:, :2] = self.engPosList[:, :2]
        self.engPosCloudProj.setData(pos=proj, size=self.sizeList, color=self.colorListProj, pxMode=False)

        motor_lf_ctrl = - headingMotorCtrl
        motor_rf_ctrl = headingMotorCtrl
        if self.flyingMode == settings.FLYING_MODE_STOP:
            self.ui.label_currentMode.setText("current mode: stop")
            self.reset_motors()
            v_side, v_forward = supportFuncs.get_velocity_in_body_frame(self.vessel)
            b_side = np.tanh(v_side)
            b_forward = np.tanh(v_forward)
            # kill velocity in side direction
            targetBiasLF = b_side  # only for symmetry situation
            targetBiasRF = -b_side  # otherwise needs modification
            targetBiasLB = b_side
            targetBiasRB = -b_side
            # kill velocity in forward direction
            targetBiasLF -= b_forward
            targetBiasRF -= b_forward
            targetBiasLB += b_forward
            targetBiasRB += b_forward
            # add a bias on pid controller
            for i in range(self.engNums):
                eng = self.engList[i]
                tag = eng.part.tag[1:]
                if tag == "lf":
                    self.pidControllerList[i].setpoint = targetBiasLF
                if tag == "rf":
                    self.pidControllerList[i].setpoint = targetBiasRF
                if tag == "lb":
                    self.pidControllerList[i].setpoint = targetBiasLB
                if tag == "rb":
                    self.pidControllerList[i].setpoint = targetBiasRB
        elif self.flyingMode == settings.FLYING_MODE_MOVE:
            self.ui.label_currentMode.setText("current mode: move")
            for i in range(self.engNums):
                self.pidControllerList[i].setpoint = 0
            if self.flyingDirection == settings.FLYING_DIR_FORWARD:
                self.motor_lb.target_angle = -25
                self.motor_rb.target_angle = -25
                motor_lf_ctrl += -25
                motor_rf_ctrl += -25
            elif self.flyingDirection == settings.FLYING_DIR_BACK:
                self.motor_lb.target_angle = 25
                self.motor_rb.target_angle = 25
                motor_lf_ctrl += 25
                motor_rf_ctrl += 25
            else:
                pass
        elif self.flyingMode == settings.FLYING_MODE_STABLE:
            self.reset_motors()
            self.ui.label_currentMode.setText("current mode: stable")
        else:
            self.ui.label_currentMode.setText("current mode: unknown")
            pass
        if settings.HEADING_CONTROL == settings.HEADING_CONTROL_ENGINE:  # 前两个引擎既要负责heading控制也要参与前后移动，放最后统一计算
            self.motor_lf.target_angle = motor_lf_ctrl
            self.motor_rf.target_angle = motor_rf_ctrl

    def btn_forward_press(self):
        self.flyingMode = settings.FLYING_MODE_MOVE
        self.flyingDirection = settings.FLYING_DIR_FORWARD

    def btn_forward_release(self):
        self.flyingMode = settings.FLYING_MODE_STABLE

    def btn_back_press(self):
        self.flyingMode = settings.FLYING_MODE_MOVE
        self.flyingDirection = settings.FLYING_DIR_BACK

    def btn_back_release(self):
        self.flyingMode = settings.FLYING_MODE_STABLE

    def btn_stop_vessel(self):
        self.flyingMode = settings.FLYING_MODE_STOP

    def btn_start(self):
        self.exteriorThread.start()

    def btn_stop(self):
        self.exteriorThread.terminate()

    def closeEvent(self, event):
        if self.exteriorThread.isRunning():
            self.exteriorThread.terminate()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
