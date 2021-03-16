from random import random
from math import sqrt
from time import time
import re
from os import listdir
from os.path import isfile, join
from nltk.corpus import stopwords

testfiles = [f for f in listdir("./test/") if isfile(join("./test/", f))]

def counter_onetoone(list_of_words):
    counter_dic = {}
    for word in list_of_words:
        if word not in counter_dic: counter_dic[word] = 0
        counter_dic[word] += 1
    return counter_dic

def counter_onetofour(list_of_words, limit=0.25):
    counter_dic = {}
    for word in list_of_words:
        if word not in counter_dic: counter_dic[word] = 0
        if random() < 0.25:
            counter_dic[word] += 1
    return counter_dic

def counter_logsqrt2(list_of_words):
    counter_dic = {}
    base = sqrt(2)
    cache_results = {}
    for word in list_of_words:
        if word not in counter_dic: counter_dic[word] = 0
        counter = counter_dic[word]
        if counter not in cache_results: cache_results[counter] = 1/(base**counter)
        chance = cache_results[counter] 
        if random() < chance:
            counter_dic[word] += 1
    return counter_dic

def counter_stats(counter, real_value, est_function):
    avg = sum(counter)/len(counter)
    max_dev = max([abs(avg-i) for i in counter])
    mean_dev = sum([abs(avg-i) for i in counter])/len(counter)
    variance = sum([(avg-i)**2 for i in counter])/len(counter)
    std_dev = sqrt(variance)

    mean_err = sum([abs(est_function(i) - real_value)/real_value for i in counter])/len(counter) 
    mean_acc_ratio = sum([est_function(i)/real_value for i in counter])/len(counter) 

    return min(counter), max(counter), avg, max_dev, mean_dev, std_dev, variance, mean_err, mean_acc_ratio

def expect_prob_counter1to4(exp_value, prob=0.25):
    print("Expected Value:", exp_value*prob)
    print("Variance:", exp_value*(prob - prob**2))
    print("Standard Deviation:", sqrt(exp_value*(prob - prob**2)))
    print()

def get_results(file, num_trials, stopwords, file_to_write):
    with open(file, "r") as f:
        text = f.read().lower()
    text = re.sub('[.!?\-,()«»"\'\*\[\]:”“]+', ' ', text)
    list_of_words = [word for word in text.split() if word not in stopwords]

    counter2_results = []
    counter3_results = []

    for i in range(num_trials):
        counter2_results.append(counter_onetofour(list_of_words))
    
    start = time()
    for i in range(num_trials):
        counter3_results.append(counter_logsqrt2(list_of_words))
    end = time()
    print("Total time {:.3f}".format(end - start))

    real_counter = counter_onetoone(list_of_words)
    top5_words = [word for word in sorted(list(real_counter.keys()), key=lambda t: real_counter[t])][-5:]
    for word in top5_words:
        print("Results for", word, "with", real_counter[word])
        #   expect_prob_counter1to4(real_counter[word], prob=0.25)
        result_fix = counter_stats([dic[word] for dic in counter2_results], real_counter[word], lambda x: x*4)
        with open(to_write_name + "-fix-prob.txt", "a") as writer:
            writer.write("{:d},{:s},".format(num_trials, word))
            writer.write("{:d},{:d},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f}\n".format(
                *result_fix
            ))
        
        result_dec = counter_stats([dic[word] for dic in counter3_results], real_counter[word], lambda x: (sqrt(2)**x - sqrt(2) + 1)/(sqrt(2) - 1))
        with open(to_write_name + "-dec-prob.txt", "a") as writer:
            writer.write("{:d},{:s},".format(num_trials, word))
            writer.write("{:d},{:d},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f}\n".format(
                *result_dec
            ))

language_dictionary = {
    'alice-in-wonderland-de.txt': stopwords.words('german'),
    'alice-in-wonderland-eng.txt': stopwords.words('english'),
    'alice-in-wonderland-fin.txt': stopwords.words('finnish'),
    'alice-in-wonderland-fr.txt': stopwords.words('french'),
    'alice-in-wonderland-it.txt': stopwords.words('italian')
}

for fi in testfiles:
    print(fi)
    to_write_name = "./results/" + fi.split('.')[0] + "-results"
    with open(to_write_name + "-fix-prob.txt", "w") as writer:
        writer.write("{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s}\n".format(
            "Num Trials", "Word", "Min val", "Max val", "Mean Value", "Max Dev", "Mean Dev", "Std Dev", "Var", "Mean Rel Error", "Mean acc ratio"
        ))
    with open(to_write_name + "-dec-prob.txt", "w") as writer:
        writer.write("{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s}\n".format(
            "Num Trials", "Word", "Min val", "Max val", "Mean Value", "Max Dev", "Mean Dev", "Std Dev", "Var", "Mean Rel Error", "Mean acc ratio"
        ))
    for i in range(1,5):
        get_results("./test/" + fi, 10**i, language_dictionary[fi], to_write_name)
        
