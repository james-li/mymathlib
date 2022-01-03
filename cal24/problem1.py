'''
任何4位不相同的10以内的数，找到所有算不出24的组合
'''
import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

from cal24 import cal_node

target_queue = Queue()


def test_cal_24(id: int):
    global target_queue
    result_set = []
    while not target_queue.empty():
        vlist = target_queue.get()
        r = "%s feed %s"%(threading.currentThread().getName(), str(vlist))
        if not cal_node.is_resolvable(vlist):
            r += " find one unresolved"
            result_set.append(vlist)
        else:
            r += " resolved"
        print(r+"\n")
    return result_set


def find_numbers(max_workers: int):
    result_set = []
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        results = pool.map(test_cal_24, range(0, max_workers))
        for r in results:
            result_set.extend(r)
        return result_set



if __name__ == "__main__":
    for vlist in cal_node.get_all_array(list(range(1, 10)), 4):
        target_queue.put(vlist)
    print(find_numbers(40))
