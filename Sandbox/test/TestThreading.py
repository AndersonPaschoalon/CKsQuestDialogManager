import multiprocessing
import threading
from threading import Thread
from threading import Lock
from multiprocessing.pool import ThreadPool
from PyUtils.Functions import *

import time


class TestThreading:

    mutex = Lock()

    def __init__(self):
        print("TestThreading")

    def big_task_thread(self, list_str_params):
        ncores = multiprocessing.cpu_count()
        if ncores <= 1:
            ncores = 2
        #print("-- ncores:" + str(ncores))
        splitted_list = split_list(list_str_params, ncores)
        #print(splitted_list)
        #print("Main thread is " + str(threading.currentThread().ident))
        # ----
        threads = []
        ret_list = []
        for item in splitted_list:
            process = Thread(target=self._exec_big_task, args=[item, ret_list])
            process.start()
            threads.append(process)
        for process in threads:
            process.join()
        # ----
        #print("ret_list:" + str(ret_list))

    def big_task_pool(self, list_str_params):
        ncores = multiprocessing.cpu_count()
        if ncores <= 1:
            ncores = 2
        #print("-- ncores:" + str(ncores))
        splitted_list = split_list(list_str_params, ncores)
        #print(splitted_list)
        #print("Main thread is " + str(threading.currentThread().ident))
        # ----
        pool = ThreadPool()
        async_result_list = []
        ret_list_arg = []
        for item in splitted_list:
            async_result = pool.apply_async(self._exec_big_task, (item, ret_list_arg))
            async_result_list.append(async_result)
        ret_val_list = []
        for item in async_result_list:
            return_val = item.get()
            ret_val_list.append(return_val)
        # ----
        #print("ret_val_list:" + str(ret_val_list))
        #print("ret_list_arg:" + str(ret_list_arg))



    def _exec_big_task(self, small_list, ret_list):
        #print("Current thread id is " + str(threading.currentThread().ident) + " => small_list = " + str(small_list))

        TestThreading.mutex.acquire()
        try:
            ret_list.append(str(threading.currentThread().ident))
        finally:
            TestThreading.mutex.release()
        return str(threading.currentThread().ident)






def gen_dataset(list_sample, n_copies):
    list_out = []
    for i in range(n_copies):
        for item in list_sample:
            list_out.append(item + "_" + str(i))
    #print(list_out)
    return list_out


if __name__ == '__main__':
    list_sample = ["abacate",
                "banana",
                "carambola",
                "damasco",
                "espinafre",
                "framboesa",
                "goiaba"]
    list_str = gen_dataset(list_sample, 1000000)


    #pp = split_list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 2)
    #print(pp)
    tt = TestThreading()

    time.sleep(2)

    start_time = 0
    start_time = time.time()
    tt.big_task_pool(list_str)
    print("pool --- %s seconds ---" % (time.time() - start_time))

    start_time = 0
    start_time = time.time()
    tt.big_task_thread(list_str)
    print("thrad --- %s seconds ---" % (time.time() - start_time))

