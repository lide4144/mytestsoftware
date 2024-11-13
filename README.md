# 中国象棋

这是一个使用PyQt6开发的中国象棋游戏。

## 功能特点

- 完整的中国象棋规则实现
- 图形化界面，美观易用
- 支持存档和读档功能
- 支持悔棋功能
- 将军和将死提示
- 可选择棋盘主题
- 走子提示功能

## 系统要求

- Python 3.6+
- PyQt6

## 安装依赖

pip install PyQt6


## 运行方法

python run.py


## 游戏规则

1. 红方先行,双方轮流走子
2. 点击己方棋子选中,再点击目标位置移动
3. 被将军时需要应将,否则判负
4. 无子可走时判负

## 项目结构

text
chess/
├── gui/ # 图形界面相关代码
│ ├── main_window.py # 主窗口
│ └── board_view.py # 棋盘视图
├── pieces/ # 棋子相关代码
│ └── specific_pieces.py # 具体棋子类实现
├── board.py # 棋盘逻辑
├── piece.py # 棋子基类
└── main.py # 程序入口

## 主要类说明

### Board
棋盘类,负责:
- 存储棋子位置
- 处理移动验证
- 检查将军和将死
- 存档和读档

### BoardView  
棋盘视图类,负责:
- 绘制棋盘和棋子
- 处理鼠标事件
- 显示走子提示
- 动画效果

### Piece
棋子基类,定义:
- 位置信息
- 颜色属性
- 移动规则接口

### MainWindow
主窗口类,包含:
- 菜单栏
- 状态栏
- 工具栏
- 对局信息显示

## 开发说明

项目使用了以下设计模式:
- MVC模式分离界面和逻辑
- 策略模式实现不同棋子的走法
- 观察者模式处理游戏状态更新
- 命令模式实现悔棋功能

## 贡献

欢迎提交Issue和Pull Request。

## 许可证

MIT License

主要代码引用:

import sys
from PyQt6.QtWidgets import QApplication
from .gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

class Board:
    def __init__(self):
        self.pieces: List[Piece] = []
        self.move_history = []  # 添加移动历史记录
        self.initialize_board()