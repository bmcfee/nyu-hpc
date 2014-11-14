#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import sys
import argparse

import os
import time
from IPython.parallel import Client, require


@require(os, time)
def demo(n):

    time.sleep(0.01)
    return 'Job {:3d}: {:s}\t{:10d}'.format(n,
                                            '-'.join(os.uname()),
                                            os.getpid())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--profile-dir", default=None,
                        help="the IPython profile dir")

    args = parser.parse_args()

    print("Running with the following arguments:")
    print("sys.argv:")
    print(sys.argv)
    print("args:")
    print(args)

    c = Client(profile_dir=args.profile_dir)

    view = c.load_balanced_view()
    view.block = True

    results = view.map(demo, range(128))

    print(results)

#     jobs = [(i, pool.apply(demo, i)) for i in range(128)]

#     retrieved = [False] * len(jobs)

#     while not all(retrieved):
#         for i, (fn, j) in enumerate(jobs):
#             if j.ready() and not retrieved[i]:
#                 try:
#                     j.get()
#                 except Exception as e:
#                     print("Task failed: {0}".format(fn))
#                     print("With error: \n{0}".format(e))
#                 else:
#                     print("Finished: {0}".format(fn))
#                 retrieved[i] = True
#         time.sleep(1)
