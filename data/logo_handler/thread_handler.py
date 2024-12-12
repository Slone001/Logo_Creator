import threading
from data import logo_handler


def start_thread(args):
    thread = threading.Thread(target=logo_handler.generator, args=args)
    thread.start()

