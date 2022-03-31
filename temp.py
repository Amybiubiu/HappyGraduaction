data = [{'id': 1, 'sum': 0}, {'id': 1, 'sum': 1}, {'id': 2, 'sum': 2}, {'id': 2, 'sum': 3}, {'id': 3, 'sum': 5}, {'id': 3, 'sum': 4},
        {'id': 3, 'sum': 6}]

# out: filter = [1, 3, 6]

def filter(data):
    i = 1
    filter_id = []
    print(len(data))
    while i < len(data):
        max_id = i - 1
        while i < len(data) and data[i]['id'] == data[i-1]['id']:
            if data[i]['sum'] > data[max_id]['sum']:
                max_id = i
            i += 1
        filter_id.append(max_id)
        i += 1
    return filter_id


print(filter(data))
