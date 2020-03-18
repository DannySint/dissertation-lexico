#credit to https://en.wikipedia.org/wiki/Trie
#credit to https://towardsdatascience.com/implementing-a-trie-data-structure-in-python-in-less-than-100-lines-of-code-a877ea23c1a1
from typing import Tuple
import sys
import string
import timeit

class TrieNode(object):
    """
    Our trie node implementation. Very basic. but does the job
    """
    
    def __init__(self, char: str):
        self.char = char
        self.children = []
        # Is it the last character of the word.
        self.word_finished = False
        # How many times this character appeared in the addition process
        self.counter = 1

    def pprint(self, indent="", last=True, stack=""):
        if indent != "":
            stack = stack + self.char

        sys.stdout.write(indent)
#        if last:
#            sys.stdout.write("┗╾") #cause issues with outputting to command line
#            indent += "  "
#        else:
#            sys.stdout.write("┣╾")
#            indent += "| "
        if last:
            sys.stdout.write("|_")
            indent += "  "
        else:
            sys.stdout.write("|--")
            indent += "| "

        sys.stdout.write("{} ({})".format(self.char, self.counter))
        if self.word_finished:
            print(" - {}".format(stack))
        else:
            print()

        for i, c in enumerate(self.children):
            c.pprint(indent, i == len(self.children) - 1, stack)

    def probability(self, str1, str2, debug=False) -> int:
        """
        Returns the probability of Pr_x(str2|str1) (where x is the trie - forward/backward)
        Probability of the forward tree of "s" given "report"
        Divide the frequency of words starting with "reports" 
        by
        the frequency of words starting "report"
        """
        value1 = find_prefix(self, str1)[1]
        if debug: print("Value of " + str1 + ": " + str(value1))
        value2 = find_prefix(self, str2)[1]
        if debug: print("Value of " + str2 + ": " + str(value2))
        return (value2 / value1)
        #return (str1 / str2)
        

    def add(self, word: str):
        """
        Adds a word to the Trie 
        if the word already exists just add to the counter
        if the word doesn't exist then create child nodes until it does exist
        """
        node = self
        
        for char in word: #loop over each character of a word
            found_in_child = False
            # Search for the character in the children of the present `node`
            for child in node.children:
                if child.char == char:
                    # We found it, increase the counter by 1 to keep track that another
                    # word has it as well
                    #child[char] = child.get(char, 0) + 1; 
                    child.counter += 1
                    # And point the node to the child that contains this char
                    node = child
                    found_in_child = True
                    break
            # We did not find it so add a new child
            if not found_in_child:
                new_node = TrieNode(char)
                node.children.append(new_node)
                # And then point node to the new child
                node = new_node
        # Everything finished. Mark it as the end of a word.
        node.word_finished = True


#TODO: Consider adding an existence check to speed up checking?
def find_prefix(root, prefix: str) -> Tuple[bool, int]:
    """
    Check and return 
      1. If the prefix exists in any of the words we added so far
      2. If yes then how many words actually have the prefix
    """
    node = root
    # If the root node has no children, then return False.
    # Because it means we are trying to search in an empty trie
    if not root.children:
        return False, 0
    for char in prefix:
        char_not_found = True
        # Search through all the children of the present `node`
        for child in node.children:
            if child.char == char:
                # We found the char existing in the child.
                char_not_found = False
                # Assign node as the child containing the char and break
                node = child
                break
        # Return False anyway when we did not find a char.
        if char_not_found:
            return False, 0
    # Well, we are here means we have found the prefix. Return true to indicate that
    # And also the counter of the last node. This indicates how many words have this
    # prefix
    return True, node.counter

def reverse(str):
    return str[::-1]

def words_from_file(file):
    words = []
    f = open(file, 'r', encoding="latin-1")
    for line in f:
        _, word = line.split()
        if (not any(char in string.punctuation for char in word)):
            words.append(word)

    return words


if __name__ == "__main__":
#    root = TrieNode('*')
#    add(root, "hackathon")
#    add(root, 'hack')
#    add(root, 'root')
#
#    print(find_prefix(root, 'hackathon'))
#    print(find_prefix(root, 'hac'))
#    print(find_prefix(root, 'hack'))
#    print(find_prefix(root, 'hackathon'))
#    print(find_prefix(root, 'ha'))
#    print(find_prefix(root, 'hammer'))
    file = "wordlist-2007-trimmed-a.eng"
    forwardtrie = TrieNode('*')
    words = words_from_file(file)
    for word in words:
        add(forwardtrie, word)
    #timeit.timeit(forwardtrie.pprint)
    forwardtrie.pprint()

#word = "a"
#regstr = '\A' + word + '\S'
#re.compile(regstr)
#print(re.match(regstr, "exaro"))
#print(re.match(regstr, "aaron"))
#print(re.match(regstr, "aron"))
#print(re.match(regstr, "raron"))

#wordlist = ["a", "aa", "aas", "aasar", "aaser", "aba", "abacos"]




