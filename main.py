from src.csv_reader import get_cargos, get_trucks
from src.nns import simple_nearest_neighbour, nearest, find_next_closest
from src.kdtree import trucks_kdtree
import argparse


def main():
    parser = argparse.ArgumentParser(
        description='Find nearest trucks to cargos.')
    parser.add_argument('option', metavar='N', type=str,
                        help='choose an algorithm ("brute" or "kdtree")')
    args = parser.parse_args()

    cargos = get_cargos()
    trucks = get_trucks()
    tree = trucks_kdtree(trucks)
    t_result = {}
    for c in cargos:
        point = (c['origin_lat'], c['origin_lng'])
        # kd tree search
        if args.option == 'kdtree':
            truck = nearest(tree, point)
        # brute force
        elif args.option == 'brute':
            truck = simple_nearest_neighbour(c, trucks)
        else:
            raise Exception(
                "No algorithm selected. Select 'brute' or 'kdtree'")

        # if truck already selected, will search for the next best and rearrange
        find_next_closest(t_result, truck, c)

    for t in t_result:
        print(
            f'{t} -> {t_result[t][1]["product"]} ({t_result[t][1]["origin_city"]}) [ {t_result[t][0]} KM ]')


if __name__ == "__main__":
    main()
