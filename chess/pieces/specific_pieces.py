from typing import List
from ..piece import Piece, Position, PieceColor, PieceType

class King(Piece):
    def __init__(self, color: PieceColor, position: Position):
        super().__init__(color, PieceType.KING, position)
    
    def get_possible_moves(self, board) -> List[Position]:
        moves = []
        # 将帅只能在九宫格内移动
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            new_x = self.position.x + dx
            new_y = self.position.y + dy
            
            # 检查是否在九宫格内
            if self.color == PieceColor.RED:
                if 3 <= new_x <= 5 and 0 <= new_y <= 2:
                    moves.append(Position(new_x, new_y))
            else:
                if 3 <= new_x <= 5 and 7 <= new_y <= 9:
                    moves.append(Position(new_x, new_y))
        
        return moves

class Advisor(Piece):
    def __init__(self, color: PieceColor, position: Position):
        super().__init__(color, PieceType.ADVISOR, position)
    
    def get_possible_moves(self, board) -> List[Position]:
        moves = []
        # 士只能在九宫格内斜着走
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            new_x = self.position.x + dx
            new_y = self.position.y + dy
            
            # 检查是否在九宫格内
            if self.color == PieceColor.RED:
                if 3 <= new_x <= 5 and 0 <= new_y <= 2:
                    moves.append(Position(new_x, new_y))
            else:
                if 3 <= new_x <= 5 and 7 <= new_y <= 9:
                    moves.append(Position(new_x, new_y))
        
        return moves

class Elephant(Piece):
    def __init__(self, color: PieceColor, position: Position):
        super().__init__(color, PieceType.ELEPHANT, position)
    
    def get_possible_moves(self, board) -> List[Position]:
        moves = []
        # 相/象走田字
        directions = [(2, 2), (2, -2), (-2, 2), (-2, -2)]
        for dx, dy in directions:
            new_x = self.position.x + dx
            new_y = self.position.y + dy
            
            # 检查是否过河和田心是否有子
            if self.color == PieceColor.RED:
                if 0 <= new_x <= 8 and 0 <= new_y <= 4:
                    # 检查田心是否有子
                    center_x = self.position.x + dx // 2
                    center_y = self.position.y + dy // 2
                    if not board.get_piece_at(Position(center_x, center_y)):
                        moves.append(Position(new_x, new_y))
            else:
                if 0 <= new_x <= 8 and 5 <= new_y <= 9:
                    # 检查田心是否有子
                    center_x = self.position.x + dx // 2
                    center_y = self.position.y + dy // 2
                    if not board.get_piece_at(Position(center_x, center_y)):
                        moves.append(Position(new_x, new_y))
        
        return moves

class Horse(Piece):
    def __init__(self, color: PieceColor, position: Position):
        super().__init__(color, PieceType.HORSE, position)
    
    def get_possible_moves(self, board) -> List[Position]:
        moves = []
        # 马走日，需要检查蹩马腿
        directions = [
            (-2, -1), (-2, 1),  # 向左跳
            (2, -1), (2, 1),    # 向右跳
            (-1, -2), (1, -2),  # 向上跳
            (-1, 2), (1, 2)     # 向下跳
        ]
        
        # 对应的蹩马腿位置
        leg_positions = {
            (-2, -1): (-1, 0), (-2, 1): (-1, 0),  # 左跳检查左边
            (2, -1): (1, 0), (2, 1): (1, 0),      # 右跳检查右边
            (-1, -2): (0, -1), (1, -2): (0, -1),  # 上跳检查上边
            (-1, 2): (0, 1), (1, 2): (0, 1)       # 下跳检查下边
        }
        
        for dx, dy in directions:
            new_x = self.position.x + dx
            new_y = self.position.y + dy
            
            # 检查是否在棋盘内
            if 0 <= new_x <= 8 and 0 <= new_y <= 9:
                # 检查蹩马腿
                leg_dx, leg_dy = leg_positions[(dx, dy)]
                leg_x = self.position.x + leg_dx
                leg_y = self.position.y + leg_dy
                
                # 如果蹩马腿位置没有棋子，这个移动是合法的
                if not board.get_piece_at(Position(leg_x, leg_y)):
                    moves.append(Position(new_x, new_y))
        
        return moves

class Chariot(Piece):
    def __init__(self, color: PieceColor, position: Position):
        super().__init__(color, PieceType.CHARIOT, position)
    
    def get_possible_moves(self, board) -> List[Position]:
        moves = []
        # 车可以横向或纵向移动任意距离，直到遇到棋子或边界
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dx, dy in directions:
            new_x = self.position.x
            new_y = self.position.y
            
            while True:
                new_x += dx
                new_y += dy
                
                # 检查是否超出边界
                if not (0 <= new_x <= 8 and 0 <= new_y <= 9):
                    break
                
                # 检查新位置是否有棋子
                target_piece = board.get_piece_at(Position(new_x, new_y))
                if target_piece:
                    # 如果是敌方棋子，可以吃掉
                    if target_piece.color != self.color:
                        moves.append(Position(new_x, new_y))
                    break
                
                moves.append(Position(new_x, new_y))
        
        return moves

class Cannon(Piece):
    def __init__(self, color: PieceColor, position: Position):
        super().__init__(color, PieceType.CANNON, position)
    
    def get_possible_moves(self, board) -> List[Position]:
        moves = []
        # 炮的移动规则：直线移动，吃子需要翻过一个棋子
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dx, dy in directions:
            new_x = self.position.x
            new_y = self.position.y
            found_platform = False  # 是否找到炮架
            
            while True:
                new_x += dx
                new_y += dy
                
                # 检查是否超出边界
                if not (0 <= new_x <= 8 and 0 <= new_y <= 9):
                    break
                
                target_piece = board.get_piece_at(Position(new_x, new_y))
                if not found_platform:
                    if target_piece:
                        found_platform = True  # 找到炮架
                    else:
                        moves.append(Position(new_x, new_y))  # 可以移动到空位
                else:
                    if target_piece:
                        # 已经有炮架，且遇到棋子，如果是敌方棋子可以吃
                        if target_piece.color != self.color:
                            moves.append(Position(new_x, new_y))
                        break
        
        return moves

class Pawn(Piece):
    def __init__(self, color: PieceColor, position: Position):
        super().__init__(color, PieceType.PAWN, position)
    
    def get_possible_moves(self, board) -> List[Position]:
        moves = []
        # 兵/卒的移动规则
        if self.color == PieceColor.RED:
            # 红方兵
            directions = [(0, 1)]  # 未过河只能向前
            if self.position.y > 4:  # 过河后可以左右移动
                directions.extend([(1, 0), (-1, 0)])
        else:
            # 黑方卒
            directions = [(0, -1)]  # 未过河只能向前
            if self.position.y < 5:  # 过河后可以左右移动
                directions.extend([(1, 0), (-1, 0)])
        
        for dx, dy in directions:
            new_x = self.position.x + dx
            new_y = self.position.y + dy
            
            # 检查是否在棋盘内
            if 0 <= new_x <= 8 and 0 <= new_y <= 9:
                moves.append(Position(new_x, new_y))
        
        return moves