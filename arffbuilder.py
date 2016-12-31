import sys
import time

class ArffBuilder:
	"""
	This class constructs an arff file from a collection of processed tweets.
	"""

	def __init__(self, inputFileName, outputFileName, numEntries = None):
		"""
		Constructor for ArffBuilder; takes in the name of an input file, the name of an output file, and, optionally, a number of entries to use in building the file.
		"""
		self.outFile = outputFileName
		openedList = open(inputFileName)
		defaultFile = []
		for row in openedList:
			defaultFile.append(row)
		openedList.close()
		workFile = []
		counter = 0
		tempList = []
		self.finalList = []
		for tweet in defaultFile:
			if not ('< A = ' in tweet and counter != 0):
				tempList.append(tweet)
			else:
				workFile.append(tempList)
				tempList = []
				tempList.append(tweet)
			counter += 1
		if numEntries:
			numSelections = int(numEntries)
			numPos = 0
			numNeu = 0
			for tweet in workFile:
				if tweet[0] == '< A = 0 >\n' and numNeu < numSelections:
					numNeu += 1
					self.finalList.append(tweet)
				if tweet[0] == '< A = 4 >\n' and numPos < numSelections:
					numPos += 1
					self.finalList.append(tweet)
		else:
			self.finalList = workFile
	
	def buildFile(self):
		"""
		Builds the contents that are to be written to the arff file, calling the appropriate data extractors before calling for writing.
		"""
		extractedData = []
		for tweet in self.finalList:
			tweetData = []
			tweetData.append(self.firstPersonPronounExtractor(tweet))
			tweetData.append(self.secondPersonPronounExtractor(tweet))
			tweetData.append(self.thirdPersonPronounExtractor(tweet))
			tweetData.append(self.coordinatingConjunctionExtractor(tweet))
			tweetData.append(self.pastTenseVerbsExtractor(tweet))
			tweetData.append(self.futureTenseVerbsExtractor(tweet))
			tweetData.append(self.commasExtractor(tweet))
			tweetData.append(self.colonsAndSemicolonsExtractor(tweet))
			tweetData.append(self.dashesExtractor(tweet))
			tweetData.append(self.parenthesesExtractor(tweet))
			tweetData.append(self.ellipsesExtractor(tweet))
			tweetData.append(self.commonNounsExtractor(tweet))
			tweetData.append(self.properNounsExtractor(tweet))
			tweetData.append(self.adverbsExtractor(tweet))
			tweetData.append(self.whWordsExtractor(tweet))
			tweetData.append(self.modernSlangAcronymsExtractor(tweet))
			tweetData.append(self.wordsAllInUpperCaseExtractor(tweet))
			tweetData.append(self.averageSentenceLengthExtractor(tweet))
			tweetData.append(self.averageTokenLengthExtractor(tweet))
			tweetData.append(self.numberOfSentencesExtractor(tweet))
			tweetData.append(self.profanitiesAndHostilitiesExtractor(tweet))
			tweetData.append(tweet[0][6])
			extractedData.append(tweetData)
		self.writeFile(extractedData)
	
	def firstPersonPronounExtractor(self, tweet):
		"""
		Finds the number of first person pronouns in the tweet, returns the sum.
		"""
		workingTweet = []
		for line in tweet[1:]:
			workingTweet = workingTweet + line.split()
		counter = 0
		for token in workingTweet:
			thisToken = token[:token.index('/')]
			if thisToken in ['I', 'Me', 'me', 'My', 'my', 'Mine', 'mine', 'We', 'we', 'Us', 'us', 'Our', 'our', 'Ours', 'ours']:
				counter += 1
		return counter
		
	def secondPersonPronounExtractor(self, tweet):
		"""
		Finds the number of second person pronouns in the tweet, returns the sum.
		"""
		workingTweet = []
		for line in tweet[1:]:
			workingTweet = workingTweet + line.split()
		counter = 0
		for token in workingTweet:
			thisToken = token[:token.index('/')]
			if thisToken in ['You', 'you', 'Your', 'your', 'Yours', 'yours', 'U', 'u', 'Ur', 'ur', 'Urs', 'urs']:
				counter += 1
		return counter
		
	def thirdPersonPronounExtractor(self, tweet):
		"""
		Finds the number of third person pronouns in the tweet, returns the sum.
		"""
		workingTweet = []
		for line in tweet[1:]:
			workingTweet = workingTweet + line.split()
		counter = 0
		for token in workingTweet:
			thisToken = token[:token.index('/')]
			if thisToken in ['He', 'he', 'Him', 'him', 'His', 'his', 'She', 'she', 'Her', 'her', 'Hers', 'hers', 'It', 'it', 'Its', 'its', 'They', 'they', 'Them', 'them', 'Their', 'their', 'Theirs', 'theirs']:
				counter += 1
		return counter

	def coordinatingConjunctionExtractor(self, tweet):
		"""
		Finds the number of coordinating conjunctions in the tweet, returns the sum.
		"""
		workingTweet = []
		for line in tweet[1:]:
			workingTweet = workingTweet + line.split()
		counter = 0
		for token in workingTweet:
			thisToken = token[token.index('/') + 1:]
			if thisToken == 'CC':
				counter += 1
		return counter

	def pastTenseVerbsExtractor(self, tweet):
		"""
		Finds the number of past tense verbs in the tweet, returns the sum.
		"""
		workingTweet = []
		for line in tweet[1:]:
			workingTweet = workingTweet + line.split()
		counter = 0
		for token in workingTweet:
			thisToken = token[token.index('/') + 1:]
			if thisToken == 'VBD':
				counter += 1
		return counter
		
	def futureTenseVerbsExtractor(self, tweet):
		"""
		Finds the number of future tense verbs in the tweet, returns the sum.
		"""
		workingTweet = []
		for line in tweet[1:]:
			workingTweet = workingTweet + line.split()
		counter = 0
		for token in workingTweet:
			thisToken = token[:token.index('/')]
			if '\'ll' in thisToken or 'gonna' in thisToken or 'going to' in thisToken:
				counter += 1
		return counter
		
	def commasExtractor(self, tweet):
		"""
		Finds the number of commas in the tweet, returns the sum.
		"""
		workingTweet = []
		for line in tweet[1:]:
			workingTweet = workingTweet + line.split()
		counter = 0
		for token in workingTweet:
			thisToken = token[:token.index('/')]
			if thisToken == ',':
				counter += 1
		return counter
		
	def colonsAndSemicolonsExtractor(self, tweet):
		"""
		Finds the number of colons and semi-colons in the tweet, returns the sum.
		"""
		workingTweet = []
		for line in tweet[1:]:
			workingTweet = workingTweet + line.split()
		counter = 0
		for token in workingTweet:
			thisToken = token[:token.index('/')]
			if thisToken == ':' or thisToken == ';':
				counter += 1
		return counter

	def dashesExtractor(self, tweet):
		"""
		Finds the number of dashes in the tweet, returns the sum.
		"""
		workingTweet = []
		for line in tweet[1:]:
			workingTweet = workingTweet + line.split()
		counter = 0
		for token in workingTweet:
			thisToken = token[:token.index('/')]
			if '-' in thisToken:
				counter += 1
		return counter

	def parenthesesExtractor(self, tweet):
		"""
		Finds the number of parentheses in the tweet, returns the sum.
		"""
		workingTweet = []
		for line in tweet[1:]:
			workingTweet = workingTweet + line.split()
		counter = 0
		for token in workingTweet:
			thisToken = token[:token.index('/')]
			if '(' in thisToken or ')' in thisToken:
				counter += 1
		return counter

	def ellipsesExtractor(self, tweet):
		"""
		Finds the number of ellipses in the tweet, returns the sum.
		"""
		workingTweet = []
		for line in tweet[1:]:
			workingTweet = workingTweet + line.split()
		counter = 0
		for token in workingTweet:
			thisToken = token[:token.index('/')]
			if '...' in thisToken:
				counter += 1
		return counter

	def commonNounsExtractor(self, tweet):
		"""
		Finds the number of common nouns in the tweet, returns the sum.
		"""
		workingTweet = []
		for line in tweet[1:]:
			workingTweet = workingTweet + line.split()
		counter = 0
		for token in workingTweet:
			thisToken = token[token.index('/') + 1:]
			if thisToken == 'NN' or thisToken == 'NNS':
				counter += 1
		return counter

	def properNounsExtractor(self, tweet):
		"""
		Finds the number of proper nouns in the tweet, returns the sum.
		"""
		workingTweet = []
		for line in tweet[1:]:
			workingTweet = workingTweet + line.split()
		counter = 0
		for token in workingTweet:
			thisToken = token[token.index('/') + 1:]
			if thisToken == 'NNP' or thisToken == 'NNPS':
				counter += 1
		return counter

	def adverbsExtractor(self, tweet):
		"""
		Finds the number of adverbs in the tweet, returns the sum.
		"""
		workingTweet = []
		for line in tweet[1:]:
			workingTweet = workingTweet + line.split()
		counter = 0
		for token in workingTweet:
			thisToken = token[token.index('/') + 1:]
			if thisToken == 'RB' or thisToken == 'RBR' or thisToken == 'RBS':
				counter += 1
		return counter

	def whWordsExtractor(self, tweet):
		"""
		Finds the number of wh-words in the tweet, returns the sum.
		"""
		workingTweet = []
		for line in tweet[1:]:
			workingTweet = workingTweet + line.split()
		counter = 0
		for token in workingTweet:
			thisToken = token[token.index('/') + 1:]
			if thisToken == 'WDT' or thisToken == 'WP' or thisToken == 'WP$' or thisToken == 'WRB':
				counter += 1
		return counter

	def modernSlangAcronymsExtractor(self, tweet):
		"""
		Finds the number of modern slang acronyms in the tweet, returns the sum.
		"""
		workingTweet = []
		for line in tweet[1:]:
			workingTweet = workingTweet + line.split()
		counter = 0
		for token in workingTweet:
			thisToken = token[:token.index('/')]
			if thisToken in ['smh', 'fwb', 'lmfao', 'lms', 'tbh', 'lmao', 'rofl', 'wtf', 'bff', 'wyd', 'lylc', 'brb', 'atm', 'imao', 'sml', 'btw', 'bw', 'imho', 'fyi', 'ppl', 'sob', 'ttyl', 'imo', 'ltr', 'thx', 'kk', 'omg', 'ttys', 'afn', 'bbs', 'cya', 'ez', 'f2f', 'gtr', 'ic', 'jk', 'k', 'ly', 'ya', 'nm', 'np', 'plz', 'ru', 'so', 'tc', 'tmi', 'ym', 'ur', 'u', 'sol']:
				counter += 1
		return counter

	def wordsAllInUpperCaseExtractor(self, tweet):
		"""
		Finds the number of words all in upper case in the tweet, returns the sum.
		"""
		workingTweet = []
		for line in tweet[1:]:
			workingTweet = workingTweet + line.split()
		counter = 0
		for i in workingTweet:
			thisToken = i[:i.index('/')]
			if len(thisToken) > 2:
				isAllUpperCase = True
				for character in thisToken:
					if ord(character) > 96 and ord(character) < 123:
						isAllUpperCase = False
				if isAllUpperCase:
					counter += 1
		return counter

	def averageSentenceLengthExtractor(self, tweet):
		"""
		Finds the length of the average sentence in the tweet, returns the average.
		"""
		sums = []
		counter = 0
		for sentence in tweet:
			if counter != 0:
				sums.append(len(sentence))
			counter += 1
		ave = 0.0
		for i in sums:
			ave += i
		ave = ave / len(sums)
		return ave

	def averageTokenLengthExtractor(self, tweet):
		"""
		Finds the length of the average token in the tweet, returns the average.
		"""
		workingTweet = []
		ave = 0.0
		for line in tweet[1:]:
			workingTweet = workingTweet + line.split()
		counter = 0
		for token in workingTweet:
			thisToken = token[:token.index('/')]
			ave += len(thisToken)
		ave = ave / (len(workingTweet))
		return ave

	def numberOfSentencesExtractor(self, tweet):
		"""
		Returns the number of sentences in the tweet.
		"""
		return len(tweet) - 1

	def profanitiesAndHostilitiesExtractor(self, tweet):
		"""
		Finds and returns the number of profanities and hostile/negatively-charged words.
		"""
		workingTweet = []
		for line in tweet[1:]:
			workingTweet = workingTweet + line.split()
		counter = 0
		for token in workingTweet:
			thisToken = token[:token.index('/')]
			if thisToken in ['piss', 'Piss', 'shit', 'Shit', 'fuck', 'Fuck', 'ass', 'Ass', 'asshole', 'Asshole', 'cunt', 'Cunt', 'whore', 'Whore', 'fucker', 'Fucker', 'shithead', 'Shithead', 'pissed', 'Pissed', 'fucking', 'Fucking', 'hate', 'Hate', 'awful', 'Awful']:
				counter += 1
		return counter
	
	def writeFile(self, compilation):
		"""
		Creates a new arff file and writes the data to it.
		"""
		file = open(self.outFile, 'a')
		file.write('@relation tweets\n')
		file.write('\n')
		file.write('@attribute firstPersonPronouns numeric\n')
		file.write('@attribute secondPersonPronouns numeric\n')
		file.write('@attribute thirdPersonPronouns numeric\n')
		file.write('@attribute coordinatingConjunctions numeric\n')
		file.write('@attribute pastTenseVerbs numeric\n')
		file.write('@attribute futureTenseVerbs numeric\n')
		file.write('@attribute commas numeric\n')
		file.write('@attribute colonsAndSemicolons numeric\n')
		file.write('@attribute dashes numeric\n')
		file.write('@attribute parentheses numeric\n')
		file.write('@attribute ellipses numeric\n')
		file.write('@attribute commonNouns numeric\n')
		file.write('@attribute properNouns numeric\n')
		file.write('@attribute adverbs numeric\n')
		file.write('@attribute whWords numeric\n')
		file.write('@attribute modernSlangAcronyms numeric\n')
		file.write('@attribute wordsAllInUpperCase numeric\n')
		file.write('@attribute averageSentenceLength numeric\n')
		file.write('@attribute averageTokenLength numeric\n')
		file.write('@attribute numberOfSentences numeric\n')
		file.write('@attribute profanitiesAndHostilities numeric\n)
		file.write('@attribute class {0,2,4}\n')
		file.write('\n')
		file.write('@data\n')
		for tweet in compilation:
			outLine = ''
			counter = 0
			for entry in tweet:
				outLine = outLine + str(entry)
				if counter != (len(tweet) - 1):
					outLine = outLine + ','
				counter += 1
			outLine = outLine + '\n'
			file.write(outLine)
		file.close()



if __name__ == '__main__':
	if len(sys.argv) < 3 or len(sys.argv) > 4:
		print "Wrong number of arguments!"
	else:
		if len(sys.argv) == 4:
			builder = ArffBuilder(sys.argv[1], sys.argv[2], sys.argv[3])
		else:
			builder = ArffBuilder(sys.argv[1], sys.argv[2])
		builder.buildFile()
