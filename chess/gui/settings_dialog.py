from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QComboBox, QSpinBox, QCheckBox,
                           QGroupBox)
from PyQt6.QtCore import Qt
from typing import Dict, Any

class SettingsDialog(QDialog):
    def __init__(self, parent=None, current_settings=None):
        super().__init__(parent)
        self.setWindowTitle("游戏设置")
        self.setModal(True)
        
        # 初始化设置
        self.current_settings = current_settings or {}
        
        # 创建布局
        layout = QVBoxLayout(self)
        
        # 添加设置组
        layout.addWidget(self._create_board_settings())
        layout.addWidget(self._create_piece_settings())
        layout.addWidget(self._create_sound_settings())
        
        # 添加按钮
        button_layout = QHBoxLayout()
        save_button = QPushButton("保存")
        cancel_button = QPushButton("取消")
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        # 连接信号
        save_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

    def _create_board_settings(self):
        """创建棋盘设置组"""
        group = QGroupBox("棋盘设置")
        layout = QVBoxLayout(group)
        
        # 棋盘主题
        theme_layout = QHBoxLayout()
        theme_label = QLabel("棋盘主题：")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["经典", "现代", "简约"])
        self.theme_combo.setCurrentText(
            self.current_settings.get('board_theme', "经典")
        )
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        layout.addLayout(theme_layout)
        
        return group

    def _create_piece_settings(self):
        """创建棋子设置组"""
        group = QGroupBox("棋子设置")
        layout = QVBoxLayout(group)
        
        # 棋子大小
        size_layout = QHBoxLayout()
        size_label = QLabel("棋子大小：")
        self.size_spin = QSpinBox()
        self.size_spin.setRange(40, 80)
        self.size_spin.setSingleStep(5)
        self.size_spin.setValue(
            self.current_settings.get('piece_size', 50)
        )
        size_layout.addWidget(size_label)
        size_layout.addWidget(self.size_spin)
        layout.addLayout(size_layout)
        
        return group

    def _create_sound_settings(self):
        """创建音效设置组"""
        group = QGroupBox("音效设置")
        layout = QVBoxLayout(group)
        
        # 音效开关
        self.sound_check = QCheckBox("启用音效")
        self.sound_check.setChecked(
            self.current_settings.get('sound_enabled', False)
        )
        layout.addWidget(self.sound_check)
        
        return group

    def get_settings(self) -> Dict[str, Any]:
        """获取设置值"""
        return {
            'board_theme': self.theme_combo.currentText(),
            'piece_size': self.size_spin.value(),
            'sound_enabled': self.sound_check.isChecked()
        } 