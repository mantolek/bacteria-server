import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import subprocess

OUTPUT_FOLDER = 'output'
# INKSCAPE_PATH = "/Applications/Inkscape.app/Contents/MacOS/inkscape"
INKSCAPE_PATH = "inkscape"

def pascal_case_columns(df):
    df.columns = [' '.join(word.capitalize() for word in col.split()) for col in df.columns]
    return df

def analyze_ph(df, chart_type, colors=None, custom_title=None, x_label=None, y_label=None):
    df = pascal_case_columns(df)
    df = df.dropna(subset=['Time Point', 'Value', 'Group', 'Sd'])
    df['Time Point'] = df['Time Point'].astype(str)
    df['Group'] = df['Group'].astype(str)

    palette = {group: colors.get(group) for group in df['Group'].unique()} if colors else None

    if chart_type == 'line':
        base_name = 'ph_line'
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
            errorbar=None,
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

        plt.title(custom_title.strip() if custom_title else "pH Value – Line Chart Over Time")
        plt.xlabel(x_label.strip() if x_label else "Time Point")
        plt.ylabel(y_label.strip() if y_label else "pH Value")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False)
        plt.tight_layout()
        plt.savefig(svg_path, format='svg', bbox_inches='tight')
        plt.close()

    elif chart_type == 'boxplot':
        base_name = 'ph_boxplot'
        svg_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.svg')
        emf_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.emf')

        plt.figure(figsize=(14, 8))

        sns.boxplot(
            data=df,
            x='Time Point',
            y='Value',
            hue='Group',
            palette=palette,
        )

        plt.title(custom_title.strip() if custom_title else "pH Value – Boxplot by Time Point")
        plt.xlabel(x_label.strip() if x_label else "Time Point")
        plt.ylabel(y_label.strip() if y_label else "pH Value")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False)
        plt.tight_layout()
        plt.savefig(svg_path, format='svg', bbox_inches='tight')
        plt.close()

    else:
        raise ValueError("Unsupported chart_type for pH")

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
