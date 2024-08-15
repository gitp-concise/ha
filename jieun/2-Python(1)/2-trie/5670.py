from lib import Trie
import sys
from typing import Callable


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

    returns: query_seq의 단어를 입력하기 위해 버튼을 눌러야 하는 횟수‹
    """
    pointer = 0
    cnt = 0

    for element in query_seq:
        if len(trie[pointer].children) > 1 or trie[pointer].is_end:
            cnt += 1

        new_index = None # 구현하세요!
        for child_idx in trie[pointer].children:
            if trie[child_idx].body == element:
                new_index = child_idx
                break
        
        if new_index is None:
            break

        pointer = new_index

    return cnt + int(len(trie[0].children) == 1)


def main() -> None:
    # 구현하세요!
    strify: Callable[[str], list[str]] = lambda l: [name.strip() for name in l.split('\n') if name.strip()]

    lines: list[str] = sys.stdin.readlines()

    i = 0
    while i < len(lines):
        N = int(lines[i].strip())
        words : list[str] = strify('\n'.join(lines[i+1: i+1+N]))

        result = 0.00
        trie = Trie[str]()
        for word in words:
            trie.push(word)
        for word in words:
            result += count(trie, word)
        print(f"{result / N:.2f}")

        i += N + 1

if __name__ == "__main__":
    main()