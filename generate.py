import MySQLdb
import MySQLdb.cursors
import nltk
import string
import csv
import threading
import pickle

import config

issues = [
  "depressed",
  "suicide",
  "self_harm",
  "family",
  "stress",
  "relationship",
  "isolated",
  "anxiety",
  "friend",
  "school",
  "abuse",
  "substance",
  "bereavement",
  "bully",
  "medical",
  "sexual_abuse",
  "lgbtq",
  "eating",
  "3rd_party",
  "other"
]


query = ''
with open('query_messages.txt', 'r') as file:
  query = file.read()

def freqForIssue(issue, results):
  db = MySQLdb.connect(
    host=config.db_host,
    user=config.db_user,
    passwd=config.db_pass,
    db=config.db_name,
    cursorclass=MySQLdb.cursors.SSCursor
  )

  cursor = db.cursor()
  sql = query.format(issue)
  cursor.execute(sql)

  text = ''
  for value in cursor:
    value = value[0].translate(string.maketrans("",""), string.punctuation).lower()
    text += ' ' + value
  
  text = text.split()
  freq = nltk.FreqDist(text)

  #bigrams = nltk.bigrams(text)
  #bigram_freq = nltk.FreqDist(bigrams)

  #freq = freq.items() + [(' '.join(i[0]), i[1]) for i in bigram_freq.items()]
  #freq = sorted(freq, reverse=True, key=lambda word_freq: word_freq[1])

  freq = freq.items()[:5000]

  results[issue] = freq


def getPickleFrequencies():
  return pickle.load(open('save.p', 'r'))


def doAnalysis(frequencies):
  threads = []
  for issue in issues:
    t = threading.Thread(target=freqForIssue, args=(issue,frequencies,))
    threads.append(t)

  [t.start() for t in threads]
  [t.join() for t in threads]

#frequencies = {}
#doAnalysis(frequencies)
#pickle.dump(frequencies, open('save.p', 'wb'))
frequencies = getPickleFrequencies()

sets = []
for issue in issues:
  sets.append(set( [freq[0] for freq in frequencies[issue][:100]] ))
intersection = set.intersection(*sets)

stopwords = nltk.corpus.stopwords.words('english') + list(intersection)

for issue in frequencies:
  writer = csv.writer(open('output/' + issue + '.csv', 'wb'), quoting=csv.QUOTE_MINIMAL)
  writer.writerows([frequency for frequency in frequencies[issue] if frequency[0] not in stopwords])


print intersection
