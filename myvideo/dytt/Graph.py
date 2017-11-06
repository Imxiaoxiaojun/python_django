# -*- coding:utf-8 -*-


class Graph(object):

    def __init__(self, max_depth):
        self.max_dept = max_depth
        self.readyList = []
        self.depth_size = {}

    def add_node(self, nodes, url_format=None):
        while len(nodes) > 0:
            node = nodes.pop(-1)
            if url_format:
                node = url_format(node)
                if node is None:
                    continue
            self.readyList.append(node)

    def get_node(self):
        if len(self.readyList) > 0:
            return self.readyList.pop(-1)
        else:
            return None

if __name__ == '__main__':
    g = Graph()
    # root_url = "www.baidu.com"
    g.add_node(["1"])
