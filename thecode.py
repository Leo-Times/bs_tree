import json

city_data = open("data/cities.json")
cities = json.load(city_data)

towns = {
    0: {'name': 'Romanshorn', 'population': 11000, 'latitude': 47.56586, 'longitude': 9.37869},
    1: {'name': 'Amriswil', 'population': 14000, 'latitude': 47.54814, 'longitude': 9.30327},
    2: {'name': 'Arbon', 'population': 12000, 'latitude': 47.51360, 'longitude': 9.42999},
    3: {'name': 'Weinfelden', 'population': 13000, 'latitude': 47.56638, 'longitude': 9.10588},
    4: {'name': 'Frauenfeld', 'population': 25000, 'latitude': 47.55856, 'longitude': 8.89685},
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

    if low <= tree.key <= high:
        results.append(tree.value)

    if tree.key > low:
        binary_search_population_range(tree.left, low, high, results)
    if tree.key < high:
        binary_search_population_range(tree.right, low, high, results)

    return results

hold = binary_search_population_range(tree, 12000000, 13000000)
print(hold)

for h in hold:
    print(cities[h]['name'])
