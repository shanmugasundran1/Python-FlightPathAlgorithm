import winsound


def data(l):
    import string
    import re

    for x in l[1:]:

        file1 = open(x + ".txt")
        line = file1.read()  # Use this to read file content as a stream:
        words = line.split()
        # print(words)
        allow = string.ascii_letters + string.digits
        re.sub('[^%s]]' % allow, '', line)
        table = str.maketrans({key: None for key in string.punctuation})
        new_s = line.translate(table)

        print("Words with punctuation of " + x + " articles : " + line)
        print('\n')
        print("Words without punctuation " + x + " articles : " + new_s)
        print('\n')

        # tokenized_text=sent_tokenize(text)
        # print(tokenized_text)

        new_s = new_s.lower()
        from nltk.tokenize import word_tokenize

        tokenized_word = word_tokenize(new_s)
        # print(tokenized_word)
        print('\n')

        from nltk.corpus import stopwords

        stop_words = set(stopwords.words("english"))
        print(stop_words)
        print('\n')

        filtered_sent = []
        for w in tokenized_word:
            if w not in stop_words:
                filtered_sent.append(w)

        stopwords_sent = []
        for y in tokenized_word:
            if y in stop_words:
                stopwords_sent.append(y)

        print("Tokenized Sentence:", tokenized_word)
        print('\n')
        print("Filterd Sentence:", filtered_sent)
        print('\n')
        print("Stopword Sentence:", stopwords_sent)
        print('\n')
        from nltk.probability import FreqDist

        fdist = FreqDist(filtered_sent)
        fdist1 = FreqDist(stopwords_sent)
        print(fdist)
        print('\n')
        print("Most Common word :", fdist.most_common(2))
        print('\n')
        print("Most Common Stopword :", fdist1.most_common(2))

        import matplotlib.pyplot as plt

        plt.xlabel('Count Words')
        plt.ylabel('Frequency')
        plt.title('The Frequency of Count Words for : ' + x + " articles")
        fdist.plot(30, cumulative=False)

        plt.show()

        import matplotlib.pyplot as plt1

        plt1.xlabel('Stop Words')
        plt1.ylabel('Frequency')
        plt1.title('The Frequency of Stop Words for : ' + x + " articles")
        fdist1.plot(30, cumulative=False)

        plt1.show()

        appendFile = open('filteredtext1.txt', 'w')
        for r in filtered_sent:
            appendFile.write(" " + r)

        appendFile.close()

        file1 = open("filteredtext1.txt")
        theTweet = file1.read()  # Use this to read file content as a stream:

        file2 = open("positive.txt")
        line2 = file2.read()  # Use this to read file content as a stream:
        positive_words = line2.split(", ")

        file3 = open("negative.txt")
        line3 = file3.read()  # Use this to read file content as a stream:
        negative_words = line3.split(", ")

        import re

        theTokens = re.findall(r'\b\w[\w-]*\b', theTweet)
        print("The Tokenized Words", theTokens)
        print("\n")

        numPosWords = 0
        numPos = []
        for word in theTokens:
            if word in positive_words:
                numPosWords += 1
                numPos.append(word)

        print("Total number of Positive Words: ", numPosWords)
        print("The Positive words for article " + x + " :", numPos)

        numNegWords = 0
        numNeg = []
        for words in theTokens:
            if words in negative_words:
                numNegWords += 1
                numNeg.append(words)
        print()
        print("Total number of Negative Words: ", numNegWords)
        print("The Negative Words for article " + x + " :", numNeg)

        numWords = len(theTokens)
        print(numWords)
        percntPos = numPosWords / numWords
        percntNeg = numNegWords / numWords
        print()
        print("Positive: " + "{:.0%}".format(percntPos) + "  Negative: " + "{:.0%}".format(percntNeg))
        print()
        if numPosWords > numNegWords:
            print("Positive " + str(numPosWords) + ":" + str(numNegWords))
            print()
            print("The Article has a Positive Sentimental Analysis!!!!")
        elif numNegWords > numPosWords:
            print("Negative " + str(numPosWords) + ":" + str(numNegWords))
            print()
            print("The Article has a Negative Sentimental Analysis!!!!")
        elif numNegWords == numPosWords:
            print("Neutral " + str(numPosWords) + ":" + str(numNegWords))
            print()
            print("The Article has a Neutral Sentimental Analysis!!!!")

        print()

        appendFile = open('Positive_InText_' + x + '.txt', 'w')
        for j in numPos:
            appendFile.write(j + ", ")

        appendFile.close()

        appendFile = open('Negative_InText_' + x + '.txt', 'w')
        for z in numNeg:
            appendFile.write(z + ", ")

        appendFile.close()

        import seaborn as sns

        sns.set_style("whitegrid")
        import matplotlib.pyplot as plt

        values = [percntPos * 100, percntNeg * 100]
        labels1 = ["Positive", "Negative"]
        cols = ['c', 'r']
        plt.pie(values, labels=labels1, colors=cols, autopct='%1.1f%%')

        plt.title('The Percentage of Positive and Negative Sentiment of The ' + x + " Article")
        plt.legend()
        plt.show()
        x = [1, 2]
        y = [numPosWords, numNegWords]
        labels = ["Positive", "Negative"]

        plt.bar(x, y, align='center')
        plt.xticks(x, labels)
        plt.title('The Total of Positive and Negative Sentiment of Article')
        plt.ylabel("Total Words")
        plt.show()

        winsound.PlaySound("Sound", winsound.SND_FILENAME)


def AnalysisArticle(positive, negative, neutral, fullword, dic):
    freq = getFreq(positive, negative, neutral, fullword, dic)
    percent = getPercent(freq["Positive"], freq["Negative"], freq["Neutral"], freq["Full"])
    results = {"freq": freq, "percent": percent}
    return results


def AnalysisFreq(percent):
    print("Article is", max(percent, key=lambda i: percent[i]))


def getPercent(pos, neg, neut, full):
    ratio = 100 / full
    percent = {
        "Positive": pos * ratio,
        "Negative": neg * ratio,
        "Neutral": neut * ratio

    }
    return percent


def getFreq(pos, neg, neut, full, dic):
    pos = 0
    neg = 0
    neut = 0
    full = 0

    for i in pos:
        pos += dic[i]
    for i in neg:
        neg += dic[i]
    for i in neut:
        neut += dic[i]
    for i in dic.keys():
        full += dic[i]
    freq = {
        "Positive": pos, "Negative": neg, "Neutral": neut, "Full": full
    }
    return freq


def get_dic(keys, ori_dic):
    new_dic = {}
    for i in keys:
        new_dic[i] = ori_dic[i]
    return new_dic


def printAnalysis(results):
    table_header = ["Type", "Total Words", "Percentage (%)"]
    table_body = [
        ["Positive", results["freq"]["Positive"], "%.f" % results["percent"]["Positive"]],
        ["Negative", results["freq"]["Negative"], "%.f" % results["percent"]["Negative"]],
        ["Neutral", results["freq"]["Neutral"], "%.f" % results["percent"]["Neutral"]]
    ]

    print(tabulate(table_body, table_header), "\n\nTotal Words: ", results["freq"]["Full"])
    AnalysisFreq(results["percent"])

    if pos > neg:
        print("The country has positive sentiment. ")

    elif neg > pos:
        print("The country has negative sentiment. ")

    elif neg == pos:
        print("The country has natural sentiment.")

    # winsound.PlaySound("Sound", winsound.SND_FILENAME)

    from gtts import gTTS
    text = "Thank You"
    speech = gTTS(text, 'en')
    speech.save("Bye.mp3")


import os

os.startfile('Bye.mp3')
