"""Just a simple timer using context manager."""

class SimpleTimer:
    def __enter__(self):
        self.start = time.time()
    
    def __exit__(self, type, values, traceback):
        print("It took {}".format(time.time() - self.start))
