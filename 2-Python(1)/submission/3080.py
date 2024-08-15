from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Iterable

"""
TODO:
- Trie.push 구현하기
- (필요할 경우) Trie에 추가 method 구현하기
"""

T = TypeVar("T")


@dataclass
class TrieNode(Generic[T]):
    body: Optional[T] = None
    children: list[int] = field(default_factory=lambda: [])
    is_end: bool = False


class Trie(list[TrieNode[T]]):
    def __init__(self) -> None:
        super().__init__()
        self.append(TrieNode(body=None))

    def push(self, seq: Iterable[T]) -> None:
        """
        seq: T의 열 (list[int]일 수도 있고 str일 수도 있고 등등...)

        action: trie에 seq을 저장하기
        """
        cur: int = 0
        for val in seq:
            found: bool = False
            for child_idx in self[cur].children:
                if self[child_idx].body == val:
                    cur = child_idx
                    found = True
                    break

            if not found:
                new_idx = len(self)
                self.append(TrieNode(body=val))
                self[cur].children.append(new_idx)
                cur = new_idx

        self[cur].is_end = True

    # 구현하세요!



import sys

"""
TODO:
- 일단 Trie부터 구현하기
- main 구현하기

힌트: 한 글자짜리 자료에도 그냥 str을 쓰기에는 메모리가 아깝다...
"""


def main() -> None:
    from collections import deque

    factorial_memo: dict[int, int] = {1: 1}
    MOD: int = 1000000007

    def bfs(trie_tree: Trie[int]) -> int:
        que: deque[int] = deque([0])
        visited: set[int] = {0}

        result: int = 1
        while que:
            node_idx = que.popleft()

            node = trie_tree[node_idx]
            if len(node.children) == 0:
                continue

            if node.is_end:
                result *= factorial(len(node.children) + 1)
            else:
                result *= factorial(len(node.children))

            for child in node.children:
                if child not in visited:
                    que.append(child)
                    visited.add(child)

        return result

    def factorial(n: int) -> int:
        if n in factorial_memo:
            return factorial_memo[n]
        else:
            factorial_memo[n] = n * factorial(n - 1)
            return factorial_memo[n]

    def diff(s1: str, s2: str) -> int:
        min_len = min(len(s1), len(s2))
        for i in range(min_len):
            if s1[i] != s2[i]:
                return i
        return min_len

    n: int = int(sys.stdin.readline().rstrip())
    args: list[str] = [sys.stdin.readline().rstrip() for _ in range(n)]
    args.sort()

    tree: Trie[int] = Trie()

    prev_lcp: int = 0
    cur_lcp: int = 0
    for i in range(n - 1):
        cur_lcp = diff(args[i], args[i + 1])
        cutted: list[int] = list(map(ord, args[i][:max(prev_lcp, cur_lcp) + 1]))
        tree.push(cutted)
        prev_lcp = cur_lcp

    tree.push(list(map(ord, args[-1])))

    answer = bfs(tree)

    print(answer % MOD)


if __name__ == "__main__":
    main()
