FROM python:3

WORKDIR /usr/src/app

RUN pip install --no-cache-dir -U nltk
RUN pip install --no-cache-dir beautifulsoup4

COPY . .

RUN python ./setup.py
RUN python -c "import nltk;nltk.download('averaged_perceptron_tagger')"

CMD [ "python",  "./main.py" ]
