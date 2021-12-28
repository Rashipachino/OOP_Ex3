import sys

from src.GraphAlgo import GraphAlgo

if __name__ == '__main__':
    g_algo = GraphAlgo()
    print(g_algo.load_from_json(sys.argv[1]))
    g_algo.plot_graph()
