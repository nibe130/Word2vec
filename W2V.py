#DO not padd the input file.
#i pad it with a # in the end and the begininng
#I pad it with only one layer irrespective of the window size



import numpy as np
import sys

la = np.linalg


# w_l===word list with lower case and uppper case text


# converts all the words to lower case
# remove repeated words
# initializes the cooccurence matrix to zeroes
# initializes window size to 2
def preprocessing():
    uniques = []
    window = 2

    # Lower caseconversion
    w_l=open(sys.argv[1]).read().split()
    corpus = [x.lower() for x in w_l]
    corpus.insert(0, "#")
    corpus.insert(len(corpus), "#")
    myarray = np.asarray(corpus)

    # remove repeated words
    for item in myarray:
        if item in uniques:
            continue
        else:
            uniques.append(item)

    size = len(uniques)
    zconc = np.zeros(shape=(size, size))
    
    return corpus, uniques, zconc


# idenity the context words within the window for each word
def ip(corpus, i, index):
    w_w = []
    window = int(sys.argv[2])
    left = index - window
    right = index + window + 1

    # when there are no words on the left
    if left < 0:
        w_w.extend(corpus[0:index])
        w_w.extend(corpus[index + 1: right])

    # when there are no words on the right
    if right >= len(corpus) :
        w_w.extend(corpus[left:len(corpus)])
        w_w.remove(i)

    # when there are words on the left anf right [eqaul to window size]
    if left >= 0 and right < len(corpus):
        w_w.extend(corpus[left:right])
        w_w.remove(i)

    return w_w


# find how many times each word is repated in context for each target word and update the concurrency matrix
def cooccurence(list2, corpus, uniques, zconc):
    n_i = 0
    for i in uniques:
      
      while (corpus.__contains__(i)):
            index_val = corpus.index(i)
            
            for element in list2[index_val]:
                
                zconc[n_i][uniques.index(element)] = zconc[n_i][uniques.index(element)] + 1
                # conc[uniques.index(element)][n_i] = conc[uniques.index(element)][n_i] + 1
                if list2.__contains__(element):
                    list2.remove(element)
            corpus[index_val] = '$'
      n_i = n_i + 1
    return zconc


#dimensionality reduction using SVD
# take the U matrix
# use 5 decimal precision
def SVD(conc):
    u, s, vh = la.svd(conc, full_matrices=False)
   
    x = np.around(u, decimals=5)
   
    return x

#normalize the concurrancy matrix
def normalize(conc):
    ij=0
    for row in conc:
        s=sum(row)
        ii=0
        for item in row:
            conc[ij][ii]=conc[ij][ii]/s
            ii=ii+1
        ij=ij+1
   
    return conc



#pre processing
corpus, uniques, zconc = preprocessing()

list2 = []
index = 1
for i in corpus:
     if i != '#':
        x = ip(corpus, i, index)
        list2.append(x)
        index = index + 1
# print(list2)
#remove padding
while corpus.__contains__("#"):
    corpus.remove("#")


conc = cooccurence(list2, corpus, uniques, zconc)

nconc=np.delete(conc,(0),axis=0)

#normalize the matrix
nconc = normalize(nconc)


#nconc=np.delete(nconc,(0),axis=1)

final=SVD(nconc)
#take transpose
final=final.T
#Take window size from console
window=int(sys.argv[2])

op=final[0:,0:2*window]
#output the results to out.txt
np.savetxt('out.txt',op, fmt='%.5f',delimiter="   ")
