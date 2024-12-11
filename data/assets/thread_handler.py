import threading
from data import assets


def start_thread(args):
    thread = threading.Thread(target=assets.generator, args=args)
    thread.start()

