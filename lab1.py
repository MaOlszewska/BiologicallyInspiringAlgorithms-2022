from math import ceil
import random


def generateData(numberTraining, numberTesting):
    file = open("points_training.txt", "w")
    for i in range(numberTraining):
        point = [random.randint(-100, 100), random.randint(-100, 100)]
        if(point[1] <= point[0] + 2):
            answer = 0
        else:
            answer = 1
        file.writelines([str(point[0] )," ",  str(point[1] ) , " " ,str(answer),"\n"])
    file.close()

    file = open("points_testing.txt", "w")
    for i in range(numberTesting):
        point = [random.randint(-100, 100), random.randint(-100, 100)]
        if(point[1] <= point[0] + 2):
            answer = 0
        else:
            answer = 1
        file.writelines([str(point[0] )," ",  str(point[1] ) , " " ,str(answer),"\n"])
    file.close()

def adjust(w, d, y, theta, u):
    return w + (d - y) * u * theta

def trainingModel(theta):
    w = [0, 0]
    file = open("points_training.txt", "r")
    for line in file:
        point = []
        for number in line.split():
            point.append(int(number))
        res = max(min(w[0] * point[0] + w[1] * point[1], 1), 0)
        while res != point[2]:
            w[0] = adjust(w[0], point[2], res, theta, point[0])
            w[1] = adjust(w[1], point[2], res, theta, point[1])
            res = ceil(max(min(w[0] * point[0] + w[1] * point[1], 1), 0))
    file.close()
    return w

def test(w):
    file = open("points_testing.txt", "r")
    count = 0
    for line in file:
        point = []
        for number in line.split():
            point.append(int(number))
        res = max(min(w[0] * point[0] + w[1] * point[1], 1), 0)
        if res == point[2]:
            count += 1
    file.close()
    return count

if __name__ == '__main__':
    numberTraining = 100
    numberTesting = 1000
    theta = 0.3
    generateData(numberTraining, numberTesting)
    w = trainingModel(theta)
    answer = test(w)
    print(answer, answer / numberTesting, "%")

