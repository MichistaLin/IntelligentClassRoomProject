# 教室智能照明系统

## 说明

该项目是哈尔滨工程大学嵌入式系统设计的综合实验，使用的工具如下：

- Proteus 8.10（最好使用8.10版本，至少不能比该版本低，否则打不开工程）
- Pycharm
- Arduino
- Python3.8
- Flask
- SQLite3
- SQLAlchemy-Flask

## 如何启动该项目

### 下位机

进入SmartRoom文件夹，双击FinalWork.pdsprj会自动使用Proteus打开该工程，在原理图中双击Arduino328芯片

![image-20231206145212410](.\README.assets\image-20231206145212410.png)

进入编辑元件，修改ProgramFile为SmartRoom文件夹下的firmware.elf，点击确定

![image-20231206145458555](.\README.assets\image-20231206145458555.png)

![image-20231206145543407](.\README.assets\image-20231206145543407.png)

最后点击左下角的运行按钮即可



### 上位机

使用pycharm打开IntelligentClassRoom文件夹，使用`pip install requirements`安装requirements.txt内的包，打开app.py，右键运行即可，数据库使用的是SQLite3，轻量轻便，它的数据就存在于`instance\sqlite3.db`中，如果这个文件没有丢失，那么你就不需要理会`数据迁移步骤.md`中的内容；如果它丢失了的话，那你就需要按照`数据迁移步骤.md`中的操作，把命令运行一遍以便进行数据迁移生成数据库。



## Erro：下位机的数据传不到上位机怎么办

极有可能是因为换了设备或者Proteus版本号不一致导致Proteus工程文件出了故障，你只需要在你的机器上新建一个Arduino328工程，把原理图里的元件拷贝到新工程里，然后Programfile仍然选择firmware.elf，在新工程里运行即可。

还不行的话，就在你的机器上新建一个Arduino328工程，把原理图里的元件拷贝到新工程里，然后把我们源代码复制到你的新工程的源代码中，运行即可。源代码由该同志提供 [yao9e](https://github.com/yao9e/HEUCSEmbedded)

![image-20231206151258903](.\README.assets\image-20231206151258903.png)

## 项目展示

后端控制台![image-20231206152117008](.\README.assets\image-20231206152117008.png)

前端页面

![image-20231206152223002](.\README.assets\image-20231206152223002.png)

![image-20231206152243314](.\README.assets\image-20231206152243314.png)

![image-20231206152312430](.\README.assets\image-20231206152312430.png)

每一个led卡片都是可点击的。

![image-20231206152415498](.\README.assets\image-20231206152415498.png)

总结：这个项目很简单，我们没有做很多功能，主要是练习上位机与下位机之间通过串口进行通信，以及下位机使用FreeRTOS进行多任务多线程处理。







