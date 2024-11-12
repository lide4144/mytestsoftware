from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import Qt, QRect, QPoint, pyqtSignal
from PyQt6.QtGui import QPainter, QPen, QColor, QFont, QBrush
from ..board import Board
from ..piece import PieceColor, Position
from typing import Dict, Any

class BoardView(QWidget):
    # 添加信号
    game_state_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.cell_size = 60  # 每个格子的大小
        self.margin = 40     # 边距
        self.piece_size = 50  # 棋子的大小
        
        # 计算棋盘大小
        self.board_width = 9 * self.cell_size
        self.board_height = 10 * self.cell_size
        
        # 设置固定大小
        self.setFixedSize(
            self.board_width + 2 * self.margin,
            self.board_height + 2 * self.margin
        )
        
        # 创建棋盘模型
        self.board = Board()
        
        # 设置棋子字体
        self.piece_font = QFont("楷体", 24, QFont.Weight.Bold)
        
        # 添加新的成员变量
        self.selected_piece = None  # 当前选中的棋子
        self.current_player = PieceColor.RED  # 当前回合的玩家
        self.selected_pos = None  # 选中的位置
        self.game_over = False
        
        # 设置鼠标追踪
        self.setMouseTracking(True)
        
        # 添加主题颜色
        self.theme_colors = {
            'background': '#f0f0f0',
            'border': '#ccc',
            'red_piece': '#c00',
            'black_piece': '#000',
            'red_bg': '#ffe6e6',
            'black_bg': '#e6e6e6'
        }

    def mousePressEvent(self, event):
        """处理鼠标点击事件"""
        if event.button() == Qt.MouseButton.LeftButton and not self.game_over:
            pos = self._pixel_to_board_pos(event.position())
            if pos is None:
                return
            
            clicked_piece = self.board.get_piece_at(pos)
            
            if self.selected_piece:
                if self.selected_pos == pos:
                    self.selected_piece = None
                    self.selected_pos = None
                    self.game_state_changed.emit()
                else:
                    if pos in self.selected_piece.get_possible_moves(self.board):
                        success, message = self.board.move_piece(self.selected_pos, pos)
                        if success:
                            self.current_player = (PieceColor.BLACK 
                                if self.current_player == PieceColor.RED 
                                else PieceColor.RED)
                            if message:
                                QMessageBox.information(self, "提示", message)
                                if "将死" in message:
                                    self.game_over = True
                            self.game_state_changed.emit()
                    
                    self.selected_piece = None
                    self.selected_pos = None
            
            elif clicked_piece and clicked_piece.color == self.current_player:
                self.selected_piece = clicked_piece
                self.selected_pos = pos
                self.game_state_changed.emit()
            
            self.update()

    def _pixel_to_board_pos(self, point: QPoint) -> Position:
        """将像素坐标转换为棋盘坐标"""
        x = round((point.x() - self.margin) / self.cell_size)
        y = round((point.y() - self.margin) / self.cell_size)
        
        if 0 <= x <= 8 and 0 <= y <= 9:
            return Position(x, y)
        return None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        self._draw_board(painter)
        
        if self.selected_piece:
            self._draw_selected_highlight(painter)
            self._draw_possible_moves(painter)
        
        self._draw_pieces(painter)
        
        if not self.game_over and self.board.is_check(self.current_player):
            self._draw_check_indicator(painter)

    def _draw_board(self, painter):
        """绘制棋盘"""
        # 设置画笔
        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(2)
        painter.setPen(pen)
        
        # 绘制外框
        painter.drawRect(
            self.margin,
            self.margin,
            self.board_width,
            self.board_height
        )
        
        # 绘制横线
        for i in range(10):
            y = self.margin + i * self.cell_size
            painter.drawLine(
                self.margin,
                y,
                self.margin + self.board_width,
                y
            )
        
        # 绘制竖线
        for i in range(9):
            x = self.margin + i * self.cell_size
            # 上半部分
            painter.drawLine(
                x,
                self.margin,
                x,
                self.margin + self.cell_size * 4
            )
            # 下半部分
            painter.drawLine(
                x,
                self.margin + self.cell_size * 5,
                x,
                self.margin + self.board_height
            )
            
        # 绘制"楚河汉界"
        painter.drawText(
            QRect(
                self.margin + self.cell_size * 2,
                self.margin + self.cell_size * 4,
                self.cell_size * 5,
                self.cell_size
            ),
            Qt.AlignmentFlag.AlignCenter,
            "楚河                 汉界"
        )
        
        # 绘制九宫格斜线
        # 上方九宫格
        painter.drawLine(
            self.margin + 3 * self.cell_size,
            self.margin,
            self.margin + 5 * self.cell_size,
            self.margin + 2 * self.cell_size
        )
        painter.drawLine(
            self.margin + 5 * self.cell_size,
            self.margin,
            self.margin + 3 * self.cell_size,
            self.margin + 2 * self.cell_size
        )
        
        # 下方九宫格
        painter.drawLine(
            self.margin + 3 * self.cell_size,
            self.margin + 7 * self.cell_size,
            self.margin + 5 * self.cell_size,
            self.margin + 9 * self.cell_size
        )
        painter.drawLine(
            self.margin + 5 * self.cell_size,
            self.margin + 7 * self.cell_size,
            self.margin + 3 * self.cell_size,
            self.margin + 9 * self.cell_size
        )

    def _draw_pieces(self, painter):
        """绘制棋子"""
        painter.setFont(self.piece_font)
        
        for piece in self.board.pieces:
            # 计算棋子的中心位置
            center_x = self.margin + piece.position.x * self.cell_size
            center_y = self.margin + piece.position.y * self.cell_size
            
            # 计算棋子的外框矩形
            piece_rect = QRect(
                center_x - self.piece_size // 2,
                center_y - self.piece_size // 2,
                self.piece_size,
                self.piece_size
            )
            
            # 设置棋子颜色（使用主题颜色）
            if piece.color == PieceColor.RED:
                text_color = QColor(self.theme_colors['red_piece'])
                bg_color = QColor(self.theme_colors['red_bg'])
            else:
                text_color = QColor(self.theme_colors['black_piece'])
                bg_color = QColor(self.theme_colors['black_bg'])
            
            # 绘制棋子背景（圆形）
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(bg_color))
            painter.drawEllipse(piece_rect)
            
            # 绘制棋子边框
            painter.setPen(QPen(QColor(0, 0, 0), 2))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(piece_rect)
            
            # 绘制棋子文字
            painter.setPen(QPen(text_color))
            painter.drawText(
                piece_rect,
                Qt.AlignmentFlag.AlignCenter,
                piece.name
            )

    def _draw_selected_highlight(self, painter):
        """绘制选中棋子的高亮效果"""
        if not self.selected_piece:
            return
            
        # 计算选中棋子的中心位置
        center_x = self.margin + self.selected_piece.position.x * self.cell_size
        center_y = self.margin + self.selected_piece.position.y * self.cell_size
        
        # 绘制高亮框
        highlight_rect = QRect(
            center_x - self.piece_size // 2 - 2,
            center_y - self.piece_size // 2 - 2,
            self.piece_size + 4,
            self.piece_size + 4
        )
        
        painter.setPen(QPen(QColor(255, 0, 0), 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(highlight_rect)

    def _draw_possible_moves(self, painter):
        """绘制可能的移动位置"""
        if not self.selected_piece:
            return
            
        # 获取可能的移动位置
        possible_moves = self.selected_piece.get_possible_moves(self.board)
        
        # 设置画笔
        painter.setPen(QPen(QColor(0, 255, 0), 2))
        painter.setBrush(QBrush(QColor(0, 255, 0, 50)))
        
        # 绘制每个可能的移动位置
        for pos in possible_moves:
            center_x = self.margin + pos.x * self.cell_size
            center_y = self.margin + pos.y * self.cell_size
            
            # 绘制小圆点
            painter.drawEllipse(
                center_x - 5,
                center_y - 5,
                10,
                10
            )

    def _draw_check_indicator(self, painter):
        """绘制将军提示"""
        king = self.board.get_king(self.current_player)
        if not king:
            return
            
        # 计算将/帅的位置
        center_x = self.margin + king.position.x * self.cell_size
        center_y = self.margin + king.position.y * self.cell_size
        
        # 绘制红色警告框
        warning_rect = QRect(
            center_x - self.piece_size // 2 - 4,
            center_y - self.piece_size // 2 - 4,
            self.piece_size + 8,
            self.piece_size + 8
        )
        
        painter.setPen(QPen(QColor(255, 0, 0), 3))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(warning_rect)

    def undo_move(self) -> bool:
        """执行悔棋操作"""
        if self.game_over:
            return False
            
        if self.board.undo_last_move():
            # 切换回上一个玩家
            self.current_player = (PieceColor.BLACK 
                if self.current_player == PieceColor.RED 
                else PieceColor.RED)
            
            # 清除选中状态
            self.selected_piece = None
            self.selected_pos = None
            
            # 重绘棋盘
            self.update()
            self.game_state_changed.emit()
            return True
            
        return False

    def save_state(self) -> Dict[str, Any]:
        """保存游戏状态"""
        return {
            'board': self.board.to_dict(),
            'current_player': self.current_player.name,
            'game_over': self.game_over
        }

    def load_state(self, state: Dict[str, Any]):
        """加载游戏状态"""
        self.board = Board.from_dict(state['board'])
        self.current_player = PieceColor[state['current_player']]
        self.game_over = state['game_over']
        self.selected_piece = None
        self.selected_pos = None
        self.update()
        self.game_state_changed.emit()

    def update_theme(self, colors: Dict[str, str]):
        """更新主题颜色"""
        self.theme_colors = colors
        self.update()