import re
import nltk
from nltk.corpus import stopwords

# download stopwords first time
nltk.download('stopwords')

def clean_text(text):

    # lowercase
    text = text.lower()

    # remove symbols and numbers
    text = re.sub(r'[^a-zA-Z ]', ' ', text)

    # remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    # remove stopwords
    stop_words = set(stopwords.words('english'))
    words = text.split()
    words = [word for word in words if word not in stop_words]

    cleaned_text = " ".join(words)

    return cleaned_text
