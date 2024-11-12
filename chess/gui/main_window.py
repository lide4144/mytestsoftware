from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QPushButton, QMessageBox,
                           QFileDialog, QDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from .board_view import BoardView
from ..piece import PieceColor
import json
from typing import Dict, Any
from .settings_dialog import SettingsDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("中国象棋")
        self.setMinimumSize(800, 1000)  # 增加高度以容纳状态栏
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        layout = QVBoxLayout(central_widget)
        
        # 创建状态栏
        self.status_bar = self._create_status_bar()
        layout.addWidget(self.status_bar)
        
        # 创建并添加棋盘视图
        self.board_view = BoardView()
        layout.addWidget(self.board_view, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # 连接信号
        self.board_view.game_state_changed.connect(self.update_status)
        
        # 初化状态显示
        self.update_status()
        
        # 添加设置
        self.settings = {
            'board_theme': "经典",
            'piece_size': 50,
            'sound_enabled': False
        }

    def _create_status_bar(self):
        """创建状态栏"""
        status_widget = QWidget()
        status_layout = QHBoxLayout(status_widget)
        
        # 设置状态栏样式
        status_widget.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QLabel {
                font-size: 16px;
                padding: 5px;
            }
            QPushButton {
                font-size: 14px;
                padding: 5px 10px;
                background-color: #e0e0e0;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        
        # 创建标签
        self.turn_label = QLabel()
        self.turn_label.setFont(QFont("楷体", 16))
        status_layout.addWidget(self.turn_label)
        
        self.check_label = QLabel()
        self.check_label.setFont(QFont("楷体", 16))
        self.check_label.setStyleSheet("color: red;")
        status_layout.addWidget(self.check_label)
        
        # 添加弹性空间
        status_layout.addStretch()
        
        # 添加按钮
        restart_button = QPushButton("重新开始")
        restart_button.clicked.connect(self.restart_game)
        status_layout.addWidget(restart_button)
        
        undo_button = QPushButton("悔棋")
        undo_button.clicked.connect(self.undo_move)
        status_layout.addWidget(undo_button)
        
        # 添加存档按钮
        save_button = QPushButton("保存游戏")
        save_button.clicked.connect(self.save_game)
        status_layout.addWidget(save_button)
        
        # 添加读档按钮
        load_button = QPushButton("读取游戏")
        load_button.clicked.connect(self.load_game)
        status_layout.addWidget(load_button)
        
        # 添加设置按钮
        settings_button = QPushButton("设置")
        settings_button.clicked.connect(self.show_settings)
        status_layout.addWidget(settings_button)
        
        # 设置布局边距
        status_layout.setContentsMargins(10, 5, 10, 5)
        
        return status_widget

    def update_status(self):
        """更新状态显示"""
        # 更新当前回合显示
        current_player = "红方" if self.board_view.current_player == PieceColor.RED else "黑方"
        self.turn_label.setText(f"当前回合：{current_player}")
        
        # 更新将军状态
        if self.board_view.board.is_check(self.board_view.current_player):
            self.check_label.setText("将军！")
        else:
            self.check_label.setText("")
            
        # 如果游戏结束
        if hasattr(self.board_view, 'game_over') and self.board_view.game_over:
            winner = "红方" if self.board_view.current_player == PieceColor.BLACK else "黑方"
            self.turn_label.setText(f"游戏结束 - {winner}胜！")

    def restart_game(self):
        """重新开始游戏"""
        self.board_view.board.initialize_board()
        self.board_view.current_player = PieceColor.RED
        self.board_view.selected_piece = None
        self.board_view.selected_pos = None
        self.board_view.game_over = False
        self.board_view.update()
        self.update_status()

    def undo_move(self):
        """悔棋功能"""
        if not self.board_view.undo_move():
            QMessageBox.information(self, "提示", "无法悔棋")

    def save_game(self):
        """保存游戏"""
        if self.board_view.game_over:
            QMessageBox.information(self, "提示", "游戏已结束，无法保存")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存游戏",
            "",
            "象棋存档 (*.chess);;所有文件 (*.*)"
        )
        
        if file_path:
            try:
                # 获取游戏状态
                state = self.board_view.save_state()
                
                # 保存到文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(state, f, ensure_ascii=False, indent=2)
                
                QMessageBox.information(self, "提示", "游戏保存成功")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"保存游戏失败：{str(e)}")

    def load_game(self):
        """读取游戏"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "读取游戏",
            "",
            "象棋存档 (*.chess);;所有文件 (*.*)"
        )
        
        if file_path:
            try:
                # 从文件读取状态
                with open(file_path, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                
                # 加载游戏状态
                self.board_view.load_state(state)
                QMessageBox.information(self, "提示", "游戏读取成功")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"读取游戏失败：{str(e)}")

    def show_settings(self):
        """显示设置对话框"""
        dialog = SettingsDialog(self, self.settings)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # 获取新的设置
            new_settings = dialog.get_settings()
            
            # 应用设置
            self.apply_settings(new_settings)
            
            # 保存设置
            self.settings = new_settings

    def apply_settings(self, settings: Dict[str, Any]):
        """应用设置"""
        # 更新棋子大小
        if settings['piece_size'] != self.settings['piece_size']:
            self.board_view.piece_size = settings['piece_size']
            self.board_view.update()
        
        # 更新棋盘主题
        if settings['board_theme'] != self.settings['board_theme']:
            self._apply_theme(settings['board_theme'])
        
        # 更新音效设置
        if settings['sound_enabled'] != self.settings['sound_enabled']:
            # TODO: 实现音效控制
            pass

    def _apply_theme(self, theme: str):
        """应用棋盘主题"""
        themes = {
            "经典": {
                'background': '#f0f0f0',
                'border': '#ccc',
                'red_piece': '#c00',
                'black_piece': '#000',
                'red_bg': '#ffe6e6',
                'black_bg': '#e6e6e6'
            },
            "现代": {
                'background': '#e8e8e8',
                'border': '#999',
                'red_piece': '#d00',
                'black_piece': '#222',
                'red_bg': '#ffd9d9',
                'black_bg': '#d9d9d9'
            },
            "简约": {
                'background': '#fff',
                'border': '#666',
                'red_piece': '#f00',
                'black_piece': '#333',
                'red_bg': '#fff',
                'black_bg': '#f9f9f9'
            }
        }
        
        theme_colors = themes.get(theme, themes["经典"])
        
        # 更新状态栏样式
        self.status_bar.setStyleSheet(f"""
            QWidget {{
                background-color: {theme_colors['background']};
                border: 1px solid {theme_colors['border']};
                border-radius: 5px;
            }}
            QLabel {{
                font-size: 16px;
                padding: 5px;
            }}
            QPushButton {{
                font-size: 14px;
                padding: 5px 10px;
                background-color: {theme_colors['background']};
                border: 1px solid {theme_colors['border']};
                border-radius: 3px;
            }}
            QPushButton:hover {{
                background-color: {theme_colors['black_bg']};
            }}
        """)
        
        # 更新棋盘视图的颜色
        self.board_view.update_theme(theme_colors)