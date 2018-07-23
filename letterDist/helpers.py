from itertools import islice

import pandas as pd
import matplotlib.pylab as plt
from matplotlib.lines import Line2D
import seaborn as sns
import numpy as np

SCRABBLE = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4,
            'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1,
            'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1,
            's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8,
            'y': 4, 'z': 10}

POINT_COLORS = {1: 'C0', 2: 'C1', 3: 'C2',
                4: 'C3', 5: 'C4', 8: 'C5',
                10: 'C6'}





def make_letter_dict():
    eachLetter = [chr(x+97) for x in range(26)]
    eachLetter = dict.fromkeys(eachLetter, dict())
    return eachLetter

def load_all_words():
    words = []

    with open('data/popular.txt') as f:
        for line in f:
            words.append(line.strip())
    return words

def get_letter_dists(corpus, asFrame=False):
    eachLetter = [chr(x+97) for x in range(26)]
    eachLetter = dict.fromkeys(eachLetter)
    
    for letter in eachLetter:
        eachLetter[letter] = dict()
        
    for word in corpus:
        for idx, letter in enumerate(word):
            eachLetter[letter][idx] = eachLetter[letter].get(idx, 0) + 1
            
    if asFrame:
        return pd.DataFrame(eachLetter).fillna(0)
    return eachLetter

def plot_letter_dists(df):
    '''
    Make 5x6 plot of letter distributins from a DF containing:
        cols: letters
        rows: place in word
        values: counts
    '''
    fig, axes = plt.subplots(5, 6, figsize=(16, 8))
    for idx, (ax, col) in enumerate(zip(axes.flatten(), df)) :
        ax.bar(df.index, df[col])
        ax.set_title(col)
        ax.set_xlim(-1, 15)
        ax.get_yaxis().set_visible(False)
    else:
        # clean up unused axes
        [ax.set_visible(False) for ax in axes.flatten()[idx+1:]]
    plt.subplots_adjust(hspace=.75)
    plt.suptitle('Letter Distributions by Location in Word',
                       fontsize=16)


def letter_dist_heatmap(df):
    # Revisualizes the distributions as a percent
    # of a letter's total use
    vals = (df / df.sum()).loc[:8].T.values

    sns.heatmap(vals, cmap='plasma')
    fig = plt.gcf()
    fig.set_size_inches(16, 10)
    ax = plt.gca()
    yax = ax.get_yaxis()
    yax.set_ticks(np.arange(0.5, 26.5, 1))
    _ = yax.set_ticklabels(SCRABBLE.keys())


def points_legend(fig, loc):
    ''' Make a custom legend tying point colors to point values '''
    custom_lines = [Line2D([0], [0], color='C0', lw=4),
                    Line2D([0], [0], color='C1', lw=4),
                    Line2D([0], [0], color='C2', lw=4),
                    Line2D([0], [0], color='C3', lw=4),
                    Line2D([0], [0], color='C4', lw=4),
                    Line2D([0], [0], color='C5', lw=4),
                    Line2D([0], [0], color='C6', lw=4)]
    fig.legend(custom_lines, ['1', '2', '3', '4', '5', '8', '10'],
               title='Points', loc=loc)



# Couldn't figure out how to cleanly use the original
# plot_letter_dists function while still adding in the
# color functionality. Would love a PR on this :)
def plot_letter_dists_scrabble(df):
    '''
    Make 5x6 plot of letter distributins from a DF containing:
        cols: letters
        rows: place in word
        values: counts
    '''
    fig, axes = plt.subplots(5, 6, figsize=(16, 8))
    for idx, (ax, col) in enumerate(zip(axes.flatten(), df)) :
        ax.bar(df.index, df[col], color=POINT_COLORS[SCRABBLE[col]])
        ax.set_title(col)
        ax.set_xlim(-1, 15)
        ax.get_yaxis().set_visible(False)
    else:
        [ax.set_visible(False) for ax in axes.flatten()[idx+1:]]
    plt.subplots_adjust(hspace=.75)

    points_legend(fig, 'right')

    plt.suptitle('Letter Distributions by Location in Word', fontsize=20)


def plot_letter_volume_scrabble(df):
    fig, ax = plt.subplots(figsize= (10, 6))

    counts = df.sum()
    counts.plot(kind='bar')
    ax.tick_params(axis='x', rotation=0)

    bars = islice(ax.get_children(), 26)

    for letter, bar in zip(ax.xaxis.get_ticklabels(), bars):
        bar.set_color(POINT_COLORS[SCRABBLE[letter.get_text()]])
        
    points_legend(ax, 'best')
    plt.suptitle('Overall Letter Usage, by Scrabble Points', fontsize=16)
