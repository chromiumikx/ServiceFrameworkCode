# API文档

## 简要说明：
> 本项目提供手势操作的基本组件，包括从传感器、控制芯片、蓝牙收发模块的硬件部分和控制、收发、识别、连接等软件部分。
## API列表：
>getGesture:获取当前手势，无手势或未知手势返回None

>getAccs:获取三个加速度数据

>getRots:获取三个角速度数据

>get6Motions:获取六轴传感器的六个数据

>连接和断开

## 系统架构：
### train:

>>1.standard data collect and mark

>>2.nural network trainning

>>3.save and get the nets after train and before use it

### for use:

>>hardwear

>>>1.sensor

>>>2.control chip

>>>3.bluetooth

>>softwear

>>>1.control chip codes

>>>2.judge validity and read the COM

>>>3.analysis data from COM

>>>4.read nets(weights)

>>>5.recognition by nural network

>>>6.show system information by tk

>>>7.data communication by socket

>>>8.real-timeing by threading module

>>>9.quit the service safely
