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
    # 구현하세요!
    data = input().split()
    n, m = int(data[0]), int(data[1])
    arr = list(map(int, data[2:n+2]))
    queries = data[n+2:]
    
    seg_tree = SegmentTree.build(size=n, combine=Pair.f_merge, default_value=Pair.default())

    for i in range(n):
        seg_tree.update(i, Pair.f_conv(arr[i]))

    result = []
    q_idx = 0
    while q_idx < len(queries):
        if queries[q_idx] == '1':
            index = int(queries[q_idx + 1]) - 1
            value = int(queries[q_idx + 2])
            seg_tree.update(index, Pair.f_conv(value))
            q_idx += 3
        elif queries[q_idx] == '2':
            left = int(queries[q_idx + 1]) - 1
            right = int(queries[q_idx + 2]) - 1
            res_pair = seg_tree.query(left, right)
            result.append(res_pair.sum())
            q_idx += 3

    print("\n".join(map(str, result)))


if __name__ == "__main__":
    main()