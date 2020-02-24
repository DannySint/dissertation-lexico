"""
class Trie:
    def find(self, node, key):
        """Find value by key in node"""
        for char in key:
            if char in node.children:
                node = node.children[char]
            else: 
                return None
        return node.value

    def insert(self, node, key, counter):
        """Insert key/value pair into node."""
        for char in key:
            if char not in node.children:
                node.children[char] = Node([], char, 0)
            elif char in node.children:
                node.children[char].update_count
            node = node.children[char]
        node.value = value
"""

nodelist = []
abacos = Node([], "abacos", 0)
aba = Node(["abacos"], "aba", 1)
aasar = Node([], "aasar", 0)
aaser = Node([], "aaser", 0)
aas = Node([aasar, aaser], "aas", 2)
aa = Node([], "aa", 0)
a = Node([aa, aba],"a", 2) #should value be 6?


#consider removing any matches from the wordlist to improve performance
def build_lexicographic_tree(wordlist): #need to remove the frequencies first though
    for word in wordlist:
        regstring = '\A' + word + '\S' #beginning of word, word, anything after
        regex = re.compile(regstring)
        #if word #
        #re.match (search beginning of string)
        # do we need to create a dictionary of the children?
        
        nodelist.append(Node({}, "word", ) )


build_lexicographic_tree(wordlist)