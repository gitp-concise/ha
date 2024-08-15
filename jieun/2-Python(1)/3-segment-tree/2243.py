from lib import SegmentTree
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

    tree: SegmentTree[int, int] = SegmentTree([0], 0, lambda x, y: x + y)
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