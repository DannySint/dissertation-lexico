
#is_prefix("c", "corresponded")
#is_suffix("corresponde", "corresponded")


#report = "reports"
#print(probability(forward_trie, "r", report))
#print(probability(forward_trie, "re", report))
#print(probability(forward_trie, "rep", report))
#print(probability(forward_trie, "repo", report))
#print(probability(forward_trie, "repor", report))
#print(probability(forward_trie, "report", report))
#print(probability(forward_trie, "reports", report))
#print(probability(forward_trie, "repor", "report"))
#print(probability(forward_trie, "correspon", "correspond"))

#corr = "corresponded"
#print(probability(forward_trie, "c", corr))
#print(probability(forward_trie, "co", corr))
#print(probability(forward_trie, "cor", corr))
#print(probability(forward_trie, "corr", corr))
#print(probability(forward_trie, "correspond", corr))
#print()
#print(probability(forward_trie, corr, "c"))
#print(probability(forward_trie, corr, "co"))
#print(probability(forward_trie, corr, "cor"))
#print(probability(forward_trie, corr, "corr"))
#print(probability(forward_trie, corr, "correspond"))

def pruning_testing():
    word_score = {"s": 5000, "ers": 3000, "er": 4000};
    word_score = prune_affixes()
    print(word_score)


#is_suffix("report", "reports");
#is_prefix("r", "reports")
    
#words = ["re", "ports", "reports", "port", "s"]
#word_score["reports"] = 19; word_score["re"] = 19; word_score["ports"] = 19;
#print("isSplittable(reports)? " + str(isSplittable("reports", len("reports"))));
    
    
#################################### LEXO TREE #################################### 
    #print(probability(forward_trie, "report", "reports")) #should this be between 0 and 1
    #print(probability(forward_trie, "e", "correspond")) #should this be between 0 and 1