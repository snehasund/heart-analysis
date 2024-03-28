from flask import Flask, render_template
import pandas as pd
import seaborn as sns
import plotly.graph_objs as go
import json

app = Flask(__name__)

# Load the dataset
df = pd.read_csv('heart.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/countplot')
def countplot():
    count_data = df['target'].value_counts().reset_index()
    data = [go.Bar(x=count_data['index'], y=count_data['target'])]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('plot.html', graphJSON=graphJSON)

@app.route('/correlation')
def correlation():
    correlation_matrix = df.corr()
    data = [go.Heatmap(z=correlation_matrix.values.tolist(), x=correlation_matrix.columns, y=correlation_matrix.index)]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('plot.html', graphJSON=graphJSON)

@app.route('/boxplot')
def boxplot():
    data = [go.Box(y=df[df['target'] == 0]['age'], name='No Heart Disease'),
            go.Box(y=df[df['target'] == 1]['age'], name='Heart Disease')]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('plot.html', graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(debug=True)
