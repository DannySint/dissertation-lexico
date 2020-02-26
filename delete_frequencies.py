def words_from_file(data, output) -> (list, set):
    f = open(data, 'r', encoding="latin-1")
    o = open(output, 'w',)
    for line in f:
        _, word = line.split()
#        words.append(word)
        o.write(word + "\n")
data = "wordlist-2007-trimmed.eng"
output = "wordlist-2007-trimmed-words.eng"
words_from_file(data, output)