from unittest import TestCase

from cal24 import cal_node


class TestCal_node(TestCase):
    def test_cal(self):
        op_node1 = cal_node('+', left=cal_node(1), right=cal_node(2))
        op_node2 = cal_node("*", left=op_node1, right=cal_node(3))
        op_node3 = cal_node('+', left=op_node2, right=cal_node(4))
        op_node4 = cal_node('+', right=op_node2, left=cal_node(4))
        op_node5 = cal_node('-', left=op_node2, right=cal_node(4))
        op_node6 = cal_node('-', right=op_node2, left=cal_node(4))
        print(op_node1)
        print(op_node2)
        print("%s:%d"%(str(op_node3), hash(op_node3)))
        print("%s:%d"%(str(op_node4), hash(op_node4)))
        print("%s:%d"%(str(op_node5), hash(op_node5)))
        print("%s:%d"%(str(op_node6), hash(op_node6)))
        self.assertEqual(cal_node.cal(op_node3), "13")
        self.assertEqual(op_node3, op_node4)
        self.assertEqual(hash(op_node3), hash(op_node4))
        self.assertNotEqual(op_node5, op_node6)

    def test_get_all_top_node(self):
        l = [cal_node(x) for x in range(1, 5)]
        for node in cal_node.get_all_top_node(l):
            print("%s=%s" % (node, cal_node.cal(node)))


    def test_get_permutation_01(self):
        l = [1, 2, 3, 4]
        permutation_list = cal_node.get_permutation(l)
        for p in permutation_list:
            print(p)
        self.assertEqual(len(permutation_list), 24)

    def test_get_permutation_02(self):
        l = [3, 3, 8, 8]
        permutation_list = cal_node.get_permutation(l)
        for p in permutation_list:
            print(p)
        #self.assertEqual(len(permutation_list), 24)

    def test_adjust(self):
        op_node1 = cal_node('-', left=cal_node(4), right=cal_node(2))
        op_node2 = cal_node("-", left=cal_node(1), right=op_node1)
        op_node3 = cal_node("*", left=op_node2, right=cal_node(8))
        print(op_node3)
        op_node3.adjust()
        print(op_node3)

