import multiprocessing
from PyUtils.Functions import *

class TestThreading:

    def __init__(self):
        print("TestThreading")

    def big_task(self, list_str_params):
        ncores = multiprocessing.cpu_count()
        if ncores <= 1:
            ncores = 2
        print("-- ncores:" + str(ncores))
        splitted_list = split_list(list_str_params, ncores)
        print(splitted_list)






def gen_dataset(list_sample, n_copies):
    list_out = []
    for i in range(n_copies):
        for item in list_sample:
            list_out.append(item + "_" + str(i))
    print(list_out)
    return list_out


if __name__ == '__main__':
    list_sample = ["abacate",
                "banana",
                "carambola",
                "damasco",
                "espinafre",
                "framboesa",
                "goiaba"]
    list_str = gen_dataset(list_sample, 10)


    pp = split_list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 2)
    print(pp)
    tt = TestThreading()
    tt.big_task(list_str)