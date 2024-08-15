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
- 일단 Segmentseg_tree부터 구현하기
- main 구현하기
"""


def main() -> None:
    # 구현하세요!
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    index += 1
    
    MAX_TASTE = 1000000
    seg_tree = SegmentTree(data=[0] * (MAX_TASTE + 1), func=lambda x, y: x + y, default=0)
    
    result = []
    for _ in range(n):
        A = int(data[index])
        if A == 1:  # B순위 사탕 꺼내기
            B = int(data[index + 1])
            index += 2

            left, right = 1, MAX_TASTE
            while left < right:
                mid = (left + right) // 2
                if seg_tree.query(1, mid + 1) >= B:
                    right = mid
                else:
                    left = mid + 1
            
            result.append(left)
            seg_tree.update(left - 1, -1)  # Remove one candy of taste `left`
        
        elif A == 2:  # B맛 사탕 C개 삽입
            B = int(data[idx])
            C = int(data[idx])
            idx += 2
            
            seg_tree.update(B - 1, C)
    
    sys.stdout.write("\n".join(map(str, result)) + "\n")

if __name__ == "__main__":
    main()