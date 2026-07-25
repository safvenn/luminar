# 3. Word Frequency
sentence="Data science is fun and data science is powerful"
#Task: Count word frequencies
word=sentence.split()
freq={}

for i in word:
    if i not in freq:
        freq[i]=1
    else:
        freq[i]+=1

print(freq)