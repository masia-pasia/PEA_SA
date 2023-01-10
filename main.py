import math
import random
from sys import maxsize
from itertools import permutations
import time
# Simulated annealing
import numpy as numpy

maxsize = float('inf')


def read_arraylist(file_name):
    with open(file_name) as given_data:
        given_arr = [line.split() for line in given_data]

    graph_length = given_arr[0][0]
    graph_length = int(graph_length)

    for i in range(graph_length):
        j = i+1
        given_arr[i] = list(map(int, given_arr[j]))

    return given_arr


def simulated_annealing(given_arr, graph_length, temp_temperature, alpha, L):
    global final_res
    global final_path

    # pierwsza sciezka po kolei
    min_path = []
    for i in range(graph_length):
        min_path.append(i)

    min_path_length = 0
    for i in range(graph_length):
        if i < graph_length-1:
            min_path_length += given_arr[min_path[i]][min_path[i+1]]
        else:
            min_path_length += given_arr[min_path[i]][min_path[0]]

    while temp_temperature > 1:
        L_count = 1

        while L > 0:
            temp_path = min_path
            temp_path_length = 0

            node1 = random.randrange(graph_length)
            node2 = random.randrange(graph_length)

            while node2 == node1:
                node2 = random.randrange(graph_length)

            # zamiana wierzcholkow dla 2-zamian (do odkomentowania)
            # temp = temp_path[node1]
            # temp_path[node1] = temp_path[node2]
            # temp_path[node2] = temp

            # zamiana wiercholkow dla po luku (do odkomentowania)
            delta = abs(node1 - node2)

            if node1 > node2:
                lownode = node2
                highnode = node1
            else:
                lownode = node1
                highnode = node2

            node_range = math.ceil(delta / 2)
            if node_range == 1:
                temp = temp_path[highnode]
                temp_path[highnode] = temp_path[lownode]
                temp_path[lownode] = temp
            else:
                for i in range(node_range):
                    temp = temp_path[highnode-i]
                    temp_path[highnode-i] = temp_path[lownode+i]
                    temp_path[lownode+i] = temp

            # ustalenie nowego kosztu sciezki
            for i in range(graph_length):
                if i < graph_length - 1:
                    temp_path_length += given_arr[temp_path[i]][temp_path[i+1]]
                else:
                    temp_path_length += given_arr[temp_path[i]][temp_path[0]]

            if temp_path_length < final_res:
                final_res = temp_path_length
                final_path = temp_path
            else:
                acceptance = numpy.exp((min_path_length - temp_path_length) / temp_temperature)
                s = random.randrange(101)/100

                if s < acceptance:
                    min_path_length = temp_path_length
                    min_path = temp_path

            L -= 1
        temp_temperature = temp_temperature * pow(alpha, L_count)  # schemat geometryczny
        # temp_temperature /= (1 + math.log(1 + L_count))  # schemat Boltzmanna
        L_count += 1


if __name__ == '__main__':

    with open("./data.ini") as data:
        given_data = [line.split() for line in data]

    with open("./output.csv", "a") as results:
        results.write("\nSimulated annealing\n")

    for i in range(13):
        file_name = given_data[i][0]
        tests_number = int(given_data[i][1])
        opt_path_length = int(given_data[i][2])

        last_index = len(given_data[i])
        verticies = []
        for k in range(3, last_index):
            verticies.append(given_data[i][k])

        print("Testing " + file_name + " in progress...\n")

        with open("./output.csv", "a") as results:
            results.write(file_name + ' ')
            results.write(str(tests_number) + ' ')
            results.write(str(opt_path_length) + '\n')

        returned_arr = read_arraylist(file_name)

        temperature = [10.0, 100.0, 1000.0, 10000.0]
        alpha = [0.99, 0.9999, 0.99999, 0.999999]
        L = [10, 100, 1000, 10000, 100000]

        for n in range(0, len(temperature)):
            for m in range(0, len(alpha)):
                for k in range(0, len(L)):

                    total_error_rate = 0
                    average_elapsed_time = 0

                    for j in range(tests_number):
                        elapsed_time = 0
                        error_rate = 0

                        graph_length = len(returned_arr) - 1
                        final_path = [None] * (graph_length + 1)
                        visited = [False] * graph_length
                        final_res = maxsize

                        st = time.time_ns()
                        simulated_annealing(returned_arr, graph_length, temperature[n], alpha[m], L[k])
                        et = time.time_ns()
                        elapsed_time = et - st

                        elapsed_time = elapsed_time / 1000  # z nano robimy mikro sekundy
                        average_elapsed_time += elapsed_time

                        error_rate = round(((final_res-opt_path_length)/opt_path_length * 100), 2)
                        total_error_rate += error_rate

                    average_elapsed_time /= tests_number
                    average_elapsed_time = round(average_elapsed_time, 3)
                    total_error_rate /= tests_number
                    total_error_rate = round(total_error_rate, 3)

                    with open("./output.csv", "a") as results:
                        results.write(str(temperature[n]) + ';')
                        results.write(str(alpha[m]) + ';')
                        results.write(str(L[k]) + ';')
                        results.write(str(average_elapsed_time) + ';')
                        results.write(str(total_error_rate) + '\n')

        print("Testing " + file_name + " completed\n")