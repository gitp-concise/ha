from lib import Trie
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
