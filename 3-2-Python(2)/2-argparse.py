import argparse
import logging


def create_parser() -> argparse.ArgumentParser:
    def str_to_bool(s: str) -> bool:
        if s == "True":
            return True
        elif s == "False":
            return False
        else:
            raise argparse.ArgumentTypeError("expected True or False")
    # 구현하세요!
    arg_parser: argparse.ArgumentParser = argparse.ArgumentParser(description="foo parser")
    arg_parser.add_argument("start", type=int)
    arg_parser.add_argument("end", type=int)
    arg_parser.add_argument("verbose", type=str_to_bool)
    return arg_parser



if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    start: int = args.start
    end: int = args.end
    verbose: bool = args.verbose

    print(start, end, verbose)
