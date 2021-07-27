from flask import Flask, request, jsonify
from flask_cors import CORS
from nltk.sentiment import SentimentIntensityAnalyzer
from configurations import DevelopmentConfig
import csv
import io

app = Flask(__name__)
CORS(app)
app.config.from_object(DevelopmentConfig)


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

    overall_poor_counter = 0
    overall_fair_counter = 0
    overall_good_counter = 0
    overall_very_good_counter = 0
    overall_excellent_counter = 0

    ps_excellent_counter = 0
    ps_very_good_counter = 0
    ps_good_counter = 0
    ps_fair_counter = 0
    ps_poor_counter = 0

    cr_excellent_counter = 0
    cr_very_good_counter = 0
    cr_good_counter = 0
    cr_fair_counter = 0
    cr_poor_counter = 0

    negative_sentiment_counter = 0
    neutral_sentiment_counter = 0
    positive_sentiment_counter = 0
    total_rows = 0

    csv_input = csv.DictReader(stream)
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

        # Increase overall rating counters
        if row['overall_rating'] == 'Excellent':
            overall_excellent_counter += 1
        elif row['overall_rating'] == 'Very Good':
            overall_very_good_counter += 1
        elif row['overall_rating'] == 'Good':
            overall_good_counter += 1
        elif row['overall_rating'] == 'Fair':
            overall_fair_counter += 1
        elif row['overall_rating'] == 'Poor':
            overall_poor_counter += 1

        # Increase presenting skills rating counters
        if row['presentation_skills'] == 'Excellent':
            ps_excellent_counter += 1
        elif row['presentation_skills'] == 'Very Good':
            ps_very_good_counter += 1
        elif row['presentation_skills'] == 'Good':
            ps_good_counter += 1
        elif row['presentation_skills'] == 'Fair':
            ps_fair_counter += 1
        elif row['presentation_skills'] == 'Poor':
            ps_poor_counter += 1

        # Increase content rating counters
        if row['content_rating'] == 'Excellent':
            cr_excellent_counter += 1
        elif row['content_rating'] == 'Very Good':
            cr_very_good_counter += 1
        elif row['content_rating'] == 'Good':
            cr_good_counter += 1
        elif row['content_rating'] == 'Fair':
            cr_fair_counter += 1
        elif row['content_rating'] == 'Poor':
            cr_poor_counter += 1

    result = [{
        'total_reviews': total_rows,
        'overall_rating_score': {
            'excellent': overall_excellent_counter,
            'very_good': overall_very_good_counter,
            'good': overall_good_counter,
            'fair': overall_fair_counter,
            'poor': overall_poor_counter
        },
        'presenting_skills_rating_score': {
            'excellent': ps_excellent_counter,
            'very_good': ps_very_good_counter,
            'good': ps_good_counter,
            'fair': ps_fair_counter,
            'poor': ps_poor_counter
        },
        'content_rating_score': {
            'excellent': cr_excellent_counter,
            'very_good': cr_very_good_counter,
            'good': cr_good_counter,
            'fair': cr_fair_counter,
            'poor': cr_poor_counter
        },
        'overall_sentiment_score': {
            'positive': positive_sentiment_counter,
            'neutral': neutral_sentiment_counter,
            'negative': negative_sentiment_counter
        }
    }]
    return jsonify(result)
