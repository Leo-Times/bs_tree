import json
import copy

city_data = open("data/cities.json")
cities = json.load(city_data)

towns = {
    0: {'name': 'Romanshorn', 'population': 11556, 'latitude': 47.56586, 'longitude': 9.37869},
    1: {'name': 'Amriswil', 'population': 14313, 'latitude': 47.54814, 'longitude': 9.30327},
    2: {'name': 'Arbon', 'population': 15459, 'latitude': 47.51360, 'longitude': 9.42999},
    3: {'name': 'Weinfelden', 'population': 11893, 'latitude': 47.56638, 'longitude': 9.10588},
    4: {'name': 'Frauenfeld', 'population': 26093, 'latitude': 47.55856, 'longitude': 8.89685},
    5: {'name': 'Kreuzlingen', 'population': 22788, 'latitude': 47.645837,'longitude': 9.178608},
    6: {'name': 'Egnach', 'population': 4897, 'latitude': 47.54565, 'longitude': 9.37864},
}

sorted = []
for id,town in cities.items():
    tuple_pop_id = (int(town['population']),id)
    sorted.append(tuple_pop_id)

sorted.sort()

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

def build_bst(sorted_list, lower, upper):
    if lower > upper:
        return None

    median_idx = (lower + upper) // 2
    median = sorted_list[median_idx]
    node = Node(median[0], median[1])
    node.left = build_bst(sorted_list, lower, median_idx - 1)
    node.right = build_bst(sorted_list, median_idx + 1, upper)
    return node  

tree = build_bst(sorted, 0 ,len(sorted)-1)


def binary_search_population_range(tree, low, high, results=[]):
    if tree is None:
        return results

    if tree.key >= low:
        binary_search_population_range(tree.left, low, high, results)

    if low <= tree.key <= high:
        results.append(tree.value)

    if tree.key <= high:
        binary_search_population_range(tree.right, low, high, results)

    return results

#hold = binary_search_population_range(tree, 1000000, 2000000)
#print(hold)

#for h in hold:
    print(cities[h]['name'])

##############
# :3 KD-Tree #
##############

class kNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

def is_within_bounds(keys, bounds):
    for key, bound in zip(keys,bounds):
        if not bound[0] <= key <= bound[1]:
            return False
        return True

def filter_tuples(tuples, bounds):
    filtered = []
    for tuple in tuples:
        keys, value = tuple
        if is_within_bounds(keys,bounds):
            filtered.append(tuple)
    return filtered

def find_median(tuples):
    if not tuples:
        return None
    index = len(tuples)//2
    return tuples.pop(index)

def build_kd_tree(tuples, bounds, depth=0):
    filtered = filter_tuples(tuples, bounds)
    median = find_median(filtered)
    if not median:
        return None
    
    node = kNode(median[0],median[1])

    dimension_index = depth % len(bounds)

    left_bounds = copy.deepcopy(bounds)
    left_bounds[dimension_index] = (left_bounds[dimension_index][0], node.key[dimension_index])

    right_bounds = copy.deepcopy(bounds)
    right_bounds[dimension_index] = (node.key[dimension_index],right_bounds[dimension_index][1])

    node.left = build_kd_tree(filtered, left_bounds, depth+1)
    node.right = build_kd_tree(filtered, right_bounds, depth+1)

    return node

lat_lon_tup = [((town['latitude'],town['longitude']),id) for id, town in towns.items()]

bounds = [(-90,90),(-180,180)]
kd_tree = build_kd_tree(lat_lon_tup,bounds)

def search_kd_tree(tree, bounds, depth=0):
    if tree is None:
        return 
    dimension_index = depth % len(bounds)
    key = tree.key[dimension_index]
    lower, upper = bounds[dimension_index]

    if not lower > key:
        yield from search_kd_tree(tree.left, bounds, depth+1)

    if lower <= key <= upper:
        yield tree

    if not upper < key:
        yield from search_kd_tree(tree.right, bounds, depth+1)


for node in search_kd_tree(kd_tree, [(-90,90),(-180,9.10588)]):
    print(node.key, node.value, towns[node.value]['name'])
