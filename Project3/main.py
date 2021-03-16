from os import listdir
from os.path import isfile, join

testfiles = ["./test/" + f for f in listdir("./test/") if isfile(join("./test/", f))]
not_allowed_letters = ",.-;:_<>[](){}*+ \n"

def exact_count(text):
    count = {}
    for letter in text:
        if letter in not_allowed_letters: continue
        if letter not in count: count[letter] = 0
        count[letter] += 1
    return count
    
def space_saving_count(text, num_elements):
    count = {}
    n = 0
    for letter in text:
        n += 1
        if letter in not_allowed_letters: continue
        if letter in count: count[letter] += 1
        elif len(count) <= num_elements: count[letter] = 1
        else:
            min_count = count.pop(min(count, key=count.get))
            count[letter] = min_count + 1
    return count

def calc_acc(exact_freq, ss_freq, max_count):
    top_letters = [letter for letter, freq in sorted(list(exact_freq.items()), key=lambda t: t[1], reverse=True)][:max_count]
    common_items = set(top_letters) & set(ss_freq.keys()) 
    return len(common_items)/max_count

def analyse_all_texts_with_k_elems(k):
    results = []
    for file_name in testfiles:
        with open(file_name, "r") as filereader:
            text = filereader.read()
        exact_freq = exact_count(text)
        ss_count = space_saving_count(text, k)
        acc = calc_acc(exact_freq, ss_count, k)
        results.append(acc)
    return results


with open("./test/alice-in-wonderland-eng.txt", "r") as filereader:
    test_text = filereader.read()
print("Top 10 in the english version of alice in wonderland")
exactTop10 = [(letter, freq) for letter, freq in sorted(list(exact_count(test_text).items()), key=lambda t: t[1], reverse=True)][:10]
space_saving_top10 = [(letter, freq) for letter, freq in sorted(list(space_saving_count(test_text, 10).items()), key=lambda t: t[1], reverse=True)]
print("{:^15s}{:^15s}".format("Exact Counter", "Space Saving"))
for i in range(10):
    print("{:^15s}{:^15s}".format(
        "{:s}({:d})".format(*exactTop10[i]),
        "{:s}({:d})".format(*space_saving_top10[i]),
    ))

with open("results.csv", "w") as filewriter:
    header = "Max Elements," + ",".join([f[7:-4] for f in testfiles])
    filewriter.write(header)
    for max_count in range(2, 22, 2):
        max_count_results = [max_count] + analyse_all_texts_with_k_elems(max_count)
        filewriter.write(",".join([str(c) for c in max_count_results]) + "\n")
