

```python
%pylab inline

from letterDist.helpers import (make_letter_dict, load_all_words,
                                get_letter_dists, plot_letter_dists, 
                                plot_just_k,
                                letter_dist_heatmap, points_legend, 
                                plot_letter_dists_scrabble,
                                plot_letter_volume_scrabble)
```

    Populating the interactive namespace from numpy and matplotlib
    

It's been a busy couple of months.

I'm working in a software engineer-ier capacity these days, building out a Sphinx-based documentation platform, standing up a Package Index for library code we've been brewing, and doing all kinds of internal writing about standards and best practices. Job title still says "Senior Data Analyst," but I've been signing emails as [developer advocate](https://medium.com/@ashleymcnamara/what-is-developer-advocacy-3a92442b627c)-- an excellent characterization of what I've been up to these past couple years. It's been slow-going and frankly a bit taxing, but I'm optimistic that it'll translate into my doing some quality data science once things are platformed a bit better.

Of course, since I'm learning a whole lot during the day, my *constructive* extracurricular work has fallen to the wayside. And in turn my "decompress" hobbies have picked up in a big way. Since the middle of June, I've burned through:

- Mario Rabbids for the Switch: Weird and fantastic
- All 100-something Marvel Civil War comics and many others: Turns out comics are pretty cool. Who knew?
- Bloodborne on the PS4: It took three, multiple-month quits before I finally got gud.
- A good deal of skin: I've still got signs of the sunburn I got beginning of the month, lol

And last, but not least, my good friend Will recommended that I check out Daniel Kahneman's *Thinking Fast and Slow*. We've compared notes over the past few years on all things mental health, imposter syndrome, and Internet garbage. He was instrumental in helping me get a standup routine together that seemed to go over well-enough, and we're often thinking on the same wavelength. So when he made a book recommendation, I was certain that it would be a quality one.

Nevertheless, I didn't even make it through the introduction before I found myself itching to do some tinkering over a couple sentences that I read, lol

## The Question

The book itself explores thinking and decision making-- establishing some simple constructions that help you conceptualize the way your brain works. It also provides insight into how that may occasionally work against us in the form of biases, and *for* us via *heuristics* (or roughly, rules of thumb).

And so while explaining the *availability heuristic*, or our tendency to form opinions based on the examples we can easily summon, he says the following:

> Consider the letter *K*.
>
> Is *K* more likely more likely to appear as the first letter in a word OR as the third letter?

And I stopped and went through the mental exercise.

    cake, lick, kangaroo, clock, acknowledge, knowledge, know, knack, kick, ...
    
It *seemed* about even, but I was very aware that for every first-letter-k I was coming up with, I was deliberately suppressing another one while I thought even harder for a third-letter-k, in some clumsy balancing strategy. Then all of a sudden, I was in my head about it, and the reflexive, "ease of access" point he was trying to impart was wasted on me.

Be that as it may, what was the answer?

### My Approach

Basically, the mental-model I was starting to think up looked like the following:

I was going to have a big old list of every letter, where each letter had its own corresponding (empty at first) list.


```python
letters = make_letter_dict()
print(letters)
```

    {'a': {}, 'b': {}, 'c': {}, 'd': {}, 'e': {}, 'f': {}, 'g': {}, 'h': {}, 'i': {}, 'j': {}, 'k': {}, 'l': {}, 'm': {}, 'n': {}, 'o': {}, 'p': {}, 'q': {}, 'r': {}, 's': {}, 't': {}, 'u': {}, 'v': {}, 'w': {}, 'x': {}, 'y': {}, 'z': {}}
    

And I'd be able to take a word, and see where each letter fell (first, second, etc)


```python
for idx, letter in enumerate('kickback'):
    print(idx, letter)
```

    0 k
    1 i
    2 c
    3 k
    4 b
    5 a
    6 c
    7 k
    

Then I'd be able to populate those sub-lists, per letter, with a count of where letters have occurred.

For example, here, `k` occurs once in the `0th`, `3rd`, and `7th` places.


```python
print(get_letter_dists(['kickback'])['k'])
```

    {0: 1, 3: 1, 7: 1}
    

And so as I layered in more words, I'd be able to get a running total of counts, per letter, of where they appeared in my list of words.


```python
print(get_letter_dists(['kickback', 'knock', 'knuckle'])['k'])
```

    {0: 3, 3: 1, 7: 1, 4: 2}
    

But to extend this idea to the point where I can make real inference, I was going to need a ridiculous amount of data.

### A Ridiculous Amount of Data

So I found myself borrowing from the `popular.txt` by [GitHub user Dolph](https://github.com/dolph/dictionary#populartxt), which is a combination of the very-famous [Enable 1](http://www.bananagrammer.com/2013/12/the-amazing-enable-word-list-project.html) dataset, cross-referenced against Wiktionary's word frequency lists generated from a comprehensive look at scripts from English-speaking TV shows and movies.


```python
words = load_all_words()
```

It's over 25,000 words long.


```python
len(words)
```




    25322



It includes words spoken by the everyman, you and me.


```python
print('dog' in words)
print('beer' in words)
print('data' in words)
print('science' in words)
```

    True
    True
    True
    True
    

But doesn't include $2 words of high-society.


```python
print('tophat' in words)
print('wainscoting' in words)
print('bourgeoisie' in words)
print('universalhealthcare' in words)
```

    False
    False
    False
    False
    

As well as just about all of the good swear words (left as an exercise to the reader).

## Running It

I ran the same "letters by count in words" across this whole dataset, this time, opting to store it in a more-easily-readible tabular format.


```python
df = get_letter_dists(words, asFrame=True)
df
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>a</th>
      <th>b</th>
      <th>c</th>
      <th>d</th>
      <th>e</th>
      <th>f</th>
      <th>g</th>
      <th>h</th>
      <th>i</th>
      <th>j</th>
      <th>...</th>
      <th>q</th>
      <th>r</th>
      <th>s</th>
      <th>t</th>
      <th>u</th>
      <th>v</th>
      <th>w</th>
      <th>x</th>
      <th>y</th>
      <th>z</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1405.0</td>
      <td>1566.0</td>
      <td>2533.0</td>
      <td>1595.0</td>
      <td>988.0</td>
      <td>1198.0</td>
      <td>825.0</td>
      <td>1036.0</td>
      <td>915.0</td>
      <td>250.0</td>
      <td>...</td>
      <td>92.0</td>
      <td>1442.0</td>
      <td>3135.0</td>
      <td>1323.0</td>
      <td>499.0</td>
      <td>377.0</td>
      <td>728.0</td>
      <td>1.0</td>
      <td>98.0</td>
      <td>44.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3554.0</td>
      <td>150.0</td>
      <td>438.0</td>
      <td>202.0</td>
      <td>3739.0</td>
      <td>91.0</td>
      <td>83.0</td>
      <td>1040.0</td>
      <td>2577.0</td>
      <td>4.0</td>
      <td>...</td>
      <td>64.0</td>
      <td>2227.0</td>
      <td>220.0</td>
      <td>624.0</td>
      <td>1914.0</td>
      <td>182.0</td>
      <td>208.0</td>
      <td>282.0</td>
      <td>238.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2368.0</td>
      <td>518.0</td>
      <td>1223.0</td>
      <td>793.0</td>
      <td>1784.0</td>
      <td>460.0</td>
      <td>703.0</td>
      <td>205.0</td>
      <td>1618.0</td>
      <td>70.0</td>
      <td>...</td>
      <td>51.0</td>
      <td>2364.0</td>
      <td>1737.0</td>
      <td>1645.0</td>
      <td>1006.0</td>
      <td>469.0</td>
      <td>257.0</td>
      <td>127.0</td>
      <td>259.0</td>
      <td>93.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1506.0</td>
      <td>442.0</td>
      <td>1139.0</td>
      <td>1007.0</td>
      <td>3003.0</td>
      <td>429.0</td>
      <td>776.0</td>
      <td>558.0</td>
      <td>1937.0</td>
      <td>39.0</td>
      <td>...</td>
      <td>46.0</td>
      <td>1618.0</td>
      <td>1473.0</td>
      <td>2138.0</td>
      <td>762.0</td>
      <td>338.0</td>
      <td>258.0</td>
      <td>32.0</td>
      <td>192.0</td>
      <td>112.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1371.0</td>
      <td>317.0</td>
      <td>729.0</td>
      <td>702.0</td>
      <td>3565.0</td>
      <td>206.0</td>
      <td>477.0</td>
      <td>699.0</td>
      <td>2296.0</td>
      <td>7.0</td>
      <td>...</td>
      <td>15.0</td>
      <td>1708.0</td>
      <td>1706.0</td>
      <td>1611.0</td>
      <td>705.0</td>
      <td>158.0</td>
      <td>147.0</td>
      <td>22.0</td>
      <td>498.0</td>
      <td>65.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>1285.0</td>
      <td>207.0</td>
      <td>640.0</td>
      <td>956.0</td>
      <td>2761.0</td>
      <td>212.0</td>
      <td>477.0</td>
      <td>419.0</td>
      <td>1976.0</td>
      <td>3.0</td>
      <td>...</td>
      <td>18.0</td>
      <td>1725.0</td>
      <td>1660.0</td>
      <td>1484.0</td>
      <td>433.0</td>
      <td>200.0</td>
      <td>147.0</td>
      <td>23.0</td>
      <td>474.0</td>
      <td>31.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>1112.0</td>
      <td>117.0</td>
      <td>428.0</td>
      <td>813.0</td>
      <td>2081.0</td>
      <td>69.0</td>
      <td>762.0</td>
      <td>207.0</td>
      <td>1545.0</td>
      <td>3.0</td>
      <td>...</td>
      <td>3.0</td>
      <td>1065.0</td>
      <td>1613.0</td>
      <td>1440.0</td>
      <td>335.0</td>
      <td>82.0</td>
      <td>45.0</td>
      <td>22.0</td>
      <td>340.0</td>
      <td>53.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>604.0</td>
      <td>85.0</td>
      <td>331.0</td>
      <td>656.0</td>
      <td>1514.0</td>
      <td>44.0</td>
      <td>713.0</td>
      <td>137.0</td>
      <td>1067.0</td>
      <td>2.0</td>
      <td>...</td>
      <td>1.0</td>
      <td>641.0</td>
      <td>1188.0</td>
      <td>995.0</td>
      <td>197.0</td>
      <td>79.0</td>
      <td>43.0</td>
      <td>6.0</td>
      <td>261.0</td>
      <td>57.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>379.0</td>
      <td>54.0</td>
      <td>178.0</td>
      <td>482.0</td>
      <td>1087.0</td>
      <td>18.0</td>
      <td>461.0</td>
      <td>89.0</td>
      <td>651.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>3.0</td>
      <td>339.0</td>
      <td>793.0</td>
      <td>638.0</td>
      <td>113.0</td>
      <td>63.0</td>
      <td>12.0</td>
      <td>3.0</td>
      <td>220.0</td>
      <td>32.0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>164.0</td>
      <td>31.0</td>
      <td>112.0</td>
      <td>290.0</td>
      <td>595.0</td>
      <td>6.0</td>
      <td>306.0</td>
      <td>68.0</td>
      <td>344.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>188.0</td>
      <td>493.0</td>
      <td>414.0</td>
      <td>52.0</td>
      <td>34.0</td>
      <td>1.0</td>
      <td>3.0</td>
      <td>190.0</td>
      <td>19.0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>105.0</td>
      <td>14.0</td>
      <td>54.0</td>
      <td>141.0</td>
      <td>343.0</td>
      <td>2.0</td>
      <td>167.0</td>
      <td>16.0</td>
      <td>177.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>104.0</td>
      <td>303.0</td>
      <td>196.0</td>
      <td>17.0</td>
      <td>12.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>124.0</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>46.0</td>
      <td>11.0</td>
      <td>26.0</td>
      <td>76.0</td>
      <td>130.0</td>
      <td>1.0</td>
      <td>90.0</td>
      <td>7.0</td>
      <td>73.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>48.0</td>
      <td>181.0</td>
      <td>70.0</td>
      <td>13.0</td>
      <td>8.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>90.0</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>12</th>
      <td>16.0</td>
      <td>1.0</td>
      <td>12.0</td>
      <td>24.0</td>
      <td>54.0</td>
      <td>0.0</td>
      <td>46.0</td>
      <td>1.0</td>
      <td>21.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>18.0</td>
      <td>84.0</td>
      <td>31.0</td>
      <td>1.0</td>
      <td>4.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>43.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>13</th>
      <td>6.0</td>
      <td>1.0</td>
      <td>3.0</td>
      <td>5.0</td>
      <td>23.0</td>
      <td>0.0</td>
      <td>9.0</td>
      <td>0.0</td>
      <td>13.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>39.0</td>
      <td>19.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>28.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>14</th>
      <td>4.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>3.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>5.0</td>
      <td>0.0</td>
      <td>5.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>17.0</td>
      <td>6.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>8.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>15</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>3.0</td>
      <td>0.0</td>
      <td>4.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>3.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>16</th>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>17</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>18</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>19</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
<p>20 rows × 26 columns</p>
</div>



Idea to execution, procuring and wrangling this dataset was actually much easier than I'd originally thought.

The real fun was trying to figure out compelling visualizations.

## Visualizing It

Admittedly, my `matplotlib` chops have always been "good enough to get the job done" but have always taken a back seat to some of the meatier Python topics. (And we're not going to talk about the D3 book collecting dust on my book shelf :( )

I had a lot of thoughts about what some nice visualizations might look like, doodling and shopping ideas from friends who are better at this stuff than me (Here's where I'd love to link the blog you should write. You know who you are!). But as I started hurling spaghetti code at my interpreter, it soon became clear that I'd be doing myself a lot of favors if I started peeling back the curtain on `matplotlib` a little bit. It wound up being a good an excuse as any to start padding out the [Data Viz section of my notes](https://napsterinblue.github.io/notes/#python)-- explaining things I've probably Googled dozens of times. 

Ultimately, I had a lot of fun deciding what a visualization was **going** to look like, then figuring out how to leverage the expressive API to make that happen.

Here are some of my favorites:

### The Meat of the Post

First, I tried taking a look at how these counts measured up, per letter, *as a percentage of that letter's overall counts*. It's clear here that `k` shows up as the `4th` far more than the first or third spot (sorry, folks not used to 0-indexing!).

I wound up leveraging the `seaborn` library to organize the plot, and in so doing stumbled across a [fascinating talk on how the devs picked this color gradient](https://www.youtube.com/watch?v=xAoljeRJ3lU).


```python
letter_dist_heatmap(df)
```


![png](Writeup_files/Writeup_34_0.png)


But this was almost too close to tell, depending on how well you can interpret differences in hue.

Instead, I went with a more traditional approach and did a bunch of bar charts, and it helps you get a better idea of the how the letters are distributed. `k` still looks pretty close.


```python
plot_letter_dists(df)
```


![png](Writeup_files/Writeup_36_0.png)


But a closer inspection of the `k` chart reveals that the first letter does, indeed, occur more often than the third.


```python
plot_just_k(df)
```


![png](Writeup_files/Writeup_38_0.png)


Look out for my unofficial sequel, *Thinking Fast and then Tinkering at Your Computer for a Couple Nights*

## Bonus Scrabble Round

Before I closed the lid on my tinkering, I was struck by some of the distributions of the letters that I'd found. `j` was overwhelmingly the first letter. `o` and `u` the second. Many others followed an almost-normal distribution.

So I did what you'd expect of any data scientist who'd gotten destroyed in Scrabble the night before, and I reworked the visualization to also include point values of each letter. Study your losses, right?


```python
plot_letter_dists_scrabble(df)
```


![png](Writeup_files/Writeup_42_0.png)


I thought it was interesting to see that vowels earn their one-point-edness and by having a pretty wide distribution, making them flexible tiles. But you might also notice that all of the two and three point consonants share a pretty handy availability as more-often the first letter in a word, making it much easier to play onto an uncrowded board. Conversely, you'll have to scratch your head a bit to make a quality play with `z`.

Alternatively, you might also just look at how prevalent these letters were across our text and find a much simpler interpretation.


```python
plot_letter_volume_scrabble(df)
```


![png](Writeup_files/Writeup_44_0.png)


## Conclusion

Thanks for reading! Per usual, the code I used to generate all of the above [can be found here](https://github.com/NapsterInBlue/LetterDistributions). I'm gonna go get back to that book.

Cheers,

-Nick
