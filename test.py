
import re
import os
import time
import datetime
from collections import defaultdict
from nltk.tokenize import word_tokenize
import nltk


import io
import math
from collections import Counter


start_time= datetime.datetime.now()
def downcased_tokens(text, each_file):
    try:
        # remove HTML tags using regex
        text = re.sub(r'<[^>]*>', '', text)
    except Exception as e:
        print(f'Error processing file {each_file}: {e}')
        return []
    # tokenize the text into words
    nltk.download('punkt')
    tokens = word_tokenize(text)
    # downcase the tokens
    tokens = [tokenize.lower() for tokenize in tokens]
    return tokens

def read(directory_path):
    documents = []
    for each_file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, each_file)
        if os.path.isfile(file_path):
            with open(os.path.join(directory_path, each_file), 'r', encoding='') as f:
                ele = f.read()
                documents.append(downcased_tokens(ele, each_file))
    return documents



def tokenize(directory_path, output):
    all_tokens = []
    size=os.path.getsize(directory_path)
    for each_file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, each_file)
        if os.path.isfile(file_path):
            with open(os.path.join(directory_path, each_file), 'r', encoding='ISO-8859-1') as f:
                ele = f.read().lower()
                tokens = downcased_tokens(ele, each_file)
                tokens = [tokenize for tokenize in tokens if tokenize.isalpha()]
            with open(os.path.join(output, each_file), 'w') as f:
                f.write("\n".join(tokens))
            all_tokens.extend(tokens)
    
    dict = {}
    for tokenize in all_tokens:
        if tokenize in dict:
            dict[tokenize] += 1
        else:
            dict[tokenize] = 1
    
    token_sorted = sorted(dict.items(), key=lambda x: x[0])
    with open(os.path.join(output, 'token_sorted.txt'), 'w') as f:
        for tokenize, count in token_sorted:
            f.write(f'{tokenize} {count}\n')
    frequency_sorted = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    with open(os.path.join(output, 'frequency_sorted.txt'), 'w') as f:
        for tokenize, count in frequency_sorted:
            f.write(f'{tokenize} {count}\n')
    elapsed = datetime.datetime.now() - start_time
    print(int(elapsed.total_seconds()*1000))
    size1=os.path.getsize(output)
    final=size+size1
    print(int(size))



if __name__=="__main__":
    input = "/Users/hemanthrao/Desktop/files"
    output = "/Users/hemanthrao/Desktop/output"
    tokenize(input, output)
    