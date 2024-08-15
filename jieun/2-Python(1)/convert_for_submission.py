import os
current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)

# PATH_1 = "./1-divide-and-conquer-multiplication"
# PATH_2 = "./2-trie"
# PATH_3 = "./3-segment-tree"
PATH_1 = os.path.join(current_dir, "1-divide-and-conquer-multiplication")
PATH_2 = os.path.join(current_dir, "2-trie")
PATH_3 = os.path.join(current_dir, "3-segment-tree")

ROOT_PATH = {
    "10830": PATH_1,
    "3080": PATH_2,
    "5670": PATH_2,
    "2243": PATH_3,
    "3653": PATH_3,
    "17408": PATH_3
}

# PATH_SUB = "./submission"
PATH_SUB = os.path.join(current_dir, "submission")


def f(n: str) -> None:
    num_code = "".join(filter(lambda x: "from lib import" not in x, open(f"{ROOT_PATH[n]}/{n}.py").readlines()))
    lib_code = open(f"{ROOT_PATH[n]}/lib.py").read()
    code = lib_code + "\n\n\n" + num_code

    open(f"{PATH_SUB}/{n}.py", 'w').write(code)


if __name__ == "__main__":
    for k in ROOT_PATH:
        f(k)