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


def main() -> None:
    from typing import Callable
    def solve(tree: list[int], cnt: int, node: int, node_start: int, node_end: int) -> int:
        if node_start == node_end:
            return node_start

        node_mid: int = (node_start + node_end) // 2

        if cnt <= tree[2 * node]:
            return solve(tree, cnt, 2 * node, node_start, node_mid)
        else:
            return solve(tree, cnt - tree[2 * node], 2 * node + 1, node_mid + 1, node_end)

    MAX: int = 1000000 + 1
    read: Callable[[], str] = lambda: sys.stdin.readline().rstrip()
    N: int = int(read())

    # 시간초과이슈로 생성자말고 수동으로 초기화
    tree: SegmentTree[int, int] = SegmentTree(
        [0],
        0,
        lambda x, y: x + y
    )
    tree.tree = [0] * (MAX * 4)
    tree.length = MAX

    modifier: Callable[[int, int], int] = lambda x, y: x + y

    for _ in range(N):
        args = list(map(int, read().split()))

        if args[0] == 1:
            # solve
            node_idx = solve(tree.tree, args[1], 1, 0, MAX - 1)
            print(node_idx)
            # modify candy cnt
            tree.modify(node_idx, -1, modifier)
        elif args[0] == 2:
            tree.modify(args[1], args[2], modifier)


if __name__ == "__main__":
    main()
