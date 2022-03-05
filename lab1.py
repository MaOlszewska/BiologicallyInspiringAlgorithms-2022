from math import ceil

examples = [(-1, -2), (-1, -1), (3, 0), (-1, 3), (1,1), (0,0)]
answers = [0, 0, 0, 1, 0, 0]
w = [0,0]
theta = 0.1

def adjust(w, d, y, theta, u):
    return w + (d - y) * u * theta

for i in range(len(examples)):
    point = examples[i]
    res = max(min(w[0] * point[0] + w[1] * point[1],1),0)
    while res != answers[i]:
        w[0] = adjust(w[0], answers[i], res, theta, point[0])
        w[1] = adjust(w[1], answers[i], res, theta, point[1])
        res = ceil(max(min(w[0] * point[0] + w[1] * point[1], 1), 0))
    print(examples[i], w, res)

