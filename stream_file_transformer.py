"""
This module implements StreamFileTransformer class, which can take very big
file, that doesn't fit into RAM and process it chunk by chunk with multiple processes using target provided. Target takes chunk and make whatever transformations you want.
"""

import os
import itertools
import multiprocessing
import numpy as np


def test_target(data):
    '''Example target'''
    return len(data)


class StreamFileTransformer:
    def __init__(self, path, target, chunk_size=1024, n_jobs=1):
        self.path = path
        self.target = target
        self.chunk_size = chunk_size
        self.n_jobs = n_jobs

    def read_file_in_chunks(self, f):
        """Generator object to read file chunk by chunk
        without loading the whole file into RAM"""
        while True:
            chunk = f.read(self.chunk_size)
            if not chunk:
                break
            yield chunk

    def process_chunk(self, chunk):
        with multiprocessing.Pool(self.n_jobs) as P:
            groups = np.array_split(np.array(list(chunk)), self.n_jobs)
            groups = [''.join(group) for group in groups]
            processed_groups = P.map(self.target, groups)
            return ''.join(list(itertools.chain.from_iterable(processed_groups)))

    def process_file(self):
        body, ext = os.path.splitext(self.path)
        path_copy = body + '_copy' + ext
        with open(self.path, 'r') as f, open(path_copy, 'w+') as f_copy:
            for chunk in self.read_file_in_chunks(f):
                processed = self.process_chunk(chunk)
                f_copy.write(processed)


if __name__ == "__main__":
    #example usage
    transformer = StreamFileTransfomer("path/to/my/file", test_target, n_jobs='your processes number')
