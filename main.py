"""Main"""
__author__ = 'Equipe-ECV'

import arguments
from calculate_icm import IcmCalculator


class Main:
    def __init__(self, args):
        self._args = args
        self._highway = args["highway"]
        self._direction = args["direction"]
        self._contract = args["contract"]

    def run(self):
        icm = IcmCalculator()
        icm.calculateAllICM(self._highway, self._direction, self._contract)


if __name__ == "__main__":

    args = arguments.parseArguments()

    main = Main(args)
    main.run()
