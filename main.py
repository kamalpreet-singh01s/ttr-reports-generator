from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from nltk.sentiment import SentimentIntensityAnalyzer
from configurations import DevelopmentConfig
import csv
import io

app = Flask(__name__)
CORS(app)
app.config.from_object(DevelopmentConfig)

@app.route("/")
def hello_world():
    host_url = request.host_url
    return render_template('index.html', host_url=host_url)

def sentiment_analyzer(data):
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(data)


@app.route("/tech_tuesday_reviews_analysis", methods=["POST"])
def csv_analysis():
    uploaded_file = request.files['csv_file']
    if not uploaded_file:
        return "No file Seleted"
    stream = io.StringIO(
        uploaded_file.stream.read().decode("UTF8"), newline=None)

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
        presenter_name = row['presenter_name']
        total_rows += 1
        input_data = row['comment_for_presenting']
        input_data1 = row['brief_learnt_detail']
        input_data2 = row['suggestion_for_presenting']
        sentiment_dict = sentiment_analyzer(
            f'{input_data}, {input_data1}, {input_data2}')

        # Decide sentiment as positive, negative and neutral
        if sentiment_dict['compound'] >= 0.05:
            positive_sentiment_counter += 1
        elif sentiment_dict['compound'] <= - 0.05:
            negative_sentiment_counter += 1
        else:
            neutral_sentiment_counter += 1

        # Increase overall rating counters
        if row['overall_rating'].lower() == 'excellent':
            overall_excellent_counter += 1
        elif row['overall_rating'].lower() == 'very good':
            overall_very_good_counter += 1
        elif row['overall_rating'].lower() == 'good':
            overall_good_counter += 1
        elif row['overall_rating'].lower() == 'fair':
            overall_fair_counter += 1
        elif row['overall_rating'].lower() == 'poor':
            overall_poor_counter += 1

        # Increase presenting skills rating counters
        if row['presentation_skills'].lower() == 'excellent':
            ps_excellent_counter += 1
        elif row['presentation_skills'].lower() == 'very good':
            ps_very_good_counter += 1
        elif row['presentation_skills'].lower() == 'good':
            ps_good_counter += 1
        elif row['presentation_skills'].lower() == 'fair':
            ps_fair_counter += 1
        elif row['presentation_skills'].lower() == 'poor':
            ps_poor_counter += 1

        # Increase content rating counters
        if row['content_rating'].lower() == 'excellent':
            cr_excellent_counter += 1
        elif row['content_rating'].lower() == 'very good':
            cr_very_good_counter += 1
        elif row['content_rating'].lower() == 'good':
            cr_good_counter += 1
        elif row['content_rating'].lower() == 'fair':
            cr_fair_counter += 1
        elif row['content_rating'].lower() == 'poor':
            cr_poor_counter += 1

    content_rate = {'Rating': 'Content Rating', 'Excellent': cr_excellent_counter, 'Very Good': cr_very_good_counter,
                    'Good': cr_good_counter, 'Fair': cr_fair_counter, 'Poor': cr_poor_counter}
    present_rate = {'Rating': 'Presenting Skillls Rating', 'Excellent': ps_excellent_counter, 'Very Good': ps_very_good_counter,
                    'Good': ps_good_counter, 'Fair': ps_fair_counter, 'Poor': ps_poor_counter}
    overall_rate = {'Rating': 'Overall Rating', 'Excellent': overall_excellent_counter, 'Very Good': overall_very_good_counter,
                    'Good': overall_good_counter, 'Fair': overall_fair_counter, 'Poor': overall_poor_counter}
    overall_sentiment = {'Rating': 'Overall Sentiment Score', 'Positive': positive_sentiment_counter, 'Neutral': neutral_sentiment_counter,
                         'Negative': negative_sentiment_counter}
    data = {
        "content_rating": content_rate,
        "presenting_skills": present_rate,
        "overall_rating": overall_rate,
        "overall_sentiment": overall_sentiment,
    }

    return render_template('google_pie_chart.html', data=data, reviews=total_rows, presenter=presenter_name)


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
