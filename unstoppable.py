import time
import inspect


def virus(message):
    while True:
        try:
            print(message)
            time.sleep(1)
        except KeyboardInterrupt:
            message = 'I am unstoppable!' + f' You fucked up {len(inspect.stack(0))} times'
            virus(message)


if __name__ == "__main__":
    virus('I am unstoppable!')
