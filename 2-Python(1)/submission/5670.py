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
- count 구현하기
- main 구현하기
"""


def count(trie: Trie, query_seq: str) -> int:
    """
    trie - 이름 그대로 trie
    query_seq - 단어 ("hello", "goodbye", "structures" 등)

    returns: query_seq의 단어를 입력하기 위해 버튼을 눌러야 하는 횟수
    """
    pointer = 0
    cnt = 0

    for element in query_seq:
        if len(trie[pointer].children) > 1 or trie[pointer].is_end:
            cnt += 1

        new_index: int = 0
        for child_idx in trie[pointer].children:
            if trie[child_idx].body == element:
                new_index = child_idx
                break

        pointer = new_index

    return cnt + int(len(trie[0].children) == 1)


def main() -> None:
    # 구현하세요!
    from functools import reduce
    from typing import Callable
    read: Callable[[], str] = lambda: sys.stdin.readline().rstrip()

    while True:
        s: str = read()
        if s == "":
            break
        n: int = int(s)

        s_arr: list[str] = [""] * n
        tree: Trie[str] = Trie()
        for i in range(n):
            s_arr[i] = read()
            tree.push(s_arr[i])

        result = reduce(lambda acc, cur: acc + count(tree, cur), s_arr, 0)
        print(f"{result / n:.2f}")

    pass


if __name__ == "__main__":
    main()
