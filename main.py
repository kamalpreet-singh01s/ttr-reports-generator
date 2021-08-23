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
def index():
    host_url = request.host_url
    return render_template('index.html', host_url=host_url)


def sentiment_analyzer(data):
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(data)


@app.route("/tech_tuesday_reviews_analysis", methods=["POST"])
def csv_analysis():
    global presenter_name, presenter_name
    uploaded_file = request.files['csv_file']
    topic_name = request.form['topic_name']
    if not uploaded_file:
        return "No file Selected"
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

    oa_negative_sentiment_counter = 0
    oa_neutral_sentiment_counter = 0
    oa_positive_sentiment_counter = 0

    cp_negative_sentiment_counter = 0
    cp_neutral_sentiment_counter = 0
    cp_positive_sentiment_counter = 0

    bl_negative_sentiment_counter = 0
    bl_neutral_sentiment_counter = 0
    bl_positive_sentiment_counter = 0

    sp_negative_sentiment_counter = 0
    sp_neutral_sentiment_counter = 0
    sp_positive_sentiment_counter = 0

    total_rows = 0
    csv_input = csv.DictReader(stream)
    for row in csv_input:
        presenter_name = row['presenter_name']
        total_rows += 1
        input_data = row['comment_for_presenting']
        input_data1 = row['brief_learnt_detail']
        input_data2 = row['suggestion_for_presenting']
        oa_sentiment_dict = sentiment_analyzer(
            f'{input_data}, {input_data1}, {input_data2}')

        # Decide overall sentiment as positive, negative and neutral
        if oa_sentiment_dict['compound'] >= 0.05:
            oa_positive_sentiment_counter += 1
        elif oa_sentiment_dict['compound'] <= - 0.05:
            oa_negative_sentiment_counter += 1
        else:
            oa_neutral_sentiment_counter += 1

        cp_sentiment_dict = sentiment_analyzer(f'{input_data}')

        # Decide comment for presenting sentiment as positive, negative and neutral
        if cp_sentiment_dict['compound'] >= 0.05:
            cp_positive_sentiment_counter += 1
        elif cp_sentiment_dict['compound'] <= - 0.05:
            cp_negative_sentiment_counter += 1
        else:
            cp_neutral_sentiment_counter += 1

        bl_sentiment_dict = sentiment_analyzer(
            f'{input_data1}')

        # Decide brief learnt sentiment as positive, negative and neutral
        if bl_sentiment_dict['compound'] >= 0.05:
            bl_positive_sentiment_counter += 1
        elif bl_sentiment_dict['compound'] <= - 0.05:
            bl_negative_sentiment_counter += 1
        else:
            bl_neutral_sentiment_counter += 1

        sp_sentiment_dict = sentiment_analyzer(
            f'{input_data2}')

        # Decide suggestion for presentation sentiment as positive, negative and neutral
        if sp_sentiment_dict['compound'] >= 0.05:
            sp_positive_sentiment_counter += 1
        elif sp_sentiment_dict['compound'] <= - 0.05:
            sp_negative_sentiment_counter += 1
        else:
            sp_neutral_sentiment_counter += 1

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

    content_rate = {
        'Rating': 'Content Rating',
        'Excellent': cr_excellent_counter,
        'Very Good': cr_very_good_counter,
        'Good': cr_good_counter,
        'Fair': cr_fair_counter,
        'Poor': cr_poor_counter,
    }
    present_rate = {
        'Rating': 'Presenting Skills Rating',
        'Excellent': ps_excellent_counter,
        'Very Good': ps_very_good_counter,
        'Good': ps_good_counter,
        'Fair': ps_fair_counter,
        'Poor': ps_poor_counter
    }
    overall_rate = {
        'Rating': 'Overall Rating',
        'Excellent': overall_excellent_counter,
        'Very Good': overall_very_good_counter,
        'Good': overall_good_counter,
        'Fair': overall_fair_counter,
        'Poor': overall_poor_counter
    }
    overall_sentiment = {
        'Rating': 'Overall Sentiment Score',
        'Positive': oa_positive_sentiment_counter,
        'Neutral': oa_neutral_sentiment_counter,
        'Negative': oa_negative_sentiment_counter
    }

    comment_for_presenting_sentiment = {
        'Rating': 'Comment For Presenting Sentiment Score',
        'Positive': cp_positive_sentiment_counter,
        'Neutral': cp_neutral_sentiment_counter,
        'Negative': cp_negative_sentiment_counter
    }

    brief_learnt_sentiment = {
        'Rating': 'Brief Learnt Sentiment Score',
        'Positive': bl_positive_sentiment_counter,
        'Neutral': bl_neutral_sentiment_counter,
        'Negative': bl_negative_sentiment_counter
    }

    suggestion_for_presenting_sentiment = {
        'Rating': 'Suggestion For Presenting Sentiment Score',
        'Positive': sp_positive_sentiment_counter,
        'Neutral': sp_neutral_sentiment_counter,
        'Negative': sp_negative_sentiment_counter
    }

    data = {
        "content_rating": content_rate,
        "presenting_skills": present_rate,
        "overall_rating": overall_rate,
        "overall_sentiment": overall_sentiment,
        "comment_for_presenting_sentiment": comment_for_presenting_sentiment,
        "brief_learnt_sentiment": brief_learnt_sentiment,
        "suggestion_for_presenting_sentiment": suggestion_for_presenting_sentiment
    }

    return render_template('google_pie_chart.html', data=data, reviews=total_rows, presenter=presenter_name,
                           topic=topic_name)


@app.route('/api/upload_csv_file', methods=['POST'])
def upload_csv_file():
    uploaded_file = request.files['file']
    if not uploaded_file:
        return "No file"
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

    oa_negative_sentiment_counter = 0
    oa_neutral_sentiment_counter = 0
    oa_positive_sentiment_counter = 0

    cp_negative_sentiment_counter = 0
    cp_neutral_sentiment_counter = 0
    cp_positive_sentiment_counter = 0

    bl_negative_sentiment_counter = 0
    bl_neutral_sentiment_counter = 0
    bl_positive_sentiment_counter = 0

    sp_negative_sentiment_counter = 0
    sp_neutral_sentiment_counter = 0
    sp_positive_sentiment_counter = 0

    total_rows = 0

    csv_input = csv.DictReader(stream)
    for row in csv_input:
        total_rows += 1
        input_data = row['comment_for_presenting']
        input_data1 = row['brief_learnt_detail']
        input_data2 = row['suggestion_for_presenting']
        oa_sentiment_dict = sentiment_analyzer(
            f'{input_data}, {input_data1}, {input_data2}')

        # Decide overall sentiment as positive, negative and neutral
        if oa_sentiment_dict['compound'] >= 0.05:
            oa_positive_sentiment_counter += 1
        elif oa_sentiment_dict['compound'] <= - 0.05:
            oa_negative_sentiment_counter += 1
        else:
            oa_neutral_sentiment_counter += 1

        cp_sentiment_dict = sentiment_analyzer(f'{input_data}')

        # Decide comment for presenting sentiment as positive, negative and neutral
        if cp_sentiment_dict['compound'] >= 0.05:
            cp_positive_sentiment_counter += 1
        elif cp_sentiment_dict['compound'] <= - 0.05:
            cp_negative_sentiment_counter += 1
        else:
            cp_neutral_sentiment_counter += 1

        bl_sentiment_dict = sentiment_analyzer(f'{input_data1}')

        # Decide brief learnt sentiment as positive, negative and neutral
        if bl_sentiment_dict['compound'] >= 0.05:
            bl_positive_sentiment_counter += 1
        elif bl_sentiment_dict['compound'] <= - 0.05:
            bl_negative_sentiment_counter += 1
        else:
            bl_neutral_sentiment_counter += 1

        sp_sentiment_dict = sentiment_analyzer(f'{input_data2}')

        # Decide suggestion for presentation sentiment as positive, negative and neutral
        if sp_sentiment_dict['compound'] >= 0.05:
            sp_positive_sentiment_counter += 1
        elif sp_sentiment_dict['compound'] <= - 0.05:
            sp_negative_sentiment_counter += 1
        else:
            sp_neutral_sentiment_counter += 1

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
            'positive': oa_positive_sentiment_counter,
            'neutral': oa_neutral_sentiment_counter,
            'negative': oa_negative_sentiment_counter
        },
        'comment_for_presenting_sentiment': {
            'positive': cp_positive_sentiment_counter,
            'neutral': cp_neutral_sentiment_counter,
            'negative': cp_negative_sentiment_counter
        },
        'brief_learnt_sentiment': {
            'positive': bl_positive_sentiment_counter,
            'neutral': bl_neutral_sentiment_counter,
            'negative': bl_negative_sentiment_counter
        },
        'suggestion_for_presenting_sentiment': {
            'positive': sp_positive_sentiment_counter,
            'neutral': sp_neutral_sentiment_counter,
            'negative': sp_negative_sentiment_counter
        }
    }]
    
    return jsonify(result)
