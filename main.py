import nltk, re, pprint
from nltk.corpus import PlaintextCorpusReader
from nltk import word_tokenize
from urllib import request

from bs4 import BeautifulSoup # http://www.crummy.com/software/BeautifulSoup/:
import argparse

def process_text_url(url):
    url = "http://www.gutenberg.org/files/2554/2554.txt"
    response = request.urlopen(url)
    raw = response.read().decode('utf8')
    type(raw)
    len(raw)
    tokens = word_tokenize(raw)
    print(tokens)
def process_html_url(url):
    url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
    html = request.urlopen(url).read().decode('utf8')
    raw = BeautifulSoup(html,"html.parser").get_text()
    # print(raw)
    tokens = word_tokenize(raw)
    print("html tokens:")
    print(tokens)

def lexical_diversity(text):
    return len(set(text)) / len(text)

def percentage(count, total):
    return 100*count/total

def stem(word):
    regexp = r'^(.*?)(ing|ly|ed|ious|ies|ive|es|s|ment)?$'
    stem, suffix = re.findall(regexp, word)[0]
    return stem

def unusual_words(text):
    text_vocab = set(w.lower() for w in text if w.isalpha())
    english_vocab = set(w.lower() for w in nltk.corpus.words.words())
    unusual = text_vocab - english_vocab
    return sorted(unusual)
def content_fraction(text):
    ### fraction of words that are not in the stopwords list.
    stopwords = nltk.corpus.stopwords.words('english')
    content = [w for w in text if w.lower() not in stopwords]
    return len(content) / len(text)
def findtags(tag_prefix, tagged_text):
    cfd = nltk.ConditionalFreqDist((tag, word) for (word, tag) in tagged_text
                                  if tag.startswith(tag_prefix))
    return dict((tag, cfd[tag].most_common(5)) for tag in cfd.conditions())
def summary(title, raw, sents):
    print("Summary: ", title)
    tokens = word_tokenize(raw) # raw data
    words = [w.lower() for w in tokens]
    vocab = sorted(set(words))

    porter = nltk.PorterStemmer()
    stems = sorted(set([porter.stem(t) for t in tokens]))

    wnl = nltk.WordNetLemmatizer()
    lemmas = sorted(set([wnl.lemmatize(t) for t in tokens]))
    num_chars = len(raw)
    num_words = len(words)
    num_sents = len(sents)
    num_vocab = len(vocab)
    data = {}
    data["num_chars"] = num_chars
    data["num_words"] = num_words
    data["num_sents"] = num_sents
    data["num_vocab"] = num_vocab
    data["average_word_length"] = num_chars/num_words
    data["average_sentence_length"] = num_words/num_sents
    data["words_per_vocab"] = num_words/num_vocab
    ld = lexical_diversity(words)

    data["lexical_diversity"] = ld

    fdist = nltk.FreqDist(words)
    data["frequency_distribution_words_total"]= fdist.N()
    data["frequency_distribution_words_max"]= fdist.max()
    data["frequency_distribution_words_max_times"]= fdist[fdist.max()]

    data["frequency_distribution_words_most_common"]= fdist.most_common()
    data["frequency_distribution_words_hapaxes"]= fdist.hapaxes()


    modals = ['can','could','may','might','must','will']
    fmodal = {}
    for m in modals:
        fmodal[m]=fdist[m]
    data["frequency_distribution_words_modal_verbs"]= fmodal


    fdistlen=nltk.FreqDist(len(w) for w in words)
    data["frequency_distribution_words_legnth_total"]= fdistlen.N()
    data["frequency_distribution_words_legnth_max"]= fdistlen.max()
    data["frequency_distribution_words_legnth_most_common"]= fdistlen.most_common()
    print("Frequency distribution of lengths of words ")

    data["unusual_words"] = unusual_words(words)
    data["content_fraction_stop_words"] = content_fraction(words)

    tags = nltk.pos_tag(vocab)

    fdist = nltk.FreqDist(tag for (word,tag) in tags)
    print("Frequency distribution of tags ")
    data["frequency_distribution_tags_total"]= fdist.N()
    data["frequency_distribution_tags_max"]= fdist.max()
    data["frequency_distribution_tags_max_times"]= fdist[fdist.max()]

    data["frequency_distribution_tags_most_common"]= fdist.most_common()
    data["frequency_distribution_tags_hapaxes"]= fdist.hapaxes()


    data["part_of_speach_tags"] = tags

    taginfo = {}
    word_tags = nltk.pos_tag(words)

    tagdict = findtags('NN', word_tags)
    for tag in sorted(tagdict):
        taginfo[tag] = tagdict[tag]

    tagdict = findtags('IN', word_tags)
    for tag in sorted(tagdict):
        taginfo[tag] = tagdict[tag]

    tagdict = findtags('AT', word_tags)
    for tag in sorted(tagdict):
        taginfo[tag] = tagdict[tag]

    tagdict = findtags('VB', word_tags)
    for tag in sorted(tagdict):
        taginfo[tag] = tagdict[tag]

    data["part_of_speach_tags_dict"] = taginfo

    fdist = nltk.FreqDist(ch.lower() for ch in raw if ch.isalpha())
    data["frequency_distribution_letters_most_common"]= fdist.most_common()


    return data
def analyze(title,raw,sents):
    print("Analyzing: ", title)
    print("raw: ")
    print(raw)

    tokens = word_tokenize(raw) # raw data
    print("token: ")
    print(tokens)
    words = [w.lower() for w in tokens]
    print("words: ")
    print(words)
    vocab = sorted(set(words))
    print("vocab: ")
    print(vocab)
    print("sentences: ")
    print(sents)
    print("--------")
    # stems = sorted(set([stem(t) for t in vocab]))
    porter = nltk.PorterStemmer()
    stems = sorted(set([porter.stem(t) for t in tokens]))
    print("stems: ")
    print(stems)
    wnl = nltk.WordNetLemmatizer()
    lemmas = sorted(set([wnl.lemmatize(t) for t in tokens]))
    print("lemmas: ")
    print(lemmas)
    print("--------")
    num_chars = len(raw)
    num_words = len(words)
    num_sents = len(sents)
    num_vocab = len(vocab)

    print(" characters: ", num_chars, " words: ", num_words, " sentences: ", num_sents)
    print("vocabulary used count: ", num_vocab )
    print("average word length: ", (num_chars/num_words))
    print("average sentence length: ", (num_words/ num_sents))
    print("words per vocab ", (num_words/num_vocab))
    print("vocab per word ", (num_vocab/num_words))
    ld = lexical_diversity(words)
    print("Lexical Diversity ", ld)
    fdist = nltk.FreqDist(words)
    print(fdist)
    print("Frequency Distribution, total: ", fdist.N(), ". max occurance : ", fdist.max(), ". occured: ", fdist[fdist.max()], " times.")

    print("Freqency Distribution, most common ", fdist.most_common())
    print("Frequency Distribution, used once (hapaxes): ", fdist.hapaxes())
    print("Frequency Distribution, tabulated: ")
    fdist.tabulate()
    fdistlen=nltk.FreqDist(len(w) for w in words)
    print("Frequency distribution of lengths of words ")
    print("Total: ", fdistlen.N(),  ", max: ", fdistlen.max())
    print("Most Common: ", fdistlen.most_common())
    #for sample in fdist:
    #    print(sample)
    modals = ['can','could','may','might','must','will']
    print("Freqency Distribution, for modal verbs: ", modals)
    for m in modals:
        print(m + ': ',fdist[m], end = ' ')
    print("")

    print("-----")
    print("Unusual or mispelled words")
    print(unusual_words(words))
    print("-----")
    print("Stop words")
    print(nltk.corpus.stopwords.words('english'))
    print("content fraction relative to stop words")
    print(content_fraction(words))
    print("tagged vocab")
    tags = nltk.pos_tag(vocab)
    print(tags)
    fdist = nltk.FreqDist(tag for (word,tag) in tags)
    print("Frequency distribution of tags ")
    print(fdist.most_common())
    tagdict = findtags('NN', tags)
    for tag in sorted(tagdict):
        print(tag, tagdict[tag])
    fdist = nltk.FreqDist(ch.lower() for ch in raw if ch.isalpha())
    print("most common letters used: ")
    print(fdist.most_common())

corpus_root = './data'
wordlists = PlaintextCorpusReader(corpus_root, '.*')
parser = argparse.ArgumentParser()
parser.add_argument("-d",help="display details instead of summary.")
args=parser.parse_args()

for fileid in wordlists.fileids():
    raw = wordlists.raw(fileid)
    sents = wordlists.sents(fileid)
    if args.d:
        analyze(fileid, raw, sents)
    else:
        data = summary(fileid, raw, sents)
        pprint.pprint(data)
    print("---------")
