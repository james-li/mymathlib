#!/usr/bin/env python3
import sys

from rational.rational import rational


class cal_node:
    _OPERATOR = {
        '+': ("__add__", 0),
        '-': ("__sub__", 1),
        "*": ("__mul__", 2),
        "/": ("__truediv__", 3)
    }

    def __init__(self, *args, **kwargs):
        value = args[0]
        if type(value) == int:
            self._value = rational(value)
        else:
            self._value = value
        self._left = kwargs.get("left")
        self._right = kwargs.get("right")

    def is_num(self):
        if type(self._value) == rational:
            return True
        else:
            return False

    def _value_key(self) -> int:
        if type(self.value) == rational:
            return self.value.int_value()
        else:
            return self._OPERATOR.get(self.value)[1] + 10

    def __hash__(self):
        v: int = self._value_key()
        if self.left:
            return v * 2 + hash(self.left) + hash(self.right)
        else:
            return v

    def equal(self, other):
        if type(other) != cal_node or not isinstance(self.value, type(other.value)):
            return False
        if self.value != other.value:
            return False
        if self.left == other.left and self.right == other.right:
            return True
        elif self.value in ["+", "*"] and self.left == other.right and self.right == other.left:
            return True
        else:
            return False

    def __eq__(self, other):
        return self.equal(other)

    @property
    def value(self):
        return self._value

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    def __str__(self):
        if self.is_num():
            return str(self._value)
        else:
            if self.left and self.left.is_num():
                l = str(self.left)
            else:
                l = "(" + str(self.left) + ")"

            if self.right and self.right.is_num():
                r = str(self.right)
            else:
                r = "(" + str(self.right) + ")"

            return "%s%s%s" % (l, self._value, r)

    def adjust(self, rotate: bool = False, parent=None):
        if rotate:
            if self.value == parent.value:
                self.left, self.right = self.right, self.left
                return True
            return False
        if self.left:
            self.left.adjust()
            if self.right.adjust(self.value in ["-", "/"], self):
                self.value = "+" if self.value == "-" else "*"
                return True
        return False

    @staticmethod
    def cal(top):
        if top.is_num():
            return top.value
        else:
            op, _ = cal_node._OPERATOR.get(top.value)
            if not op:
                raise SyntaxError("Invalid op")
            func = getattr(rational, op)
            if not func:
                raise SyntaxError("Invalid op")
            return func(cal_node.cal(top.left), cal_node.cal(top.right))

    @staticmethod
    def get_top_node(expr: str):
        pass

    @staticmethod
    def get_all_top_node(vlist: list) -> list:
        if len(vlist) == 1:
            if type(vlist[0]) != cal_node:
                return [cal_node(vlist[0])]
            else:
                return vlist
        else:
            r = []
            for i in range(1, len(vlist)):
                l_list = cal_node.get_all_top_node(vlist[0:i])
                r_list = cal_node.get_all_top_node(vlist[i:])
                for l_node in l_list:
                    for r_node in r_list:
                        for op in cal_node._OPERATOR.keys():
                            cnode = cal_node(op, left=l_node, right=r_node)
                            cnode.adjust()
                            r.append(cnode)
            return r

    @staticmethod
    def get_permutation(vlist: list) -> list:
        if len(vlist) == 1:
            return [vlist]
        rlist = []
        r = []
        for i, v in enumerate(vlist):
            if v in rlist:
                continue
            rlist.append(v)
            nlist = vlist[0:i] + vlist[i + 1:]
            for sublist in cal_node.get_permutation(nlist):
                r.append([v] + sublist)
        return r

    @value.setter
    def value(self, value):
        self._value = value

    @left.setter
    def left(self, value):
        self._left = value

    @right.setter
    def right(self, value):
        self._right = value


if __name__ == "__main__":
    try:
        vlist = [int(sys.argv[i]) for i in range(1, 5)]
    except:
        vlist = [3, 3, 8, 8]
    p_list = cal_node.get_permutation(vlist)
    cal_node_set = set()
    result_set = set()
    for vlist in p_list:
        tmp_list = cal_node.get_all_top_node(vlist)
        cal_node_set.update(tmp_list)
    for node in cal_node_set:
        # print(node)
        try:
            if cal_node.cal(node) == 24:
                result_set.add(node)
        except:
            pass
    for node in result_set:
        print("%s=24" % (node))
