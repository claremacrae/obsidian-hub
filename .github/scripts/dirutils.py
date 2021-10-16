import os

pushstack = list()


def pushdir(dirname: str):
    global pushstack
    pushstack.append(os.getcwd())
    os.chdir(dirname)


def popdir():
    global pushstack
    os.chdir(pushstack.pop())


def use_directory(dir):
    class PushPopDirectory:
        def __init__(self, dir):
            self.dir = dir

        def __enter__(self):
            pushdir(dir)

        def __exit__(self, exc_type, exc_val, exc_tb):
            popdir()

    os.makedirs(dir, exist_ok=True)
    return PushPopDirectory(dir)
