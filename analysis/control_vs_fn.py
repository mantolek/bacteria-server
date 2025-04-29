import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

OUTPUT_FOLDER = 'output'

def analyze_control_vs_fn(xls, chart_type, colors=None):
    try:
        control = xls.parse('Control').set_index('Wavelength (nm)')
        fn = xls.parse('Fn').set_index('Wavelength (nm)')
    except Exception as e:
        raise ValueError(f"Missing required sheets: {str(e)}")

    merged = pd.concat([control.mean(axis=1), fn.mean(axis=1)], axis=1)
    merged.columns = ['Control', 'Fn']

    if chart_type == 'grouped_bar':
        image_path = os.path.join(OUTPUT_FOLDER, 'control_fn_bar.svg')
        plt.figure(figsize=(14, 8))

        color_list = [colors.get(col, None) for col in merged.columns] if colors else None

        merged.plot(kind='bar', figsize=(14, 8), color=color_list)

        plt.title("Control vs Fn – Grouped Bar Chart")
        plt.tight_layout()
        plt.savefig(image_path, format='svg', bbox_inches='tight')
        plt.close()

        return {"tytul": "Control vs Fn – Grouped Bar", "img": f"/output/{os.path.basename(image_path)}"}

    elif chart_type == 'violin':
        stacked = pd.concat([
            pd.DataFrame({'Value': control.values.flatten(), 'Group': 'Control'}),
            pd.DataFrame({'Value': fn.values.flatten(), 'Group': 'Fn'})
        ])

        image_path = os.path.join(OUTPUT_FOLDER, 'control_fn_violin.svg')
        plt.figure(figsize=(14, 8))

        palette = {group: colors.get(group) for group in stacked['Group'].unique()} if colors else None

        sns.violinplot(x='Group', y='Value', data=stacked, palette=palette)

        plt.title("Control vs Fn – Violin Plot")
        plt.tight_layout()
        plt.savefig(image_path, format='svg', bbox_inches='tight')
        plt.close()

        return {"tytul": "Control vs Fn – Violin Plot", "img": f"/output/{os.path.basename(image_path)}"}

    else:
        raise ValueError("Unsupported chart_type for ControlVsFn")
