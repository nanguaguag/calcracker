# CALCracker

#### 介绍
fx991cnx刷机

uEase正放PINOUT

14   13

NC   3V3

NC   NC

NC   NC

NC   SDA

NC   SCK

NC   NC

GND  VREF

2    1

fx991cnx:

    P172:GND

    P154:VCC

    P152:SDA

    P151:SCK 


fx991cnx     uEase             RP2040

GND       -   GND          -    GND

VCC       -   3V3, VREF    -    3V3

SDA       -   SDA          -    GP1

SCK       -   SCK          -    GP0


我的Gitee仓库(Calcracker)里有两个micropython文件(PIO.py, PIO_slave.py)，把他们下载下来。

然后要用到uEASE, 991cnx, rp2040（记得安装上mpy固件）

计算器 rp2040 uease

VCC　　—　3v3　— 　VREF

GND　　— 　GND　—　GND

SDA　　—　GP2

SCK　　—　GP3

　　　　　　GP1　—　SDA

　　　　　　GP0　—　SCK

首先把ML620Q418.TRG替换为我仓库里的trg文件

Thonny里运行PIO_slave.py，然后打开MWU FLASH16

Target选ML620Q418，点plug

此时能看到mpy脚本报了一个Out of bound，不用管它

运行PIO.py，看到“ID(10 * 4hex):”后

关键步骤：

1.把991cnx连到rp2040的线拔掉

2.把rp2040连到uease的线拔掉

3.把991cnx的线连到uease上

然后就可以操作了