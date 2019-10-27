import numpy as np


def tile_generator(values, rand=False, shape=[10, 10]):
    length = shape[0]*shape[1]
    values = np.array(values)
    summ = sum(values)
    relative_val = np.ceil(values/summ * length)

    if sum(relative_val) > length:
        max_ind = relative_val.argmax()
        relative_val[max_ind] = relative_val[max_ind] - (sum(relative_val) - length)

    relative_val = relative_val.astype('int32')
    categories = len(values)

    points = []

    for cat in range(categories):
        for i in range(relative_val[cat]):
            points.append(cat)
    points = np.array(points)

    if(rand):
        np.random.shuffle(points)
        np.random.shuffle(points)
        np.random.shuffle(points)

    points = points.reshape(shape)

    return points