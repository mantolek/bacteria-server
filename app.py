from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os
from flask_cors import CORS
import numpy as np
from sklearn.decomposition import PCA
from scipy.stats import linregress

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def clear_folders():
    for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
        for f in os.listdir(folder):
            os.remove(os.path.join(folder, f))

@app.route('/analyze', methods=['POST'])
def analyze():
    clear_folders()

    file = request.files['file']
    analysis_type = request.form.get('analysis_type')
    chart_type = request.form.get('chart_type')

    if not analysis_type or not chart_type:
         return jsonify({"error": "Missing analysis_type or chart_type"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, 'input.xlsx')
    file.save(filepath)
    xls = pd.ExcelFile(filepath)

    try:
        df = xls.parse(xls.sheet_names[0])
    except Exception as e:
         return jsonify({"error": f"Failed to read Excel sheet: {str(e)}"}), 400


    if analysis_type == 'QLF':
        if chart_type == 'bar':
            image_path = os.path.join(OUTPUT_FOLDER, 'qlf_bar.png')
            plt.figure(figsize=(8, 5))
            sns.barplot(data=df, x='Point', y='R/G Value (Mean)', hue='Group', ci=None)
            plt.errorbar(df['Point'], df['R/G Value (Mean)'], yerr=df['R/G Value (SD)'], fmt='none', c='black', capsize=5)
            plt.title("QLF – RGB Bar Chart")
            plt.tight_layout()
            plt.savefig(image_path)
            plt.close()
        elif chart_type == 'heatmap':
            image_path = os.path.join(OUTPUT_FOLDER, 'qlf_heatmap.png')
            pivot = df.pivot(index='Point', columns='Group', values='R/G Value (Mean)')
            plt.figure(figsize=(8, 6))
            sns.heatmap(pivot, annot=True, cmap="coolwarm", cbar_kws={'label': 'R/G Value'})
            plt.title("QLF – RGB Heatmap")
            plt.tight_layout()
            plt.savefig(image_path)
            plt.close()
        else:
            return jsonify({"error": "Unsupported chart_type for QLF"}), 400

        result = {"tytul": f"QLF – {chart_type}", "img": f"/output/{os.path.basename(image_path)}"}

    elif analysis_type == 'Hyperspectral':
        if chart_type == 'lines':
            image_path = os.path.join(OUTPUT_FOLDER, 'hyperspectral_lines.png')
            plt.figure(figsize=(10, 6))
            for group in df['Group'].unique():
                subset = df[df['Group'] == group]
                plt.plot(subset['Wavelength'], subset['Intensity'], label=group)
            plt.title("Hyperspectral – Spectral Lines")
            plt.xlabel("Wavelength (nm)")
            plt.ylabel("Intensity")
            plt.legend()
            plt.tight_layout()
            plt.savefig(image_path)
            plt.close()
        else:
            return jsonify({"error": "Unsupported chart_type for Hyperspectral"}), 400

        result = {"tytul": f"Hyperspectral – {chart_type}", "img": f"/output/{os.path.basename(image_path)}"}

    elif analysis_type == '16S':
        df.set_index('Taxon Name', inplace=True)
        df = df.astype(float)

        if chart_type == 'bar':
            image_path = os.path.join(OUTPUT_FOLDER, '16s_stacked_bar.png')
            df.T.plot(kind='bar', stacked=True, figsize=(12, 6))
            plt.title("16S rRNA – Stacked Bar Chart")
            plt.xlabel("Sample")
            plt.ylabel("Relative Abundance")
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            plt.savefig(image_path)
            plt.close()
        elif chart_type == 'pie':
            image_path = os.path.join(OUTPUT_FOLDER, '16s_pie.png')
            summed = df.sum(axis=1)
            top = summed.nlargest(10)
            plt.figure(figsize=(8, 8))
            plt.pie(top, labels=top.index, autopct='%1.1f%%')
            plt.title("16S rRNA – Top 10 Taxa (Pie Chart)")
            plt.tight_layout()
            plt.savefig(image_path)
            plt.close()
        elif chart_type == 'heatmap':
            image_path = os.path.join(OUTPUT_FOLDER, '16s_heatmap.png')
            plt.figure(figsize=(10, 6))
            sns.heatmap(df, cmap="YlGnBu")
            plt.title("16S rRNA – Heatmap")
            plt.tight_layout()
            plt.savefig(image_path)
            plt.close()
        else:
            return jsonify({"error": "Unsupported chart_type for 16S"}), 400

        result = {"tytul": f"16S – {chart_type}", "img": f"/output/{os.path.basename(image_path)}"}

    elif analysis_type == 'LFC':
        df.set_index('Taxon Name', inplace=True)
        df = df.astype(float)

        if chart_type == 'bar':
            image_path = os.path.join(OUTPUT_FOLDER, 'lfc_bar.png')
            df.mean(axis=1).sort_values().plot(kind='barh', figsize=(10, 8))
            plt.title("Log Fold Change – Mean Change per Taxon")
            plt.xlabel("log2 Fold Change")
            plt.tight_layout()
            plt.savefig(image_path)
            plt.close()
        elif chart_type == 'heatmap':
            image_path = os.path.join(OUTPUT_FOLDER, 'lfc_heatmap.png')
            plt.figure(figsize=(10, 6))
            sns.heatmap(df, cmap="vlag", center=0)
            plt.title("Log Fold Change – Heatmap")
            plt.tight_layout()
            plt.savefig(image_path)
            plt.close()
        else:
            return jsonify({"error": "Unsupported chart_type for LFC"}), 400

        result = {"tytul": f"LFC – {chart_type}", "img": f"/output/{os.path.basename(image_path)}"}

    elif analysis_type == 'pH':
        if chart_type == 'boxplot':
            image_path = os.path.join(OUTPUT_FOLDER, 'ph_boxplot.png')
            plt.figure(figsize=(8, 6))
            sns.boxplot(data=df, x='Time Point', y='Value', hue='Group')
            plt.title("pH Value – Boxplot by Time Point")
            plt.tight_layout()
            plt.savefig(image_path)
            plt.close()
        elif chart_type == 'line':
            image_path = os.path.join(OUTPUT_FOLDER, 'ph_line.png')
            plt.figure(figsize=(8, 6))
            sns.lineplot(data=df, x='Time Point', y='Value', hue='Group', estimator='mean')
            plt.title("pH Value – Line Chart Over Time")
            plt.tight_layout()
            plt.savefig(image_path)
            plt.close()
        else:
            return jsonify({"error": "Unsupported chart_type for pH"}), 400

        result = {"tytul": f"pH – {chart_type}", "img": f"/output/{os.path.basename(image_path)}"}

    elif analysis_type == 'CFU':
        if chart_type == 'line':
            image_path = os.path.join(OUTPUT_FOLDER, 'cfu_line.png')
            plt.figure(figsize=(8, 6))
            sns.lineplot(data=df, x='Time Point', y='Value', hue='Group', estimator='mean')
            plt.title("CFU/ml – Line Chart Over Time")
            plt.tight_layout()
            plt.savefig(image_path)
            plt.close()
        elif chart_type == 'bar':
            image_path = os.path.join(OUTPUT_FOLDER, 'cfu_bar.png')
            plt.figure(figsize=(8, 6))
            sns.barplot(data=df, x='Time Point', y='Value', hue='Group')
            plt.title("CFU/ml – Grouped Bar Chart")
            plt.tight_layout()
            plt.savefig(image_path)
            plt.close()
        else:
            return jsonify({"error": "Unsupported chart_type for CFU"}), 400

        result = {"tytul": f"CFU – {chart_type}", "img": f"/output/{os.path.basename(image_path)}"}

    elif analysis_type == 'AlphaDiversity':
        if chart_type == 'boxplot':
            image_path = os.path.join(OUTPUT_FOLDER, 'alpha_diversity_boxplot.png')
            plt.figure(figsize=(8, 6))
            sns.boxplot(data=df, x='Group', y='AlphaDiversity')
            plt.title("Alpha Diversity – Boxplot")
            plt.tight_layout()
            plt.savefig(image_path)
            plt.close()
        else:
            return jsonify({"error": "Unsupported chart_type for AlphaDiversity"}), 400

        result = {"tytul": f"Alpha Diversity – {chart_type}", "img": f"/output/{os.path.basename(image_path)}"}

    elif analysis_type == 'BetaDiversity':
        if chart_type == 'scatter':
            image_path = os.path.join(OUTPUT_FOLDER, 'beta_scatter.png')
            plt.figure(figsize=(8, 6))
            sns.scatterplot(data=df, x='Axis1', y='Axis2', hue='Group')
            plt.title("β-diversity (PCoA)")
            plt.tight_layout()
            plt.savefig(image_path)
            plt.close()
        else:
            return jsonify({"error": "Unsupported chart_type for BetaDiversity"}), 400

        result = {"tytul": f"BetaDiversity – {chart_type}", "img": f"/output/{os.path.basename(image_path)}"}

    elif analysis_type == 'LSMS':
        df.set_index('Compound', inplace=True)
        if chart_type == 'bar':
            image_path = os.path.join(OUTPUT_FOLDER, 'lsms_bar.png')
            df.T.plot(kind='bar', figsize=(10, 6))
            plt.title("LS/MS – Signal Intensity")
            plt.tight_layout()
            plt.savefig(image_path)
            plt.close()
        elif chart_type == 'pca':
            pca = PCA(n_components=2)
            components = pca.fit_transform(df.T)
            image_path = os.path.join(OUTPUT_FOLDER, 'lsms_pca.png')
            plt.figure(figsize=(8, 6))
            plt.scatter(components[:, 0], components[:, 1])
            plt.title("LS/MS – PCA")
            plt.tight_layout()
            plt.savefig(image_path)
            plt.close()
        else:
            return jsonify({"error": "Unsupported chart_type for LSMS"}), 400

        result = {"tytul": f"LSMS – {chart_type}", "img": f"/output/{os.path.basename(image_path)}"}

    elif analysis_type == 'Correlations':
        if chart_type == 'scatter_reg':
            image_path = os.path.join(OUTPUT_FOLDER, 'correlation.png')
            plt.figure(figsize=(8, 6))
            sns.regplot(data=df, x='Parameter_1', y='Parameter_2')
            plt.title("Correlation Between Parameters")
            plt.tight_layout()
            plt.savefig(image_path)
            plt.close()
        else:
            return jsonify({"error": "Unsupported chart_type for Correlations"}), 400

        result = {"tytul": f"Correlations – {chart_type}", "img": f"/output/{os.path.basename(image_path)}"}

    elif analysis_type == 'FluorescenceOverTime':
        df.set_index('Wavelength (nm)', inplace=True)
        if chart_type == 'line':
            image_path = os.path.join(OUTPUT_FOLDER, 'fluorescence_line.png')
            df.T.plot(figsize=(10, 6))
            plt.title("Fluorescence Change Over Time")
            plt.xlabel("Time")
            plt.ylabel("Intensity")
            plt.tight_layout()
            plt.savefig(image_path)
            plt.close()
        elif chart_type == 'surface':
            from mpl_toolkits.mplot3d import Axes3D
            X, Y = np.meshgrid(df.columns, df.index)
            Z = df.values
            image_path = os.path.join(OUTPUT_FOLDER, 'fluorescence_surface.png')
            fig = plt.figure(figsize=(10, 7))
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(X, Y, Z, cmap='viridis')
            ax.set_xlabel("Time")
            ax.set_ylabel("Wavelength")
            ax.set_zlabel("Intensity")
            plt.tight_layout()
            plt.savefig(image_path)
            plt.close()
        else:
            return jsonify({"error": "Unsupported chart_type for FluorescenceOverTime"}), 400

        result = {"tytul": f"FluorescenceOverTime – {chart_type}", "img": f"/output/{os.path.basename(image_path)}"}

    elif analysis_type == 'ControlVsFn':
        try:
            control = xls.parse('Control').set_index('Wavelength (nm)')
            fn = xls.parse('Fn').set_index('Wavelength (nm)')
        except Exception as e:
            return jsonify({"error": f"Missing required sheets: {str(e)}"}), 400

        merged = pd.concat([control.mean(axis=1), fn.mean(axis=1)], axis=1)
        merged.columns = ['Control', 'Fn']

        if chart_type == 'grouped_bar':
            image_path = os.path.join(OUTPUT_FOLDER, 'control_fn_bar.png')
            merged.plot(kind='bar', figsize=(10, 6))
            plt.title("Control vs Fn – Grouped Bar Chart")
            plt.tight_layout()
            plt.savefig(image_path)
            plt.close()
        elif chart_type == 'violin':
            stacked = pd.concat([
                pd.DataFrame({'Value': control.values.flatten(), 'Group': 'Control'}),
                pd.DataFrame({'Value': fn.values.flatten(), 'Group': 'Fn'})
            ])
            image_path = os.path.join(OUTPUT_FOLDER, 'control_fn_violin.png')
            plt.figure(figsize=(8, 6))
            sns.violinplot(x='Group', y='Value', data=stacked)
            plt.title("Control vs Fn – Violin Plot")
            plt.tight_layout()
            plt.savefig(image_path)
            plt.close()
        else:
            return jsonify({"error": "Unsupported chart_type for ControlVsFn"}), 400

        result = {"tytul": f"ControlVsFn – {chart_type}", "img": f"/output/{os.path.basename(image_path)}"}

    elif analysis_type == 'SMDI':
        if chart_type == 'boxplot':
            image_path = os.path.join(OUTPUT_FOLDER, 'smdi_boxplot.png')
            plt.figure(figsize=(8, 6))
            sns.boxplot(data=df, x='Group', y='SMDI_Value')
            plt.title("SMDI – Boxplot")
            plt.tight_layout()
            plt.savefig(image_path)
            plt.close()
        elif chart_type == 'bar':
            image_path = os.path.join(OUTPUT_FOLDER, 'smdi_bar.png')
            plt.figure(figsize=(8, 6))
            sns.barplot(data=df, x='Group', y='SMDI_Value', ci='sd')
            plt.title("SMDI – Bar Chart")
            plt.tight_layout()
            plt.savefig(image_path)
            plt.close()
        else:
            return jsonify({"error": "Unsupported chart_type for SMDI"}), 400

        result = {"tytul": f"SMDI – {chart_type}", "img": f"/output/{os.path.basename(image_path)}"}


    else:
        return jsonify({"error": "Unsupported analysis_type"}), 400

    return jsonify(result)

@app.route('/output/<filename>')
def serve_output_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
