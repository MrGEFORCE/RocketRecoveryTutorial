
# 四轴矢量飞行器

具体看视频（[【KSP】四轴矢量飞行器](https://www.bilibili.com/video/BV1CaF6eVEJM/)）或自己游戏里打开看。该飞行器只有三个模式，前后平动、配平飞行和悬停，高度和方位实时被动控制，可以在界面上拉条子去修改。

### 使用注意事项

1.这是一个带PyQt的GUI工程，别忘了安装界面相关的库，具体看requirements

2.需要配合载具的name tag才能使用，以便更方便地寻找到对应方位的引擎和转轴

3.由于参数的原因，使用原本代码时必须配合上传的飞行器一同使用，否则需要自己调参，飞行器在上级目录的craft中，名为rocketDrone.craft

4.部分函数是chatGPT写的，已经在注释中标出，没去仔细看过具体的过程

### 想法起源

1.[红警3中的“平定者野战加农炮”](https://wiki.biligame.com/redalert3/%E5%B9%B3%E5%AE%9A%E8%80%85)

2.俄乌战场上的无人机

3.视频：[【KRPC】非对称推力配平](https://www.bilibili.com/video/BV1cjFDeNEUw/)

4.Mr.G自己存档中大量的这一构型飞船需要一个飞控
