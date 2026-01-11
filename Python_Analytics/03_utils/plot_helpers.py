# 03_utils/plot_helpers.py
import matplotlib.pyplot as plt
import seaborn as sns

def line_plot(df, x, y, title, xlabel, ylabel):
    sns.set(style="whitegrid")
    plt.figure(figsize=(8,5))
    sns.lineplot(data=df, x=x, y=y, marker='o')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def bar_plot(df, x, y, title, xlabel, ylabel, horizontal=False):
    sns.set(style="whitegrid")
    plt.figure(figsize=(8,5))
    if horizontal:
        sns.barplot(data=df, x=x, y=y)
    else:
        sns.barplot(data=df, x=x, y=y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def pie_chart(values, labels, title):
    plt.figure(figsize=(6,6))
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title(title)
    plt.show()
