import math
import re
import sys
from collections import defaultdict, namedtuple

SIDES = ["top", "left", "bottom", "right"]
BORDER_COLOR = "black"


class SquarePiece(namedtuple("SquarePiece", SIDES)):
    def __str__(self):
        return f"({','.join(getattr(self, s) for s in SIDES)})"

    @staticmethod
    def parse_string(string):
        string = re.sub(r"(\(|\))", "", string)
        return SquarePiece(*string.split(","))


class PuzzleAssembly:
    def __init__(self, square_pieces):
        self._square_pieces = square_pieces
        self._n = int(math.sqrt(len(square_pieces)))

        self._grid = [[None] * self._n for _ in range(self._n)]
        self._in_grid = set()

        self._build_lookup_table()
        self._place_corner_pieces()

        self._backtrack((0, 0))

    def _build_lookup_table(self):
        self._lookup_table = defaultdict(set)

        for square_piece in self._square_pieces:
            for side in SIDES:
                color = getattr(square_piece, side)
                self._lookup_table[(side, color)].add(square_piece)

    def _place_corner_pieces(self):
        corners = [
            ("top", "left", 0, 0),
            ("top", "right", 0, self._n - 1),
            ("bottom", "left", self._n - 1, 0),
            ("bottom", "right", self._n - 1, self._n - 1),
        ]

        for *sides, i, j in corners:
            corner_piece = self._get_corner_piece(*sides)
            self._grid[i][j] = corner_piece
            self._in_grid.add(corner_piece)

    def _get_corner_piece(self, side_1, side_2):
        for piece in self._lookup_table[(side_1, BORDER_COLOR)]:
            if piece in self._lookup_table[(side_2, BORDER_COLOR)]:
                return piece

    def _backtrack(self, prev_pos):
        cur_pos = self._get_next_pos(prev_pos)

        # Reach the end of the grid
        if cur_pos is None:
            return True

        i, j = cur_pos
        for piece in self._get_non_corner_piece(cur_pos):
            self._grid[i][j] = piece
            self._in_grid.add(piece)
            solution_found = self._backtrack(cur_pos)

            if solution_found:
                return True

            self._grid[i][j] = None
            self._in_grid.remove(piece)

        return False

    def _get_next_pos(self, pos):
        # Skip 4 corners
        i, j = pos
        next_pos = (i, j + 1)

        # Reach the end of the grid
        if i == self._n - 1 and j == self._n - 2:
            return None

        # Move to the next row
        if j == self._n - 1:
            next_pos = (i + 1, 0)

        # Skip 4 corners
        if next_pos in [
            (0, 0),
            (0, self._n - 1),
            (self._n - 1, 0),
            (self._n - 1, self._n - 1),
        ]:
            return self._get_next_pos(next_pos)

        return next_pos

    def _get_non_corner_piece(self, pos):
        i, j = pos

        # Top border
        if i == 0:
            template = SquarePiece(
                top=BORDER_COLOR,
                left=self._grid[i][j - 1].right,
                bottom=None,
                right=self._grid[i][j + 1] and self._grid[i][j + 1].left,
            )

        # Bottom border
        elif i == self._n - 1:
            template = SquarePiece(
                top=self._grid[i - 1][j].bottom,
                left=self._grid[i][j - 1].right,
                bottom=BORDER_COLOR,
                right=self._grid[i][j + 1] and self._grid[i][j + 1].left,
            )

        # Left border
        elif j == 0:
            template = SquarePiece(
                top=self._grid[i - 1][j].bottom,
                left=BORDER_COLOR,
                bottom=self._grid[i + 1][j] and self._grid[i + 1][j].top,
                right=self._grid[i][j + 1] and self._grid[i][j + 1].left,
            )

        # Right border
        elif j == self._n - 1:
            template = SquarePiece(
                top=self._grid[i - 1][j].bottom,
                left=self._grid[i][j - 1].right,
                bottom=self._grid[i + 1][j] and self._grid[i + 1][j].top,
                right=BORDER_COLOR,
            )

        # Center piece
        else:
            template = SquarePiece(
                top=self._grid[i - 1][j].bottom,
                left=self._grid[i][j - 1].right,
                bottom=None,
                right=None,
            )

        for piece in self._lookup_table[("top", template.top)]:
            if not (
                piece in self._in_grid
                or template.left != piece.left
                or (template.bottom and template.bottom != piece.bottom)
                or (template.right and template.right != piece.right)
            ):
                yield piece

    @property
    def result(self):
        return "\n".join(";".join(str(piece) for piece in row) for row in self._grid)


if __name__ == "__main__":
    data = sys.stdin.read().split("\n")
    square_pieces = [SquarePiece.parse_string(s) for s in data if s]
    print(PuzzleAssembly(square_pieces).result)
