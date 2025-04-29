import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

OUTPUT_FOLDER = 'output'

def pascal_case_columns(df):
    df.columns = [' '.join(word.capitalize() for word in col.split()) for col in df.columns]
    return df

def analyze_cfu(df, chart_type, colors=None):
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
        image_path = os.path.join(OUTPUT_FOLDER, 'cfu_bar.svg')
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

        plt.title("CFU/ml – Grouped Bar Chart")
        plt.xlabel("Time Point")
        plt.ylabel("CFU/ml")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False)
        plt.tight_layout()
        plt.savefig(image_path, format='svg', bbox_inches='tight')
        plt.close()

        return {"tytul": "CFU – Bar", "img": f"/output/{os.path.basename(image_path)}"}

    elif chart_type == 'line':
        image_path = os.path.join(OUTPUT_FOLDER, 'cfu_line.svg')
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

        plt.title("CFU/ml – Line Chart Over Time")
        plt.xlabel("Time Point")
        plt.ylabel("CFU/ml")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False)
        plt.tight_layout()
        plt.savefig(image_path, format='svg', bbox_inches='tight')
        plt.close()

        return {"tytul": "CFU – Line", "img": f"/output/{os.path.basename(image_path)}"}

    else:
        raise ValueError("Unsupported chart_type for CFU")
