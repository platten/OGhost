"""trie.py: Optimal Ghost Trie data structure."""

__author__      = "Paul Pietkiewicz"
__copyright__   = "Copyright 2012, Paul Pietkiewicz"
__license__     = "GPL"
__version__     = "0.1"
__email__       = "paul.pietkiewicz@acm.org"


class IncompleteWord(Exception):
    pass


class Node(object):
    """Trie node"""
    def __init__(self, parent, key, nodes, value, weight, height):
        self.parent = parent
        self.key = key
        self.nodes = nodes
        self.value = value
        self.weight = weight
        self.height = height


class Trie(object):
    """Prefix tree/trie implementation.

    When trying to access a node without a value, but with children,
    IncompleteWord will be raised. If there are no children, KeyError
    will be raised.
    """

    def __init__(self):
        self.root = Node(None, None, {}, None, 0, 0)

    def __setitem__(self, key, value):
        node = self.root
        height = 0
        node.weight += 1

        for char in key:
            height += 1
            if char in node.nodes:
                node = node.nodes[char]
                node.weight += 1
            else:
                node.nodes[char] = Node(node, char, {}, None, 1, height)
                node = node.nodes[char]

        node.value = value

    def _get_node(self, key):
        node = self.root

        for char in key:
            try:
                node = node.nodes[char]
            except KeyError:
                raise KeyError(key)
        return node

    def __getitem__(self, key):
        node = self._get_node(key)
        if node.value is None:
            if node.nodes:
                raise IncompleteWord()
            else:
                raise KeyError(key)
        return node.value

    def get_weight_dict(self, key=None):
        """Returns a dict containing the child node's branch weight"""
        weight_dict = {}

        if key:
            node = self._get_node(key)
        else:
            node = self.root

        for key in node.nodes.keys():
            weight = node.nodes[key].weight
            weight_dict.setdefault(weight, list()).append(key)

        return weight_dict

    def get_max_child_height_dict(self, key=None):
        """Returns a dict containing the maximum node depths of a given key's
        children"""
        height_dict = {}

        if key:
            node = self._get_node(key)
        else:
            node = self.root

        for key in node.nodes.keys():
            height = self._height(node.nodes[key]) - node.height
            height_dict.setdefault(height, list()).append(key)

        return height_dict

    def _height(self, node):
        """Recursive internal method to determine the maximum node depth"""
        if node.value is not None and not node.nodes:
            return node.height
        elif node.value is not None and node.nodes:
            return max(flatten([node.height, ] +
                               map(self._height, node.nodes.values())))
        elif node.value is None and node.nodes:
            return max(flatten(map(self._height, node.nodes.values())))
        else:
            raise Exception('should never have gotten here')

    def immediate_children(self, key):
        """Return a dict of the immediate children of the given key"""
        node = self._get_node(key)
        return dict((key, node.nodes[key].value)
            for key in node.nodes
                if node.nodes[key].value is not None)

    def _r_children(self, node):
        """Recursive internal method to determine all the given node's
        children"""
        if node.value is not None and not node.nodes:
            return [node.value, ]
        elif node.value is not None and node.nodes:
            return [node.value, ] + map(self._r_children, node.nodes.values())
        elif node.value is None and node.nodes:
            return map(self._r_children, node.nodes.values())
        else:
            raise Exception('should never have gotten here')

    def all_children(self, key=None):
        """Return a list of all the children for a given key."""
        if key:
            node = self._get_node(key)
        else:
            node = self.root
        if node.nodes:
            return flatten(map(self._r_children, node.nodes.values()))
        return []

    def add_word(self, word):
        self.__setitem__(word, word)


def flatten(nested):
    """Recursively flatten arbitrarily nested lists"""
    result_list = []

    for element in nested:
        if hasattr(element, "__iter__") and not\
        isinstance(element, basestring):
            result_list.extend(flatten(element))
        else:
            result_list.append(element)

    return result_list
