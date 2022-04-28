
text = open('texts/pride.txt').read()

words = text.split('\n\n')

count = 0

for item in words:
    count += 1
    filename = 'texts/outputLarge/{}.txt'.format(count)
    with open(filename, 'w') as f:
        f.write('{}\n'.format(item))