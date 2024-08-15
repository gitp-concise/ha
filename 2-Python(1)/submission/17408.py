from __future__ import annotations

from typing import TypeVar, Generic, Optional, Callable

"""
TODO:
- SegmentTree 구현하기
"""

T = TypeVar("T")
U = TypeVar("U")


class SegmentTree(Generic[T, U]):
    def __init__(self,
                 arr: list[T],
                 default_value: T,
                 merger: Callable[[T, T], T],
                 ):
        self.merger: Callable[[T, T], T] = merger
        self.default_value: T = default_value
        self.tree: list[T] = [default_value for i in range(len(arr) * 4)]
        self.length: int = len(arr)

        # init tree
        for idx, val in enumerate(arr):
            self.insert(idx, val)

    def _query(self, start_idx: int, end_idx: int, node_start: int, node_end: int, node: int) -> T:
        # 겹치는 게 존재하지 않을때
        if node_end < start_idx or end_idx < node_start:
            return self.default_value
        # node범위가 query범위에 포함될때
        if start_idx <= node_start and node_end <= end_idx:
            return self.tree[node]

        node_mid: int = (node_start + node_end) // 2
        return self.merger(
            self._query(start_idx, end_idx, node_start, node_mid, 2 * node),
            self._query(start_idx, end_idx, node_mid + 1, node_end, 2 * node + 1)
        )

    # leaf node를 우선찍고
    # leafnode에서 default value반환
    # 그뒤로 다시 올라오며 modify 실행
    def _modify(self, target_idx: int, node_start: int, node_end: int, node: int, modify_val: T,
                modifier: Callable[[T, T], T]) -> None:
        if not (node_start <= target_idx <= node_end):
            return

        if node_start == node_end:
            self.tree[node] = modifier(self.tree[node], modify_val)
            return

        node_mid: int = (node_start + node_end) // 2
        self._modify(target_idx, node_start, node_mid, 2 * node, modify_val, modifier)
        self._modify(target_idx, node_mid + 1, node_end, 2 * node + 1, modify_val, modifier)

        self.tree[node] = self.merger(self.tree[2 * node], self.tree[2 * node + 1])

    def query(self, start_idx: int, end_idx: int) -> T:
        return self._query(start_idx, end_idx, 0, self.length - 1, 1)

    def insert(self, target_idx: int, modify_val: T) -> None:
        self._modify(target_idx, 0, self.length - 1, 1, modify_val, lambda _, x: x)

    def modify(self, target_idx: int, modify_val: T, modifier: Callable[[T, T], T]) -> None:
        self._modify(target_idx, 0, self.length - 1, 1, modify_val, modifier)



import sys

"""
TODO:
- 일단 SegmentTree부터 구현하기
- main 구현하기
"""


class Pair(tuple[int, int]):
    """
    힌트: 2243, 3653에서 int에 대한 세그먼트 트리를 만들었다면 여기서는 Pair에 대한 세그먼트 트리를 만들 수 있을지도...?
    """

    def __new__(cls, a: int, b: int) -> 'Pair':
        return super().__new__(cls, (a, b))

    @staticmethod
    def default() -> 'Pair':
        """
        기본값
        이게 왜 필요할까...?
        """
        return Pair(0, 0)

    @staticmethod
    def f_conv(w: int) -> 'Pair':
        """
        원본 수열의 값을 대응되는 Pair 값으로 변환하는 연산
        이게 왜 필요할까...?
        """
        return Pair(w, 0)

    @staticmethod
    def f_merge(a: Pair, b: Pair) -> 'Pair':
        """
        두 Pair를 하나의 Pair로 합치는 연산
        이게 왜 필요할까...?
        """
        return Pair(*sorted([*a, *b], reverse=True)[:2])

    def sum(self) -> int:
        return self[0] + self[1]


def main() -> None:
    from typing import Callable
    _ = sys.stdin.readline().rstrip()
    read: Callable[[], str] = lambda: sys.stdin.readline().rstrip()
    arr: list[int] = list(map(int, read().split()))
    pair_arr: list[Pair] = list(map(Pair.f_conv, arr))
    M: int = int(sys.stdin.readline().rstrip())

    tree: SegmentTree[Pair, Pair] = SegmentTree(
        pair_arr,
        Pair.default(),
        Pair.f_merge,
    )
    for _ in range(M):
        args: list[int] = list(map(int, sys.stdin.readline().rstrip().split()))
        if args[0] == 1:
            tree.insert(args[1] - 1, Pair.f_conv(args[2]))
        elif args[0] == 2:
            print(tree.query(args[1] - 1, args[2] - 1).sum())
        else:
            return


if __name__ == "__main__":
    main()
