import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import subprocess

OUTPUT_FOLDER = 'output'
INKSCAPE_PATH = "/Applications/Inkscape.app/Contents/MacOS/inkscape"  # dostosuj do systemu

def analyze_cfu(df, chart_type, colors=None, custom_title=None, x_label=None, y_label=None):
    df = df.copy()
    df.columns = [col.strip().lower() for col in df.columns]
    df = df.rename(columns={
        'group': 'Group',
        'sample': 'Sample',
        'time point': 'Time Point',
        'value': 'Value',
        'sd': 'Sd'
    })

    df = df.dropna(subset=['Time Point', 'Value', 'Group', 'Sd'])
    df['Time Point'] = df['Time Point'].astype(str)
    df['Group'] = df['Group'].astype(str)

    palette = {group: colors.get(group) for group in df['Group'].unique()} if colors else None

    if chart_type == 'bar':
        base_name = 'cfu_bar'
        svg_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.svg')
        emf_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.emf')

        plt.figure(figsize=(14, 8))

        ax = sns.barplot(
            data=df,
            x='Time Point',
            y='Value',
            hue='Group',
            palette=palette,
            errorbar=None
        )

        for bars, (name, group_df) in zip(ax.containers, df.groupby('Group')):
            for bar, (_, row) in zip(bars, group_df.iterrows()):
                height = bar.get_height()
                ax.errorbar(
                    bar.get_x() + bar.get_width() / 2,
                    height,
                    yerr=row['Sd'],
                    fmt='none',
                    ecolor='black',
                    capsize=5,
                    alpha=0.7
                )

        plt.title(custom_title.strip() if custom_title else "CFU/ml – Grouped Bar Chart")
        plt.xlabel(x_label.strip() if x_label else "Time Point")
        plt.ylabel(y_label.strip() if y_label else "CFU/ml")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False)
        plt.tight_layout()
        plt.savefig(svg_path, format='svg', bbox_inches='tight')
        plt.close()

    elif chart_type == 'line':
        base_name = 'cfu_line'
        svg_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.svg')
        emf_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.emf')

        plt.figure(figsize=(14, 8))

        sns.lineplot(
            data=df,
            x='Time Point',
            y='Value',
            hue='Group',
            palette=palette,
            marker='o',
            estimator=None,
            errorbar=None
        )

        for group_name, group_df in df.groupby('Group'):
            plt.errorbar(
                group_df['Time Point'],
                group_df['Value'],
                yerr=group_df['Sd'],
                fmt='none',
                capsize=5,
                color='black',
                alpha=0.7
            )

        plt.title(custom_title.strip() if custom_title else "CFU/ml – Line Chart Over Time")
        plt.xlabel(x_label.strip() if x_label else "Time Point")
        plt.ylabel(y_label.strip() if y_label else "CFU/ml")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False)
        plt.tight_layout()
        plt.savefig(svg_path, format='svg', bbox_inches='tight')
        plt.close()

    else:
        raise ValueError("Unsupported chart_type for CFU")

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
