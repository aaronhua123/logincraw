from lxml import etree


class Tree(list):
    def __init__(self, ele):
        super().__init__(ele)
        # self.ele = ele

    def first(self):
        return self[0] if len(self) > 0 else ""

class Xpath:
    def __init__(self, content):
        self.tree = etree.HTML(content)

    def path(self, _path):
        ele = self.tree.xpath(_path)
        return Tree(ele)

    def xpath(self, _path):
        return self.tree.xpath(_path)
