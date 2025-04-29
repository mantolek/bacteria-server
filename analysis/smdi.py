import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

OUTPUT_FOLDER = 'output'

def analyze_smdi(df, chart_type, colors=None):
    df = df.copy()
    df.columns = [col.strip().lower() for col in df.columns]
    df = df.rename(columns={
        'group': 'Group',
        'smdi_value': 'SMDI_Value'
    })

    df['Group'] = df['Group'].astype(str)

    palette = {group: colors.get(group) for group in df['Group'].unique()} if colors else None

    if chart_type == 'boxplot':
        image_path = os.path.join(OUTPUT_FOLDER, 'smdi_boxplot.svg')
        plt.figure(figsize=(14, 8))

        sns.boxplot(data=df, x='Group', y='SMDI_Value', palette=palette)

        plt.title("SMDI – Boxplot")
        plt.tight_layout()
        plt.savefig(image_path, format='svg', bbox_inches='tight')
        plt.close()

        return {"tytul": "SMDI – Boxplot", "img": f"/output/{os.path.basename(image_path)}"}

    elif chart_type == 'bar':
        image_path = os.path.join(OUTPUT_FOLDER, 'smdi_bar.svg')
        plt.figure(figsize=(14, 8))

        sns.barplot(data=df, x='Group', y='SMDI_Value', ci='sd', palette=palette)

        plt.title("SMDI – Bar Chart")
        plt.tight_layout()
        plt.savefig(image_path, format='svg', bbox_inches='tight')
        plt.close()

        return {"tytul": "SMDI – Bar Chart", "img": f"/output/{os.path.basename(image_path)}"}

    else:
        raise ValueError("Unsupported chart_type for SMDI")
