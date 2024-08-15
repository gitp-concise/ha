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



from sys import stdin

"""
TODO:
- 일단 SegmentTree부터 구현하기
- main 구현하기
"""


def main() -> None:
    N: int = int(stdin.readline().rstrip())
    for _ in range(N):
        args: list[int] = list(map(int, stdin.readline().rstrip().split()))
        n = args[0]
        m = args[1]
        cd_ids: list[int] = list(map(int, stdin.readline().rstrip().split()))

        # create cd_coor map
        cd_coor = {}
        for i in range(n):
            cd_coor[i + 1] = n - i
        # create position accumulate segmenttree
        flag_arr = [0 for i in range(n + m + 1)]
        for i in range(n):
            flag_arr[i + 1] = 1
        tree: SegmentTree[int, int] = SegmentTree(flag_arr, 0, lambda x, y: x + y)
        cursor = n + 1
        for cd_id in cd_ids:
            print(tree.query(cd_coor[cd_id] + 1, n+m), end=" ")
            # modify position flag
            tree.insert(cd_coor[cd_id], 0)
            tree.insert(cursor, 1)
            # move cd_coor
            cd_coor[cd_id] = cursor
            # query
            cursor += 1


if __name__ == "__main__":
    main()
