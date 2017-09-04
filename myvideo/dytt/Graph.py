# -*- coding:utf-8 -*-


class Graph(object):

    def __init__(self, max_depth):
        self.max_dept = max_depth
        self.readyList = []
        self.depth_size = {}

    def add_node(self, nodes, filter_list=None, url_format=None):
        while len(nodes) > 0:
            node = nodes.pop(-1)
            if (filter_list is None or node not in filter_list) and node not in self.readyList:
                if url_format:
                    url_format(node)
                self.readyList.append(node)

    def get_node(self):
        if len(self.readyList) > 0:
            return self.readyList.pop(-1)

if __name__ == '__main__':
    g = Graph()
    # root_url = "www.baidu.com"
    g.add_node(["1"])
