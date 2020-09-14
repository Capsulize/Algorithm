from algorithm import input_models as inputs
from algorithm import output_models as outputs
from algorithm.algorithm import capsulize


def test():
    shifts = capsulize(1, [inputs.Employee(1, 1, (0.5, 0.5), 4, set(), set(), {0})], [inputs.Workspace(1, 1)])
    print(shifts)


if __name__ == "__main__":
    test()
