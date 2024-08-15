from lib import SegmentTree
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
