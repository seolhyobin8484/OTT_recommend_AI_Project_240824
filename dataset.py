# 필요한 라이브러리 설치
# !pip install scikit-learn pandas numpy

import pandas as pd
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# 데이터 로드
# 여기서는 20 Newsgroups 데이터를 사용하지만, 실제로는 IMDB 데이터셋을 사용할 수 있습니다.
categories = ['rec.sport.baseball', 'rec.sport.hockey']
data = fetch_20newsgroups(subset='train', categories=categories, remove=('headers', 'footers', 'quotes'))

# 데이터프레임 생성
df = pd.DataFrame({'text': data.data, 'label': data.target})
df['label'] = df['label'].map({i: label for i, label in enumerate(categories)})

# TF-IDF 벡터화
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(df['text'])
print(X)
y = df['label']
print("--",5)
print(y)
# 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 모델 학습
model = MultinomialNB()
model.fit(X_train, y_train)

# 예측 및 평가
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
print("Classification Report:")
print(classification_report(y_test, y_pred))
