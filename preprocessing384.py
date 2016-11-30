import NLPlib
import re
import sys

class Preprocessing384:
	"""
	Takes a csv file containing tweets and their parameters, removes extraneous information, tags elements of the tweets with grammatical information, and then writes it all to a text file.
	"""

	def __init__(self, tweetArchive, outputFile):
		"""
		Constructor; takes the csv and the name of the text file to be written to.
		"""
		self.textDump = outputFile
		openArchive = open(tweetArchive)
		csvDump = []
		for row in openArchive:
			csvDump.append(row)
		openArchive.close()
		self.tweets = []
		self.tagger = NLPlib.NLPlib()
		for i in csvDump:
			sentiment = i[1]
			breakdown = i
			for j in range(5):
				breakdown = breakdown[breakdown.index(',') + 1:]
			breakdown = breakdown[1:-1]
			self.tweets.append([sentiment, breakdown])
	
	def processTweets(self):
		"""
		Calls functions to process the tweets and then write the processed tweets to a text file.
		"""
		counter = 0
		for i in self.tweets:
			tweet = i
			tweet[1] = self.clearHtml(tweet[1])
			tweet[1] = self.fixCodes(tweet[1])
			tweet[1] = self.clearUrls(tweet[1])
			tweet[1] = self.clearTags(tweet[1])
			tweet[1] = self.breakSentence(tweet[1])
			tweet[1] = self.spaceTokens(tweet[1])
			tweet[1] = self.tagTokens(tweet[1])
			self.tweets[counter] = tweet
			counter += 1
		self.writeLines(self.tweets, self.textDump)
	
	def clearHtml(self, twut): #recheck this
		"""
		Strips out HTML tags and attributes.
		"""
		twut = twut.translate(None, '<[^>]+>')
		return twut
	
	def fixCodes(self, twut):
		"""
		Replaces HTML characters with ASCII equivalents.
		"""
		finalText = ''
		badChar = True
		for i in twut:
			if ord(i) < 128:
				finalText += i
		finalText = finalText.replace('&quot', '\"')
		finalText = finalText.replace('&amp', '&')
		finalText = finalText.replace('&lt', '<')
		finalText = finalText.replace('&gt', '>')
		finalText = finalText.replace('&circ', '^')
		finalText = finalText.replace('&tilde', '~')
		return finalText
	
	def clearUrls(self, twut):
		"""
		Removes URLs.
		"""
		newTwut = twut
		urlHunter = re.compile('(https?:\/\/)([0-9a-z]+)\.([a-z\.]+)\/?')
		while urlHunter.search(newTwut):
			newTwut = urlHunter.sub('', newTwut)
		return newTwut
	
	def clearTags(self, twut):
		"""
		Removes the @'s from usernames, and the #'s from hashtags.
		"""
		userName = re.compile('@([0-9a-zA-Z]+)')
		hashTag = re.compile('#([0-9a-zA-Z]+)')
		newTwut = twut
		while userName.search(newTwut):
			position = userName.search(newTwut)
			newTwut = newTwut[:position.start()] + userName.search(newTwut).group(0)[1:] + newTwut[position.end():]
		while hashTag.search(newTwut):
			position = hashTag.search(newTwut)
			newTwut = newTwut[:position.start()] + hashTag.search(newTwut).group(0)[1:] + newTwut[position.end():]
		return newTwut
	
	def breakSentence(self, twut):
		"""
		Breaks tweets down into individual sentences.
		"""
		sentenceDetection = re.compile('(\S+)((\.+)|([!?]))(\s+)(\S+)')
		newTwut = twut
		finalTwut = [] 
		while sentenceDetection.search(newTwut):
			subSentence = sentenceDetection.search(newTwut)
			subStart = subSentence.start()
			subEnd = subSentence.end()
			moddedSub = subSentence.group(0)
			moddedSuba = moddedSub.split()
			firstHalf = newTwut[:subStart]
			secondHalf = newTwut[subEnd:]
			newTwut = moddedSuba[1] + secondHalf
			finalTwut.append(firstHalf + moddedSuba[0])
		finalTwut.append(newTwut)
		return finalTwut
	
	def spaceTokens(self, twut):
		"""
		Separates clitics, possessives, and punctuation from words.
		"""
		cliticBreaker = re.compile('(\S+)(\'s)')
		otherCliticBreaker = re.compile('(\S+n)(\'t)')
		possessiveBreaker = re.compile('(\S+s)(\')(\s+)')
		punctuationBreaker = re.compile('(\S+)([\.!\?\"\:\;\,]+)(\s*)')
		newTwut = twut
		finalTwut = []
		counter = 0
		for i in newTwut:
			workInput = newTwut[counter].split()
			workOutput = []
			for j in workInput:
				if cliticBreaker.search(j):
					subClitic = cliticBreaker.search(j)
					moddedSub = subClitic.group(0)
					moddedSuba = moddedSub.replace('\'', ' \'')
					subIndex = moddedSuba.index(' ')
					firstHalf = j[:subIndex]
					secondHalf = j[subIndex:]
					workOutput.append(firstHalf)
					workOutput.append(secondHalf)
				elif otherCliticBreaker.search(j):
					subClitic = otherCliticBreaker.search(j)
					moddedSub = subClitic.group(0)
					moddedSuba = moddedSub.replace('\'', ' \'')
					subIndex = moddedSuba.index(' ')
					firstHalf = j[:subIndex]
					secondHalf = j[subIndex:]
					workOutput.append(firstHalf)
					workOutput.append(secondHalf)
				elif possessiveBreaker.search(j):
					subPoss = possessiveBreaker.search(j)
					moddedSub = subPoss.group(0)
					moddedSuba = moddedSub.replace('\'', ' \'')
					subIndex = moddedSuba.index(' ')
					firstHalf = j[:subIndex]
					secondHalf = j[subIndex:]
					workOutput.append(firstHalf)
					workOutput.append(secondHalf)
				elif punctuationBreaker.search(j):
					subPunc = punctuationBreaker.search(j)
					moddedSub = subPunc.group(0)
					internalCounter = len(moddedSub)
					while not moddedSub[internalCounter-1].isalpha() and not moddedSub[internalCounter-1].isdigit() and internalCounter >= 0:
						internalCounter -= 1
					firstHalf = j[:internalCounter]
					secondHalf = j[internalCounter:]
					workOutput.append(firstHalf)
					workOutput.append(secondHalf)
				else:
					workOutput.append(j)
			finalTwut.append(workOutput)
			counter += 1
		return finalTwut
	
	def tagTokens(self, twut):
		"""
		Tags tokens with syntactic and other linguistic data.
		"""
		finalTwut = twut
		counter = 0
		for sentence in finalTwut:
			tags = self.tagger.tag(sentence)
			finalSentence = []
			wordCounter = 0
			for word in sentence:
				finalSentence.append(word + '/' + tags[wordCounter])
				wordCounter += 1
			finalTwut[counter] = finalSentence
			counter += 1
		return finalTwut
	
	def writeLines(self, tweetCollection, outputDump):
		"""
		Writes the processed tweets to a text file.
		"""
		file = open(outputDump, 'a')
		for i in tweetCollection:
			file.write('< A = ' + i[0] + " >")
			file.write('\n')
			for j in i[1]:
				done = ''
				for k in j:
					done = done + ' ' + k
				file.write(done)
				file.write('\n')
		file.close()		

	

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print "Wrong number of arguments!"
	else:
		processor = Preprocessing384(sys.argv[1], sys.argv[2])
		processor.processTweets()