from typing import Optional, List, Tuple, Dict, Any
from .piece import Piece, Position, PieceColor, PieceType
from .pieces.specific_pieces import King, Advisor, Elephant, Horse, Chariot, Cannon, Pawn
import json

class Board:
    def __init__(self):
        self.pieces: List[Piece] = []
        self.move_history = []  # 添加移动历史记录
        self.initialize_board()
    
    def initialize_board(self):
        """初始化棋盘，放置所有棋子"""
        # 清空棋盘和历史记录
        self.pieces.clear()
        self.move_history.clear()
        
        # 放置红方棋子
        self.pieces.extend([
            King(PieceColor.RED, Position(4, 0)),
            Advisor(PieceColor.RED, Position(3, 0)),
            Advisor(PieceColor.RED, Position(5, 0)),
            Elephant(PieceColor.RED, Position(2, 0)),
            Elephant(PieceColor.RED, Position(6, 0)),
            Horse(PieceColor.RED, Position(1, 0)),
            Horse(PieceColor.RED, Position(7, 0)),
            Chariot(PieceColor.RED, Position(0, 0)),
            Chariot(PieceColor.RED, Position(8, 0)),
            Cannon(PieceColor.RED, Position(1, 2)),
            Cannon(PieceColor.RED, Position(7, 2)),
            Pawn(PieceColor.RED, Position(0, 3)),
            Pawn(PieceColor.RED, Position(2, 3)),
            Pawn(PieceColor.RED, Position(4, 3)),
            Pawn(PieceColor.RED, Position(6, 3)),
            Pawn(PieceColor.RED, Position(8, 3)),
        ])
        
        # 放置黑方棋子
        self.pieces.extend([
            King(PieceColor.BLACK, Position(4, 9)),
            Advisor(PieceColor.BLACK, Position(3, 9)),
            Advisor(PieceColor.BLACK, Position(5, 9)),
            Elephant(PieceColor.BLACK, Position(2, 9)),
            Elephant(PieceColor.BLACK, Position(6, 9)),
            Horse(PieceColor.BLACK, Position(1, 9)),
            Horse(PieceColor.BLACK, Position(7, 9)),
            Chariot(PieceColor.BLACK, Position(0, 9)),
            Chariot(PieceColor.BLACK, Position(8, 9)),
            Cannon(PieceColor.BLACK, Position(1, 7)),
            Cannon(PieceColor.BLACK, Position(7, 7)),
            Pawn(PieceColor.BLACK, Position(0, 6)),
            Pawn(PieceColor.BLACK, Position(2, 6)),
            Pawn(PieceColor.BLACK, Position(4, 6)),
            Pawn(PieceColor.BLACK, Position(6, 6)),
            Pawn(PieceColor.BLACK, Position(8, 6)),
        ])

    def get_king(self, color: PieceColor) -> Optional[King]:
        """获取指定颜色的将/帅"""
        for piece in self.pieces:
            if isinstance(piece, King) and piece.color == color:
                return piece
        return None

    def is_check(self, color: PieceColor) -> bool:
        """检查指定颜色的将/帅是否被将军"""
        king = self.get_king(color)
        if not king:
            return False
        
        # 检查所有对方棋子是否可以吃到将/帅
        for piece in self.pieces:
            if piece.color != color:  # 对方棋子
                if king.position in piece.get_possible_moves(self):
                    return True
        return False

    def is_checkmate(self, color: PieceColor) -> bool:
        """检查指定颜色是否被将死"""
        if not self.is_check(color):
            return False
        
        # 获取该方所有棋子
        pieces = [p for p in self.pieces if p.color == color]
        
        # 尝试每个棋子的每个可能移动
        for piece in pieces:
            original_pos = piece.position
            possible_moves = piece.get_possible_moves(self)
            
            for move in possible_moves:
                # 尝试移动
                captured_piece = None
                target_piece = self.get_piece_at(move)
                if target_piece:
                    self.pieces.remove(target_piece)
                    captured_piece = target_piece
                
                piece.position = move
                
                # 检查移动后是否仍被将军
                still_in_check = self.is_check(color)
                
                # 恢复位置
                piece.position = original_pos
                if captured_piece:
                    self.pieces.append(captured_piece)
                
                # 如果有一种移动可以解除将军，则未被将死
                if not still_in_check:
                    return False
        
        # 所有移动都无法解除将军，则被将死
        return True

    def get_piece_at(self, position: Position) -> Optional[Piece]:
        """获取指定位置的棋子"""
        for piece in self.pieces:
            if piece.position.x == position.x and piece.position.y == position.y:
                return piece
        return None

    def move_piece(self, from_pos: Position, to_pos: Position) -> Tuple[bool, str]:
        """移动棋子，返回(是否成功移动, 提示信息)"""
        piece = self.get_piece_at(from_pos)
        if not piece:
            return False, "没有找到棋子"
            
        # 检查目标位置是否有己方棋子
        target_piece = self.get_piece_at(to_pos)
        if target_piece and target_piece.color == piece.color:
            return False, "不能吃掉己方棋子"
            
        # 检查移动是否合法
        if to_pos not in piece.get_possible_moves(self):
            return False, "不符合走子规则"
        
        # 尝试移动
        original_pos = Position(piece.position.x, piece.position.y)  # 创建位置的副本
        original_target = target_piece
        if target_piece:
            self.pieces.remove(target_piece)
        piece.position = Position(to_pos.x, to_pos.y)  # 创建新的位置对象
        
        # 检查移动后是否会导致己方被将军
        if self.is_check(piece.color):
            # 恢复移动
            piece.position = original_pos
            if original_target:
                self.pieces.append(original_target)
            return False, "此移动会导致被将军"
        
        # 记录移动历史
        self.move_history.append({
            'piece': piece,
            'from_pos': original_pos,
            'to_pos': Position(to_pos.x, to_pos.y),  # 创建位置的副本
            'captured_piece': original_target
        })
        
        # 检查是否将军对方
        opponent_color = PieceColor.BLACK if piece.color == PieceColor.RED else PieceColor.RED
        if self.is_check(opponent_color):
            if self.is_checkmate(opponent_color):
                return True, "将死！游戏结束"
            return True, "将军！"
        
        return True, ""

    def undo_last_move(self) -> bool:
        """撤销最后一步移动"""
        if not self.move_history:
            return False
        
        # 获取最后一步移动的记录
        last_move = self.move_history.pop()
        
        # 恢复棋子位置
        piece = last_move['piece']
        piece.position = Position(last_move['from_pos'].x, last_move['from_pos'].y)  # 创建新的位置对象
        
        # 如果有被吃掉的棋子，将其放回
        if last_move['captured_piece']:
            captured_piece = last_move['captured_piece']
            # 确保被吃掉的棋子不在棋盘上
            if captured_piece not in self.pieces:
                self.pieces.append(captured_piece)
        
        return True

    def restart_game(self):
        """重新开始游戏"""
        self.initialize_board()

    def to_dict(self) -> Dict[str, Any]:
        """将棋盘状态转换为字典"""
        return {
            'pieces': [
                {
                    'type': piece.__class__.__name__,
                    'color': piece.color.name,
                    'position': {'x': piece.position.x, 'y': piece.position.y}
                }
                for piece in self.pieces
            ]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Board':
        """从字典创建棋盘状态"""
        from .pieces.specific_pieces import (
            King, Advisor, Elephant, Horse, Chariot, Cannon, Pawn
        )
        
        piece_classes = {
            'King': King,
            'Advisor': Advisor,
            'Elephant': Elephant,
            'Horse': Horse,
            'Chariot': Chariot,
            'Cannon': Cannon,
            'Pawn': Pawn
        }
        
        board = cls()
        board.pieces.clear()  # 清空当前棋子
        
        for piece_data in data['pieces']:
            piece_class = piece_classes[piece_data['type']]
            color = PieceColor[piece_data['color']]
            position = Position(
                piece_data['position']['x'],
                piece_data['position']['y']
            )
            board.pieces.append(piece_class(color, position))
        
        return board