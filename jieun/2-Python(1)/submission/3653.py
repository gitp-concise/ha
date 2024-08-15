from __future__ import annotations
from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Callable, List

T = TypeVar("T")
U = TypeVar("U")

@dataclass
class SegmentTree(Generic[T, U]):
    def __init__(self, data: list[T], func: Callable[[U, U], U], default: U):
        self.n = len(data)
        self.tree = [default] * (4 * self.n)
        self.func = func        # 구간 쿼리를 위한 함수
        self.default = default  # 기본값
        # 세그먼트 트리에 data 복사하기
        for i in range(self.n):
            self.tree[self.n + i] = data[i]
        # leaf node를 제외한 나머지 node 채우기
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = func(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, index: int, diff: T):
        index += self.n
        self.tree[index] += diff
        while index > 1:
            index //= 2
            self.tree[index] = self.func(self.tree[2 * index], self.tree[2 * index + 1])

    def query(self, left: int, right: int) -> U:
        result = self.default
        left += self.n
        right += self.n
        while left < right:
            if left % 2:
                result = self.func(result, self.tree[left])
                left += 1
            if right % 2:
                right -= 1
                result = self.func(result, self.tree[right])
            left //= 2
            right //= 2
        return result


import sys


"""
TODO:
- 일단 SegmentTree부터 구현하기
- main 구현하기
"""


def main() -> None:
    # 구현하세요!
    pass


if __name__ == "__main__":
    main()