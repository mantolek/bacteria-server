import matplotlib
matplotlib.use('Agg')
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA

OUTPUT_FOLDER = 'output'

def analyze_lfc(df, chart_type, colors=None):
    numeric_df = df.select_dtypes(include='number')
    filtered_df = numeric_df.where(numeric_df > 2)

    if 'Taxon Name' in df.columns:
        filtered_df['Taxon Name'] = df['Taxon Name']

    if 'Taxon Name' in filtered_df.columns:
        filtered_df = filtered_df.set_index('Taxon Name')

    if filtered_df.dropna(how='all').empty:
        raise ValueError("No data points with absolute LFC > 2 after filtering.")

    if chart_type == 'bar':
        image_path = os.path.join(OUTPUT_FOLDER, 'lfc_bar.svg')
        plt.figure(figsize=(14, 8))

        mean_values = filtered_df.mean(axis=1).dropna().sort_values()

        color_list = [colors.get(taxon, None) for taxon in mean_values.index] if colors else None

        ax = mean_values.plot(
            kind='barh',
            figsize=(14, 8),
            color=color_list
        )

        plt.title("Log Fold Change – Mean Change per Taxon")
        plt.xlabel("log2 Fold Change")
        plt.ylabel("Taxon Name")
        ax.legend().set_visible(False)

        plt.savefig(image_path, format='svg', bbox_inches='tight')
        plt.close()

        return {"tytul": "Log Fold Change – Bar", "img": f"/output/{os.path.basename(image_path)}"}

    elif chart_type == 'heatmap':
        image_path = os.path.join(OUTPUT_FOLDER, 'lfc_heatmap.svg')
        plt.figure(figsize=(14, 8))

        sns.heatmap(filtered_df, cmap="vlag", center=0)

        plt.title("Log Fold Change – Heatmap")
        plt.savefig(image_path, format='svg', bbox_inches='tight')
        plt.close()

        return {"tytul": "Log Fold Change – Heatmap", "img": f"/output/{os.path.basename(image_path)}"}

    else:
        raise ValueError("Unsupported chart_type for LFC")
