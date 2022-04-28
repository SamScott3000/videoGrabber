import os

count = 0

for x in range(2298):
    count += 1

    file = open("texts/outputLarge3/" + str(count) + ".txt")
    data = file.read()
    words = data.split()
    wordNumber = len(words)
    print(wordNumber)
    if wordNumber < 21:
       os.remove("texts/outputLarge3/" + str(count) + ".txt")
