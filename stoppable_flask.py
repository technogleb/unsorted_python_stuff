"""
Simple wrapper, that adds stop method to Flask app.
It allows for the flask application to be run and stopped any times.
That can be sometimes helpful.
"""

import multiprocessing as mp
import time

import flask


class StoppableFlask(flask.Flask):
    def __init__(self, name):
        super().__init__(name)
        self.run_proxy = None

    def run(self, *args, **kwargs):
        self.run_proxy = mp.Process(target=super().run, args=args, kwargs=kwargs)
        self.run_proxy.start()

    def stop(self):
        self.run_proxy.terminate()


if __name__ == "__main__":
    app = StoppableFlask(__name__)
    app.run()
    time.sleep(5)
    app.stop()
    time.sleep(5)
    app.run()
