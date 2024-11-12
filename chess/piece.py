from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple

class PieceColor(Enum):
    RED = "红"
    BLACK = "黑"

class PieceType(Enum):
    KING = "帅将"
    ADVISOR = "士"
    ELEPHANT = "相象"
    HORSE = "马"
    CHARIOT = "车"
    CANNON = "炮"
    PAWN = "兵卒"

@dataclass
class Position:
    x: int  # 0-8
    y: int  # 0-9

class Piece:
    def __init__(self, color: PieceColor, piece_type: PieceType, position: Position):
        self.color = color
        self.piece_type = piece_type
        self.position = position
        
    @property
    def name(self) -> str:
        """返回棋子的中文名称"""
        if self.color == PieceColor.RED:
            names = {
                PieceType.KING: "帅",
                PieceType.ADVISOR: "仕",
                PieceType.ELEPHANT: "相",
                PieceType.HORSE: "马",
                PieceType.CHARIOT: "车",
                PieceType.CANNON: "炮",
                PieceType.PAWN: "兵"
            }
        else:
            names = {
                PieceType.KING: "将",
                PieceType.ADVISOR: "士",
                PieceType.ELEPHANT: "象",
                PieceType.HORSE: "马",
                PieceType.CHARIOT: "车",
                PieceType.CANNON: "炮",
                PieceType.PAWN: "卒"
            }
        return names[self.piece_type]

    def get_possible_moves(self, board) -> List[Position]:
        """获取所有可能的移动位置，需要在子类中实现"""
        raise NotImplementedError