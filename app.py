from flask import Flask, render_template_string
from graph_visualizer import draw_graph, load_state_and_genes

app = Flask(__name__)

@app.route('/')
def home():
    try:
        states_in, genes_in = load_state_and_genes()
        image_base64 = draw_graph(states_in, genes_in)
    except FileNotFoundError:
        return "State and genes file not found. Please ensure branches.py is running and saving the state and genes."

    return render_template_string('''
        <!doctype html>
        <title>Node Graph</title>
        <h1>Node Graph</h1>
        <img src="data:image/png;base64,{{ image_base64 }}">
    ''', image_base64=image_base64)

if __name__ == '__main__':
    app.run(debug=True)