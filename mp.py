import re
import math
stop_words = open("Hindi_StopWords.txt", "r", encoding="utf-8").read()
list = []
def lemmatizer(word):
    if word == "खोलता" or word == "खोला":
        return "खोल"
    if word == "कौआ" or word == "कौए":
        return "कौआ"
    if word == "पंखों":
        return "पंख"
    else:
        return word
    
def preprocess(str):
    words = str.split()
    filtered_words = [lemmatizer(re.sub(r"।|!|,|\?|-", "", word)) for word in words if word not in stop_words]
    return filtered_words

def jaccard_sim(w1, w2):
    trigrams1=[]
    for i in range(len(w1)-2):
        t=(w1[i],w1[i+1],w1[i+2])
        trigrams1.append(t)

    s=0
    trigrams2=[]
    for i in range(len(w2)-2):
        t=(w2[i],w2[i+1],w2[i+2])
        trigrams2.append(t)
        if t in trigrams1:
            s+=1

    J=s/(len(trigrams1)+len(trigrams2)) 
    return J

def calculate_tf(words):
    word_count = len(words)
    tf_dict = {}
    
    for word in words:
        tf_dict[word] = tf_dict.get(word, 0) + 1 / word_count
    
    return tf_dict

def calculate_idf(w1, w2):
    N = 2
    idf_dict = {}
    
    for word in w1:
        idf_dict[word] = idf_dict.get(word, 0) + 1
    
    for word in w2:
        idf_dict[word] = idf_dict.get(word, 0) + 1
    
    for word, count in idf_dict.items():
        idf_dict[word] = math.log(N / count)
    
    return idf_dict

def calculate_tfidf(tf, idf):
    tfidf = {}
    for word, tf_value in tf.items():
        tfidf[word] = tf_value * idf.get(word, 0)
    return tfidf

def calculate_cosine_similarity(tfidf1, tfidf2):
    dot_product = sum(tfidf1[word] * tfidf2[word] for word in tfidf1 if word in tfidf2)
    magnitude1 = math.sqrt(sum(tfidf1[word] ** 2 for word in tfidf1))
    magnitude2 = math.sqrt(sum(tfidf2[word] ** 2 for word in tfidf2))
    return dot_product / (magnitude1 * magnitude2)

def start(docs):
    list.clear()
    # str1 = open(docs[0], "r", encoding="utf-8").read()
    # str2 = open(docs[1], "r", encoding="utf-8").read()
    str1 = str(docs[0], encoding="utf-8")
    str2 = str(docs[1], encoding="utf-8")

    filtered_words1 = preprocess(str1)
    filtered_words2 = preprocess(str2)
    print("\nStopword removal:\n",filtered_words1)
    print("\nStopword removal:\n",filtered_words2)

    J = jaccard_sim(filtered_words1, filtered_words2)
    print("Jaccard Similarity:", J)
    list.append(round(J,3))

    idf_dict = calculate_idf(filtered_words1, filtered_words2)

    tf1 = calculate_tf(filtered_words1)
    tf2 = calculate_tf(filtered_words2)
            
    tfidf1 = calculate_tfidf(tf1, idf_dict)
    tfidf2 = calculate_tfidf(tf2, idf_dict)

    similarity = calculate_cosine_similarity(tfidf1, tfidf2) * 100
    list.append(round(similarity,2))
    print(f"Plagiarism found using TF-IDF: {similarity:.2f}")

    
