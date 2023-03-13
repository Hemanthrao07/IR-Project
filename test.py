import re
import os
import numpy as np
import matplotlib.pyplot as plt 
#importing time and datetime for processing time calculation
import time
import datetime
from collections import defaultdict
#using nltk.tokenize class for tokenization
from nltk.tokenize import word_tokenize
import nltk
import io
import math
from collections import Counter
nltk.download('gutenberg')
#making note of the starttime of processing
start= datetime.datetime.now()
print(start)
def tokenise(dir_path, output_dir):
    alltokens = []
    k1=1.25
    b=0.75
    size=os.path.getsize(dir_path)
    DF,q=DFcount(dir_path)
    N = len([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])
    avgdl=q/N
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        if os.path.isfile(file_path):
            with open(os.path.join(dir_path, file), 'r', encoding='ISO-8859-1') as f:
                tf={}
                words = f.read().lower()
                token = downcased_tokens(words, file)
                for i in token:
                    if i not in tf.keys():
                        tf[i]=1
                    else:
                        tf[i]+=1
                n=len(token)
                token=set(token)
                with open(os.path.join(output_dir, f'{file}.txt'), 'a') as s:
                    for i in token:
                        idf = math.log((N-DF[i]+0.5)/(DF[i] + 0.5))
                        tf_idf = tf[i]/n*idf
                        num=idf*(tf[i]/n)*(k1+1)
                        den=tf[i]+(k1*(1-b+b*(N/avgdl)))
                        score=num/den
                        s.write(f'{i} {tf[i]} {tf_idf} {score}\n')
                alltokens.extend(token)
def download_punkt():
    # check if punkt package is already downloaded
    if not nltk.corpus.gutenberg.fileids():
        nltk.download('punkt')

def DFcount(dir_path):
    n=0
    DF={}
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        if os.path.isfile(file_path):
            with open(os.path.join(dir_path, file), 'r', encoding='ISO-8859-1') as f:
                words = f.read().lower()
                token = downcased_tokens(words, file)
                n+=len(token)
                token=set(token)
                for term in token:
                    if term not in DF.keys():
                        DF[term]=1
                    else:
                        DF[term]+=1
    return DF,n


    
    freq = {}
    for t in alltokens:
        if t in freq:
            freq[t] += 1
        else:
            freq[t] = 1
    
    #sorting the words alphabetically
    sort_by_token = sorted(freq.items(), key=lambda x: x[0])
    freq1=[]
    with open(os.path.join(output_dir, 'sorted_by_token.txt'), 'w') as f:
        for token, count in sort_by_token:
            f.write(f'{token} {count}\n')
            freq1.append(count)
    freq1.sort(reverse=True)
    rank = np.arange(1, len(freq1)+1)
    rank_freq = np.multiply(rank ,freq1)
    plt.loglog(rank_freq)
    plt.xlabel('Rank')
    plt.ylabel('Frequency')
    plt.title('Rank to Frequency')
    plt.show()
    #sorting the words by the frequency of their occurance
    sort_by_frequency = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    with open(os.path.join(output_dir, 'sorted_by_frequency.txt'), 'w') as f:
        for token, count in sort_by_frequency:
            f.write(f'{token} {count}\n')
    #this gives us the time of processing the files
    end = datetime.datetime.now() - start
    print(int(end.total_seconds())*1000)
    #this gives the size of the output directory
    size_1=os.path.getsize(output_dir)
    final=size+size_1
    print(int(size),int(size_1),int(final))

#This function returns all the token of a file
def downcased_tokens(text, each_file):
    try:
        text = re.sub(r'<[^>]*>', '', text)
    except Exception as e:
        print(f'Error while processing the present file {file}: {e}')
        return []
    #tokenizing the words using the simple_preprocess
    token = word_tokenize(text)
    # downcasing the words using lower() method
    token=[]
    stop_words=stopwords()
    for i in token:
        token.append(i.lower())
    token = [token for token in token if token.isalpha() and token not in stop_words and len(token)>1 and token.count(token)!=1]
    return token

#input and output files path
in_dir= r"/Users/hemanthrao/Desktop/untitled folder/input"
out_dir = r"/Users/hemanthrao/Desktop/untitled folder/ouput2"
tokenise(in_dir, out_dir)
