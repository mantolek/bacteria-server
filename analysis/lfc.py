import matplotlib
matplotlib.use('Agg')
import os
import matplotlib.pyplot as plt
import seaborn as sns
import subprocess

OUTPUT_FOLDER = 'output'
INKSCAPE_PATH = "/Applications/Inkscape.app/Contents/MacOS/inkscape"  # dopasuj do środowiska

def analyze_lfc(df, chart_type, colors=None, custom_title=None, x_label=None, y_label=None):
    numeric_df = df.select_dtypes(include='number')
    filtered_df = numeric_df.where(numeric_df > 2)

    if 'Taxon Name' in df.columns:
        filtered_df['Taxon Name'] = df['Taxon Name']

    if 'Taxon Name' in filtered_df.columns:
        filtered_df = filtered_df.set_index('Taxon Name')

    if filtered_df.dropna(how='all').empty:
        raise ValueError("No data points with absolute LFC > 2 after filtering.")

    if chart_type == 'bar':
        base_name = 'lfc_bar'
        svg_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.svg')
        emf_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.emf')

        plt.figure(figsize=(14, 8))
        mean_values = filtered_df.mean(axis=1).dropna().sort_values()
        color_list = [colors.get(taxon, None) for taxon in mean_values.index] if colors else None

        ax = mean_values.plot(
            kind='barh',
            figsize=(14, 8),
            color=color_list
        )

        plt.title(custom_title.strip() if custom_title else "Log Fold Change – Mean Change per Taxon")
        plt.xlabel(x_label.strip() if x_label else "log2 Fold Change")
        plt.ylabel(y_label.strip() if y_label else "Taxon Name")
        ax.legend().set_visible(False)

        plt.tight_layout()
        plt.savefig(svg_path, format='svg', bbox_inches='tight')
        plt.close()

    elif chart_type == 'heatmap':
        base_name = 'lfc_heatmap'
        svg_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.svg')
        emf_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.emf')

        plt.figure(figsize=(14, 8))

        sns.heatmap(filtered_df, cmap="vlag", center=0)

        plt.title(custom_title.strip() if custom_title else "Log Fold Change – Heatmap")
        if x_label: plt.xlabel(x_label.strip())
        if y_label: plt.ylabel(y_label.strip())

        plt.tight_layout()
        plt.savefig(svg_path, format='svg', bbox_inches='tight')
        plt.close()

    else:
        raise ValueError("Unsupported chart_type for LFC")

    try:
        subprocess.run([
            INKSCAPE_PATH,
            svg_path,
            "--export-type=emf",
            "--export-filename", emf_path
        ], check=True)
    except Exception as e:
        return {"error": f"Failed to convert SVG to EMF: {str(e)}"}

    return {
        "tytul": custom_title.strip() if custom_title else base_name.replace("_", " ").title(),
        "img_svg": f"/output/{os.path.basename(svg_path)}",
        "img_emf": f"/output/{os.path.basename(emf_path)}"
    }
