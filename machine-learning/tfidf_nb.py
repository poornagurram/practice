from sklearn import preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import PorterStemmer
from sklearn.naive_bayes import GaussianNB

ps = PorterStemmer()

docs = {"politics": ["republican Fed", "administrations nation", "Fed administrations address nation"],
        "history": ["archives anarchy migration", "anarchy poll"]
        }
test_input = "administrations republican"
corpus = []
labels = []
for i, j in docs.items():
        corpus.extend(j)
        for label in j:
                labels.append(i)

def tokenize(text):
    tokens = [ps.stem(t) for t in text.split(" ")]
    return tokens

le = preprocessing.LabelEncoder()
labels = le.fit_transform(labels)

vectorizer = TfidfVectorizer(tokenizer=tokenize)
X = vectorizer.fit_transform(corpus)
X_test = vectorizer.transform([test_input])
model = GaussianNB()
model.fit(X.toarray(), labels)
print(f"the document '{test_input}' belongs to {le.inverse_transform(model.predict(X_test.toarray()))[0]}")
