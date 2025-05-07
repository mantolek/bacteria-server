import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import subprocess

OUTPUT_FOLDER = 'output'
# INKSCAPE_PATH = "/Applications/Inkscape.app/Contents/MacOS/inkscape"
INKSCAPE_PATH = "inkscape"

def analyze_control_vs_fn(xls, chart_type, colors=None, custom_title=None, x_label=None, y_label=None):
    try:
        control = xls.parse('Control').set_index('Wavelength (nm)')
        fn = xls.parse('Fn').set_index('Wavelength (nm)')
    except Exception as e:
        raise ValueError(f"Missing required sheets: {str(e)}")

    merged = pd.concat([control.mean(axis=1), fn.mean(axis=1)], axis=1)
    merged.columns = ['Control', 'Fn']

    if chart_type == 'grouped_bar':
        base_name = 'control_fn_bar'
        svg_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.svg')
        emf_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.emf')

        color_list = [colors.get(col, None) for col in merged.columns] if colors else None

        plt.figure(figsize=(14, 8))
        merged.plot(kind='bar', color=color_list, ax=plt.gca())

        plt.title(custom_title.strip() if custom_title else "Control vs Fn – Grouped Bar Chart")
        plt.xlabel(x_label.strip() if x_label else "Wavelength Index")
        plt.ylabel(y_label.strip() if y_label else "Mean Value")
        plt.tight_layout()
        plt.savefig(svg_path, format='svg', bbox_inches='tight')
        plt.close()

    elif chart_type == 'violin':
        base_name = 'control_fn_violin'
        svg_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.svg')
        emf_path = os.path.join(OUTPUT_FOLDER, f'{base_name}.emf')

        stacked = pd.concat([
            pd.DataFrame({'Value': control.values.flatten(), 'Group': 'Control'}),
            pd.DataFrame({'Value': fn.values.flatten(), 'Group': 'Fn'})
        ])

        palette = {group: colors.get(group) for group in stacked['Group'].unique()} if colors else None

        plt.figure(figsize=(14, 8))
        sns.violinplot(x='Group', y='Value', data=stacked, palette=palette)

        plt.title(custom_title.strip() if custom_title else "Control vs Fn – Violin Plot")
        plt.xlabel(x_label.strip() if x_label else "Group")
        plt.ylabel(y_label.strip() if y_label else "Value")
        plt.tight_layout()
        plt.savefig(svg_path, format='svg', bbox_inches='tight')
        plt.close()

    else:
        raise ValueError("Unsupported chart_type for ControlVsFn")

    # Konwersja do EMF
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
