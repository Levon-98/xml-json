import xmltodict
import json
from xml.etree import ElementTree


class Node:
    def __init__(
        self,
        name: str,
        parent=None,
        metadata: dict = None,
        value: str = None,
        child: list = None,
    ):
        self.name = name
        self.parent = parent
        self.value = value
        self.child = child
        self.metadata = metadata
        if self.child is None:
            self.child = []
        if self.parent is not None:
            self.parent.add_child(self)

    def __str__(self):
        return str(self.__dict__)

    def add_child(self, node_1):
        self.child.append(node_1)


class Tree:
    def __init__(self, root, tree_type: str):
        self.root = root
        self.tree_type = tree_type
        self.root_xml = Tree._xml_tree(self.root, ElementTree.Element(self.root.name))
        if self.tree_type == "json":
            self.json_ord_dict = xmltodict.parse(
                ElementTree.tostring(self.root_xml, encoding="unicode")
            )

    @staticmethod
    def _xml_tree(root, root_name):
        for i in root.child:
            if i.child == []:
                ElementTree.SubElement(root_name, i.name).text = i.value
            else:
                Tree._xml_tree(i, ElementTree.SubElement(root_name, i.name))
        return root_name

    def result(self):
        if self.tree_type == "json":
            return json.dumps(self.json_ord_dict[self.root.name])
        elif self.tree_type == "xml":
            return ElementTree.tostring(self.root_xml).decode("utf-8")

    def xml_to_json(self):
        xml_json = xmltodict.parse(
            ElementTree.tostring(self.root_xml, encoding="unicode")
        )
        return json.dumps(xml_json[self.root.name])

    def json_to_xml(self):
        tree_xml = ElementTree.ElementTree(self.root_xml)
        return tree_xml

    def write(self, path: str):
        if self.tree_type == "json":
            with open(path, "w") as jf:
                jf.write(json.dumps(self.json_ord_dict["data"], indent=4))
        elif self.tree_type == "xml":
            tree_xml = ElementTree.ElementTree(self.root_xml)
            tree_xml.write(path)


if __name__ == "__main__":

    root = Node("data")
    node_1 = Node("data_1", parent=root, value="1")
    node_2 = Node("data_2", parent=root)
    sub_node2_1 = Node("data_2_sub", parent=node_2, metadata={"id": 0}, value="1")
    sub_node2_2 = Node("data_2_sub", parent=node_2, metadata={"id": 1}, value="2")
    sub_node2_3 = Node("data_2_sub", parent=node_2, metadata={"id": 2}, value="5")
    node_3 = Node("data_3", parent=root)
    sub_node3_1 = Node("sub_d_1", parent=node_3, value="3")
    sub_node3_2 = Node("sub_d_2", parent=node_3, value="5")

    xml_tree_1 = Tree(root, "xml")
    json_tree_1 = Tree(root, "json")

    print("xml to json >>>", xml_tree_1.xml_to_json())
    print("json to xml >>>", json_tree_1.json_to_xml())

    json_tree_1.write("json.json")
    xml_tree_1.write("xml.xml")

    print(json_tree_1.result())
    print(xml_tree_1.result())
