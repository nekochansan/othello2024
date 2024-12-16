import math
import random

# 石の種類を定義 (1が黒石、2が白石)
BLACK = 1
WHITE = 2

# 6x6の初期状態のオセロボードを定義
board = [
    [0, 0, 0, 0, 0, 0],  # 0は空きマスを表す
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 2, 0, 0],  # 中央に黒石(1)と白石(2)が配置されている
    [0, 0, 2, 1, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]

def can_place_x_y(board, stone, x, y):
    """
    石を置けるかどうかを調べる関数。
    board: 2次元配列のオセロボード
    x, y: 石を置きたい座標 (0-indexed)
    stone: 現在のプレイヤーの石 (1: 黒, 2: 白)
    return: 置けるなら True, 置けないなら False
    """
    if board[y][x] != 0:
        return False  # 既に石がある場合は置けない

    opponent = 3 - stone  # 相手の石 (1なら2、2なら1)
    directions = [(-1, -1), (-1, 0), (-1, 1),  # 全8方向 (左上, 上, 右上)
                  (0, -1),          (0, 1),     # 左, 右
                  (1, -1), (1, 0), (1, 1)]     # 左下, 下, 右下

    # 各方向を調べる
    for dx, dy in directions:
        nx, ny = x + dx, y + dy  # 隣のマス
        found_opponent = False  # 相手の石が挟まれるかどうか

        # 相手の石が続いている限り進む
        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            found_opponent = True

        # 最後に自分の石があれば、この方向で石を置ける
        if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            return True

    # どの方向でも石を置けなかった場合はFalseを返す
    return False

def count_flipped(board, stone, x, y):
    """
    石を置いたときに裏返せる石の数をカウントする関数。
    board: 2次元配列のオセロボード
    x, y: 石を置きたい座標 (0-indexed)
    stone: 現在のプレイヤーの石 (1: 黒, 2: 白)
    return: 裏返せる石の総数
    """
    if not can_place_x_y(board, stone, x, y):
        return 0  # 置けない場所なら0を返す

    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    total_flipped = 0

    # 各方向で裏返せる石を数える
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        flipped = 0  # この方向で裏返せる石の数

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            flipped += 1

        # 自分の石で挟めた場合のみ有効
        if 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            total_flipped += flipped

    return total_flipped

class EagarAI(object):
    """
    最も多くの石を裏返せる場所を選ぶAIクラス。
    """

    def face(self):
        # AIのシンボルとしての顔文字を返す
        return "🤖"

    def place(self, board, stone):
        """
        最も多くの石を裏返せる場所を選んで返す。
        board: 2次元配列のオセロボード
        stone: 現在のプレイヤーの石 (1: 黒, 2: 白)
        return: 選んだ位置 (x, y)
        """
        max_flipped = -1
        best_move = None

        # ボード全体をチェックして最良の場所を探す
        for y in range(len(board)):
            for x in range(len(board[0])):
                flipped = count_flipped(board, stone, x, y)  # 裏返せる石の数を計算
                if flipped > max_flipped:
                    max_flipped = flipped
                    best_move = (x, y)  # 最良の位置を更新

        return best_move  # 最良の位置を返す
