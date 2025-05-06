from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import os
import json
import random
from analysis import (
    analyze_qlf,
    analyze_hyperspectral,
    analyze_16s,
    analyze_lfc,
    analyze_ph,
    analyze_cfu,
    analyze_alpha_diversity,
    analyze_beta_diversity,
    analyze_lsms,
    analyze_correlations,
    analyze_fluorescence_over_time,
    analyze_control_vs_fn,
    analyze_smdi,
)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'

app = Flask(__name__)
CORS(app)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def clear_folders():
    for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
        for f in os.listdir(folder):
            os.remove(os.path.join(folder, f))

def random_color():
    """Generate a random hex color."""
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def validate_colors(groups, colors):
    """Ensure every group has a unique color. If missing or repeated, generate new ones."""
    if not colors:
        colors = {}

    validated = {}
    used_colors = set()

    for group in groups:
        color = colors.get(group)
        if not color or color in used_colors:
            new_color = random_color()
            while new_color in used_colors:
                new_color = random_color()
            validated[group] = new_color
            used_colors.add(new_color)
        else:
            validated[group] = color
            used_colors.add(color)

    return validated

@app.route('/analyze', methods=['POST'])
def analyze():
    clear_folders()

    file = request.files['file']
    analysis_type = request.form.get('analysis_type')
    chart_type = request.form.get('chart_type')
    colors_raw = request.form.get('colors')

    if not analysis_type or not chart_type:
        return jsonify({"error": "Missing analysis_type or chart_type"}), 400

    colors = None
    if colors_raw:
        try:
            colors = json.loads(colors_raw)  # bezpieczny JSON zamiast eval
        except Exception:
            colors = None

    filepath = os.path.join(UPLOAD_FOLDER, 'input.xlsx')
    file.save(filepath)
    xls = pd.ExcelFile(filepath)

    try:
        df = xls.parse(xls.sheet_names[0])
    except Exception as e:
        return jsonify({"error": f"Failed to read Excel sheet: {str(e)}"}), 400

    try:
        if analysis_type == 'QLF':
            groups = df['Group'].unique().tolist()
            colors = validate_colors(groups, colors)
            custom_title = request.form.get('custom_title')
            x_label = request.form.get('x_label')
            y_label = request.form.get('y_label')
            result = analyze_qlf(df, chart_type, colors, custom_title, x_label, y_label)

        elif analysis_type == 'Hyperspectral':
            groups = df['Group'].astype(str).str.strip().unique().tolist()
            if not colors:
                colors = validate_colors(groups, None)
            else:
                colors = {str(k).strip(): v for k, v in colors.items()}
            custom_title = request.form.get('custom_title')
            x_label = request.form.get('x_label')
            y_label = request.form.get('y_label')
            result = analyze_hyperspectral(df, chart_type, colors, custom_title, x_label, y_label)

        elif analysis_type == '16S':
            groups = df['Taxon Name'].unique().tolist()
            colors = validate_colors(groups, colors)
            custom_title = request.form.get('custom_title')
            x_label = request.form.get('x_label')
            y_label = request.form.get('y_label')
            result = analyze_16s(df, chart_type, colors, custom_title, x_label, y_label)

        elif analysis_type == 'LFC':
            custom_title = request.form.get('custom_title')
            x_label = request.form.get('x_label')
            y_label = request.form.get('y_label')
            result = analyze_lfc(df, chart_type, colors, custom_title, x_label, y_label)

        elif analysis_type == 'pH':
            groups = df['Group'].unique().tolist()
            colors = validate_colors(groups, colors)
            custom_title = request.form.get('custom_title')
            x_label = request.form.get('x_label')
            y_label = request.form.get('y_label')
            result = analyze_ph(df, chart_type, colors, custom_title, x_label, y_label)

        elif analysis_type == 'CFU':
            df.columns = [col.strip().lower() for col in df.columns]
            df = df.rename(columns={
                'group': 'Group',
                'sample': 'Sample',
                'time point': 'Time Point',
                'value': 'Value',
                'sd': 'Sd'
            })
            groups = df['Group'].unique().tolist()
            colors = validate_colors(groups, colors)
            custom_title = request.form.get('custom_title')
            x_label = request.form.get('x_label')
            y_label = request.form.get('y_label')
            result = analyze_cfu(df, chart_type, colors, custom_title, x_label, y_label)

        elif analysis_type == 'AlphaDiversity':
            groups = df['Group'].unique().tolist()
            colors = validate_colors(groups, colors)
            custom_title = request.form.get('custom_title')
            x_label = request.form.get('x_label')
            y_label = request.form.get('y_label')
            result = analyze_alpha_diversity(df, chart_type, colors, custom_title, x_label, y_label)

        elif analysis_type == 'BetaDiversity':
            groups = df['Group'].unique().tolist()
            colors = validate_colors(groups, colors)
            custom_title = request.form.get('custom_title')
            x_label = request.form.get('x_label')
            y_label = request.form.get('y_label')
            result = analyze_beta_diversity(df, chart_type, colors, custom_title, x_label, y_label)

        elif analysis_type == 'LSMS':
            groups = df['Compound'].unique().tolist()
            colors = validate_colors(groups, colors)
            custom_title = request.form.get('custom_title')
            x_label = request.form.get('x_label')
            y_label = request.form.get('y_label')
            result = analyze_lsms(df, chart_type, colors, custom_title, x_label, y_label)

        elif analysis_type == 'Correlations':
            custom_title = request.form.get('custom_title')
            x_label = request.form.get('x_label')
            y_label = request.form.get('y_label')
            result = analyze_correlations(df, chart_type, colors, custom_title, x_label, y_label)

        elif analysis_type == 'FluorescenceOverTime':
            custom_title = request.form.get('custom_title')
            x_label = request.form.get('x_label')
            y_label = request.form.get('y_label')
            result = analyze_fluorescence_over_time(df, chart_type, colors, custom_title, x_label, y_label)

        elif analysis_type == 'ControlVsFn':
            groups = ['Control', 'Fn']
            colors = validate_colors(groups, colors)
            custom_title = request.form.get('custom_title')
            x_label = request.form.get('x_label')
            y_label = request.form.get('y_label')
            result = analyze_control_vs_fn(xls, chart_type, colors, custom_title, x_label, y_label)

        elif analysis_type == 'SMDI':
            groups = df['Group'].unique().tolist()
            colors = validate_colors(groups, colors)
            custom_title = request.form.get('custom_title')
            x_label = request.form.get('x_label')
            y_label = request.form.get('y_label')

            result = analyze_smdi(df, chart_type, colors, custom_title, x_label, y_label)
        else:
            return jsonify({"error": "Unsupported analysis_type"}), 400

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Processing error: {str(e)}"}), 400

@app.route('/output/<filename>')
def serve_output_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050)

# source venv/bin/activate
# python app.py