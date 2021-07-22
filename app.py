from flask import Flask, request, jsonify
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from pandas import read_csv, DataFrame
import csv
import io
import copy

app = Flask(__name__)

with app.app_context():
    nltk.download('popular')


def sentiment_analyzer(data):
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(data)


@app.route('/')
def hello_world():
    return "01Synergy"


@app.route('/api/upload_csv_file', methods=['POST'])
def upload_csv_file():
    uploaded_file = request.files['file']
    if not uploaded_file:
        return "No file"
    stream = io.StringIO(uploaded_file.stream.read().decode("UTF8"), newline=None)
    stream1 = copy.copy(stream)
    read_file = read_csv(stream)

    df = DataFrame(read_file, columns=['presentation_skills', 'content_rating', 'overall_rating'])
    presenting_skills = round(list(df.mean(axis=0))[0])
    content_rating = round(list(df.mean(axis=0))[1])

    poor_counter = 0
    fair_counter = 0
    good_counter = 0
    very_good_counter = 0
    excellent_counter = 0

    negative_sentiment_counter = 0
    neutral_sentiment_counter = 0
    positive_sentiment_counter = 0
    total_rows = 0

    csv_input = csv.DictReader(stream1)
    for row in csv_input:
        total_rows += 1
        input_data = row['comment_for_presenting']
        input_data1 = row['brief_learnt_detail']
        input_data2 = row['suggestion_for_presenting']
        sentiment_dict = sentiment_analyzer(f'{input_data}, {input_data1}, {input_data2}')

        # Decide sentiment as positive, negative and neutral
        if sentiment_dict['compound'] >= 0.05:
            positive_sentiment_counter += 1
        elif sentiment_dict['compound'] <= - 0.05:
            negative_sentiment_counter += 1
        else:
            neutral_sentiment_counter += 1

        # Increase rating counters
        if row['overall_rating'] == '5':
            excellent_counter += 1
        elif row['overall_rating'] == '4':
            very_good_counter += 1
        elif row['overall_rating'] == '3':
            good_counter += 1
        elif row['overall_rating'] == '2':
            fair_counter += 1
        elif row['overall_rating'] == '1':
            poor_counter += 1

    result = [{
        'total_reviews': total_rows,
        'avg_presenting_skills_score': presenting_skills,
        'avg_content_rating_score': content_rating,
        'rating_score': {
            'excellent': excellent_counter,
            'very_good': very_good_counter,
            'good': good_counter,
            'fair': fair_counter,
            'poor': poor_counter
        },
        'overall_sentiment_score': {
            'positive': positive_sentiment_counter,
            'neutral': neutral_sentiment_counter,
            'negative': negative_sentiment_counter
        }
    }]
    return jsonify(result)


if __name__ == '__main__':
    app.run()
