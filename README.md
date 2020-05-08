# Music 21 Conventional Progressions

Our Final Project for MIT Computational Music Theory class (21M.383).

The idea of this project is to allow the user to be able to submit a chord progression. The algorithm will then in some way analyze how closely this chord progression resembles the music patterns of a particular composer.

# 1. Format Roman Numeral Datasets

The first Jupyter Notebook of interest is `List Generator.ipynb`. In this notebook, the goal is to format songs from several known composers into a text file which can be easily parsed and analyzed by the next python notebook.

In the end, the format that we chose to encode the songs into is to separate each song with new line characters `\n`. Within each song, the data for each chord is separated by commas.

# 2. Conduct Frequency Analysis

The second Jupyter Notebook of interest is `Chord Progression Frequency Analysis.ipynb`, where we actually conduct the frequency analysis.

This notebook contains a handful of helper functions and methods.

# Future Work

Currently, this project only works using the `rntxt` files that come natively with the music21 library: 46 songs by Monteverdi and 20 by Bach. Ideally, we would have many more datasets for each composer, and more composers to choose from.

Additionally, we would want to encode duration as well into the datasets and somehow encode the
