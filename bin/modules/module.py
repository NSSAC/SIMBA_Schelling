#import pandas as pd
import numpy as np
import json


class environment:
    def __init__(self):
        self.STATUS = "INIT"

    def reset(self):
        self.STATUS = "RUNNING"
        self.msg = "Hello World"
        self.tick = 0
        self.MAX_TICKS = len(self.msg)

        return(self.output(self.msg))

    def step(self):
        out = self.msg[self.tick]

        self.tick += 1
        if self.tick == self.MAX_TICKS:
            self.end()

        return(self.output(out))

    def output(self, out: str):
        return({'status': self.STATUS, 'output': [out]})

    def end(self):
        self.STATUS = "DONE"


if __name__ == '__main__':
    e = environment()
    print(e.reset())
    print(json.dumps(e.reset(), indent=4))
    print(e.step())
