#print(string.punctuation)
PATTERN = re.compile("[\d{}]+$".format(re.escape(string.punctuation)))
#print(bool(PATTERN.match("")))
#print(bool(PATTERN.match("'''")))
#print(bool(PATTERN.match("rek'sai")))

#is_prefix("c", "corresponded")
#is_suffix("corresponde", "corresponded")

#backward_trie.probability( reverse("eports"), reverse("ports"))

#report = "reports"
#print(forward_trie.probability("r", report))
#print(forward_trie.probability("re", report))
#print(forward_trie.probability("rep", report))
#print(forward_trie.probability("repo", report))
#print(forward_trie.probability("repor", report))
#print(forward_trie.probability("report", report))
#print(forward_trie.probability("reports", report))
#print(forward_trie.probability("repor", "report"))
#print(forward_trie.probability("correspon", "correspond"))

#corr = "corresponded"
#print(forward_trie.probability("c", corr))
#print(forward_trie.probability("co", corr))
#print(forward_trie.probability("cor", corr))
#print(forward_trie.probability("corr", corr))
#print(forward_trie.probability("correspond", corr))
#print()
#print(forward_trie.probability(corr, "c"))
#print(forward_trie.probability(corr, "co"))
#print(forward_trie.probability(corr, "cor"))
#print(forward_trie.probability(corr, "corr"))
#print(forward_trie.probability(corr, "correspond"))

def pruning_testing():
    word_score = {"s": 5000, "ers": 3000, "er": 4000};
    word_score = prune_affixes()
    print(word_score)


#is_suffix("report", "reports");
#is_prefix("r", "reports") #WRONG Look Down for what it should be.
#is_prefix(reverse("reports")[:1], reverse("reports"))
    
#words = ["re", "ports", "reports", "port", "s"]
#word_score["reports"] = 19; word_score["re"] = 19; word_score["ports"] = 19;
#print("isSplittable(reports)? " + str(isSplittable("reports", len("reports"))));
    
    
#################################### LEXO TREE #################################### 
    #print(forward_trie.probability("report", "reports")) #should this be between 0 and 1
    #print(forward_trie.probability("e", "correspond")) #should this be between 0 and 1
    
#print(backward_trie.probability( "s", "", debug))
#print(backward_trie.probability( "st", "s", debug))
#print(backward_trie.probability( "str", "st", debug))
#print(backward_trie.probability( "stro", "str", debug))
#print(backward_trie.probability( "strop", "stro", debug))
#print(backward_trie.probability( "strope", "strop", debug))
#print(backward_trie.probability( "stroper", "strope", debug))