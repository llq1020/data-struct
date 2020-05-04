import random

MAX_LEVEL = 16


class Node:
    """
    跳表节点类
    """

    def __init__(self, level, key=None, value=None):
        self.key = key
        self.value = value
        self.forwards = [None] * level


def random_level():
    level = 0
    for i in range(-1, MAX_LEVEL):
        level += random.randint(0, 1)
    return level


class SkipList:
    """
    跳表
    """

    def __init__(self):
        self.head = Node(level=MAX_LEVEL)
        self.level = 0
        self.size = 0

    def insert(self, key, value):
        """
        新增
        找出每一级要更新的节点
        通过随机数确定更新的级数
        如果大于当前跳表级别  跳表扩张一级
        :param key:    key
        :param value:  value
        :return:       insert res
        """
        if key is None:
            return False
        update = [None] * MAX_LEVEL
        try:
            for i in range(self.level - 1, -1, -1):
                q = self.head
                while q.forwards[i] and q.forwards[i].key <= key:
                    q = q.forwards[i]
                if q and q.key == key:
                    return False
                update[i] = q
            ins_level = random_level()
            if ins_level > self.level:
                update[self.level] = self.head
                ins_level = self.level + 1
                self.level = ins_level
            ins_node = Node(level=ins_level, key=key, value=value)
            for i in range(ins_level):
                ins_node.forwards[i] = update[i].forwards[i]
                update[i].forwards[i] = ins_node
            self.size += 1
        except Exception as e:
            print(e)
            return False
        return True

    def find(self, key):
        """
        寻找某个key对应value
        :param key: key
        :return: value
        """
        if not key:
            return None
        p = self.head
        for i in range(self.level - 1, -1, -1):
            while p.forwards[i] and p.forwards[i].key <= key:
                if p.forwards[i].key == key:
                    return p.forwards[i].value
                p = p.forwards[i]
        return None

    def delete(self, key):
        """
        同新增  依然是要找到对应节点的前驱节点
        :param key: key
        :return: t/f
        """
        if not key:
            return False
        update = [None] * MAX_LEVEL
        q = None
        for i in range(MAX_LEVEL - 1, -1, -1):
            q = self.head
            while q.forwards[i] and q.forwards[i].key < key:
                q = q.forwards[i]
            update[i] = q
        del_node = q.forwards[0]
        del q
        if del_node and del_node.key == key:
            for i in range(self.level):
                if update[i] and update[i].forwards[i] == del_node:
                    del_node.forwards[i] = None
                    update[i].forwards[i] = update[i].forwards[i].forwards[i]
            del del_node
            for i in range(self.level - 1, -1, -1):
                if self.head.forwards[i] is None:
                    self.level -= 1
            self.size -= 1
            return True
        else:
            return False

    def print_all(self):
        for i in range(self.level - 1, -1, -1):
            p = self.head
            while p.forwards[i]:
                print(str(p.forwards[i].key) + "-->", end="")
                p = p.forwards[i]
            print('\r\n')


if __name__ == '__main__':
    data = [item for item in range(1000)]
    sl = SkipList()
    for item in data:
        sl.insert(item, "测试")
    sl.print_all()
    print(sl.find(467))
