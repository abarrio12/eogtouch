from os.path import abspath, dirname, join

ROOT_DIR = dirname(dirname(dirname(abspath(__file__))))


def img_path(img: str) -> str:
    return join(ROOT_DIR, "data/img", img)
