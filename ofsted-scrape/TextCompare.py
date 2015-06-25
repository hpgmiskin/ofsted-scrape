import nltk.corpus
import nltk.tokenize
import nltk.stem.snowball
import string

class TextCompare(object):
    """TextCompare can be used to compare sentences on a tokenised word
    basis"""

    def __init__(self):
        """Configures the components used for the string comparison
        """
        
        # Create a stopword list
        self.stopwords = nltk.corpus.stopwords.words('english')
        self.stopwords.extend(string.punctuation)
        self.stopwords.append('')

        # Create a tokenizer
        self.tokenizer = nltk.tokenize.TreebankWordTokenizer()

        # Create a stemmer
        self.stemmer = nltk.stem.snowball.PorterStemmer()

    def stripWords(self,words):
        """Strips the punctuation from each word in the list and also
        removes the words that appear in the stopwords list
        """

        newWords = []

        for word in words:

            # word = unicode(word,"utf-8")
            word = word.lower()
            word = word.strip(string.punctuation)
            # word = word.encode("utf-8","ignore")

            if word not in self.stopwords:
                word = self.stemmer.stem(word)
                newWords.append(word)

        return newWords

    def tokenizeSentence(self,sentence):
        """Tokenises the words in the given sentence and returns a set
        of the tokenised sentence with stopwords and punctuation removed
        """

        words = [token for token in self.tokenizer.tokenize(sentence)]
        words = self.stripWords(words)

        return set(words)

    def setSearch(self,search):
        self.search = self.tokenizeSentence(str(search))

    def setMatch(self,match):
        self.match = self.tokenizeSentence(str(match))

    def compare(self,sentence1,sentence2):
        """Compares the tokenised versions of the given sentences and
        returns the Jaccard ratio of the comparison
        """

        self.search = self.tokenizeSentence(str(sentence1))
        self.match = self.tokenizeSentence(str(sentence2))

        return ratio()

    def ratio(self):

        intersectCount = len(self.search & self.match)
        unionCount = len(self.search | self.match)
        ratio = intersectCount / float(unionCount)

        return ratio
