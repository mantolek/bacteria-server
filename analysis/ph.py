import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

OUTPUT_FOLDER = 'output'

def pascal_case_columns(df):
    df.columns = [' '.join(word.capitalize() for word in col.split()) for col in df.columns]
    return df

def analyze_ph(df, chart_type, colors=None):
    df = pascal_case_columns(df)
    df = df.dropna(subset=['Time Point', 'Value', 'Group', 'Sd'])
    df['Time Point'] = df['Time Point'].astype(str)
    df['Group'] = df['Group'].astype(str)

    if chart_type == 'line':
        image_path = os.path.join(OUTPUT_FOLDER, 'ph_line.svg')
        plt.figure(figsize=(14, 8))

        palette = {group: colors.get(group) for group in df['Group'].unique()} if colors else None

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

        plt.title("pH Value – Line Chart Over Time")
        plt.xlabel("Time Point")
        plt.ylabel("pH Value")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False)
        plt.tight_layout()
        plt.savefig(image_path, format='svg', bbox_inches='tight')
        plt.close()

        return {"tytul": "pH – Line", "img": f"/output/{os.path.basename(image_path)}"}

    elif chart_type == 'boxplot':
        image_path = os.path.join(OUTPUT_FOLDER, 'ph_boxplot.svg')
        plt.figure(figsize=(14, 8))

        palette = {group: colors.get(group) for group in df['Group'].unique()} if colors else None

        sns.boxplot(
            data=df,
            x='Time Point',
            y='Value',
            hue='Group',
            palette=palette,
        )

        plt.title("pH Value – Boxplot by Time Point")
        plt.xlabel("Time Point")
        plt.ylabel("pH Value")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False)
        plt.tight_layout()
        plt.savefig(image_path, format='svg', bbox_inches='tight')
        plt.close()

        return {"tytul": "pH – Boxplot", "img": f"/output/{os.path.basename(image_path)}"}

    else:
        raise ValueError("Unsupported chart_type for pH")
