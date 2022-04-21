#!/usr/bin/env python3

from rational.rational import rational


class alg_exp_parser:
    NUMBER = "NUMBER"
    BLOCK = "BLOCK"
    OPERATOR = "OPERATOR"
    UNKNOWN = "UNKNOWN"

    @staticmethod
    def isdigit(expr: str) -> bool:
        dot_num = 0
        for i in range(0, len(expr)):
            if expr[i].isdigit():
                continue
            elif expr[i] == '-' and i == 0 and len(expr) > 1:
                continue
            elif expr[i] == '.' and dot_num == 0:
                dot_num += 1
                continue
            else:
                return False
        return True

    @staticmethod
    def get_expr_type(expr: str) -> str:
        if alg_exp_parser.isdigit(expr):
            return alg_exp_parser.NUMBER
        if expr in ["+", "-", "*", "/"]:
            return alg_exp_parser.OPERATOR
        return alg_exp_parser.BLOCK

    @staticmethod
    def expr_split(expr: str) -> list:
        tokens = []
        l = len(expr)
        i = 0
        prev_block_type = None
        while i < l:
            c: str = expr[i]
            if c == '(':
                if prev_block_type != 'OPERATOR' and prev_block_type is not None:
                    raise SyntaxError("Invalid format before bracket")
                prev_block_type = alg_exp_parser.BLOCK
                bracket_level = 1
                i += 1
                block_start = i
                while i < l:
                    c = expr[i]
                    if c == '(':
                        bracket_level += 1
                    elif c == ")":
                        bracket_level -= 1
                        if bracket_level == 0:
                            break
                    i += 1
                if bracket_level != 0:
                    raise SyntaxError("Invalid format without bracket close")
                tokens.append(expr[block_start:i])
                i += 1
            elif (c == '-' and prev_block_type is None) or c.isdigit() or c == '.':
                if prev_block_type != alg_exp_parser.OPERATOR and prev_block_type is not None:
                    raise SyntaxError("Invalid format before number")
                prev_block_type = alg_exp_parser.NUMBER
                block_start = i
                i += 1
                while i < l:
                    c = expr[i]
                    if not c.isdigit() and c != '.':
                        break
                    i += 1
                if expr[block_start:i] == "-":
                    raise SyntaxError("Invalid number format")
                tokens.append(expr[block_start:i])
            elif c in "+-*/":
                if prev_block_type == alg_exp_parser.OPERATOR:
                    raise SyntaxError("Invalid format before operator")
                prev_block_type = alg_exp_parser.OPERATOR
                block_start = i
                i += 1
                tokens.append(expr[block_start:i])
            elif c == ' ' or c == '\t':
                i += 1
            else:
                raise SyntaxError("Invalid char")
        return tokens

    @staticmethod
    def valid_alg_expr(tokens: list) -> bool:
        if len(tokens) % 2 != 1:
            return False
        for i in range(0, len(tokens)):
            if i % 2 == 1 and alg_exp_parser.get_expr_type(tokens[i]) != alg_exp_parser.OPERATOR:
                return False
            if i % 2 == 0 and alg_exp_parser.get_expr_type(tokens[i]) == alg_exp_parser.OPERATOR:
                return False
        return True

    @staticmethod
    def get_cal_node(expr: str = None, tokens: list = None):
        if not tokens:
            tokens = alg_exp_parser.expr_split(expr)
        if len(tokens) == 1:
            type = alg_exp_parser.get_expr_type(tokens[0])
            if type == alg_exp_parser.NUMBER:
                return cal_node(rational(tokens[0]))
            elif type == alg_exp_parser.OPERATOR or type == alg_exp_parser.UNKNOWN:
                raise SyntaxError("Invalid expressions")
            else:
                return alg_exp_parser.get_cal_node(tokens[0])
        if not alg_exp_parser.valid_alg_expr(tokens):
            raise SyntaxError("Invalid expressions")
        if len(tokens) == 3:
            return cal_node(tokens[1], left=alg_exp_parser.get_cal_node(expr=tokens[0]),
                            right=alg_exp_parser.get_cal_node(expr=tokens[2]))
        i = 1
        for i in range(1, len(tokens), 2):
            if tokens[i] in ['+', '-']:
                break
        return cal_node(tokens[i], left=alg_exp_parser.get_cal_node(tokens=tokens[0:i]),
                        right=alg_exp_parser.get_cal_node(tokens=tokens[i + 1:]))


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
        elif type(value) == rational:
            self._value = value
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
    def cal(top: object) -> int:
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
    def get_permutation(a: list):
        n = len(a)
        k = n - 2
        inc = -1
        n_factor = 1
        for i in range(1, n + 1):
            n_factor *= i
        i = 0
        while i < n_factor:
            a[k], a[k + 1] = a[k + 1], a[k]
            yield a.copy()
            k += inc
            i += 1
            if k == -1:
                inc = 1
                k = 0
                a[-2], a[-1] = a[-1], a[-2]
                yield a.copy()
                i += 1
            if k == n - 1:
                inc = -1
                k = n - 2
                a[0], a[1] = a[1], a[0]
                yield a.copy()
                i += 1

    @staticmethod
    def get_permutation_old(vlist: list) -> list:
        if len(vlist) == 1:
            return [vlist]
        rlist = {}
        r = []
        for i, v in enumerate(vlist):
            if v in rlist:
                continue
            rlist[v] = True
            nlist = vlist[0:i] + vlist[i + 1:]
            for sublist in cal_node.get_permutation(nlist):
                r.append([v] + sublist)
        return r

    @staticmethod
    def get_all_array(vlist: list, n: int) -> list:
        if len(vlist) < n:
            raise RuntimeError("Insufficient length")
        if n == 1:
            return [[x] for x in vlist]
        if len(vlist) == n:
            return [vlist]
        rlist = []
        for i in range(0, len(vlist) - n + 1):
            for sublist in cal_node.get_all_array(vlist[i + 1:], n - 1):
                rlist.append([vlist[i]] + sublist)
        return rlist

    @value.setter
    def value(self, value):
        self._value = value

    @left.setter
    def left(self, value):
        self._left = value

    @right.setter
    def right(self, value):
        self._right = value

    @staticmethod
    def get_formula(vlist: list) -> set:
        p_list = cal_node.get_permutation(vlist)
        cal_node_set = set()
        result_set = set()
        for v in p_list:
            tmp_list = cal_node.get_all_top_node(v)
            cal_node_set.update(tmp_list)
        for node in cal_node_set:
            # print(node)
            try:
                if cal_node.cal(node) == 24:
                    result_set.add(node)
            except:
                pass
        return result_set

    @staticmethod
    def is_resolvable(vlist: list) -> bool:
        p_list = cal_node.get_permutation(vlist)
        for v in p_list:
            tmp_list = cal_node.get_all_top_node(v)
            for node in tmp_list:
                if cal_node.cal(node) == 24:
                    return True
        return False


if __name__ == "__main__":
    for r in cal_node.get_formula([3, 3, 8, 8]):
        print(r)
    for vlist in cal_node.get_all_array(list(range(1, 10)), 4):
        result_set = cal_node.get_formula(vlist)
        if not result_set:
            print(vlist)
