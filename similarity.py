
def get_dataset(composer: str, with_inversions=False) -> str:
    '''
    Returns the content of the txt file for the composer's repertoire

    Parameters
    ----------
    composer : str
        The composer which has been encoded
    with_inversion : bool, optional
        Whether to fetch the dataset with or without inversions
        (default is False for no inversions)

    Returns
    -------
    str
        A comma-separated string encoding the composer's repertoire
    '''

    file_location = "datasets/{}-dataset-{}.txt".format(
        "inv" if with_inversions else "simple",
        composer)
    try:
        return open(file_location, "r").read()
    except FileNotFoundError:
        raise NotImplementedError("The composer you've entered is not in the database.")

def build_n_sequence_dictionary(n : int, txt : str) -> dict:
    """
    Returns a dict counting appearances of n-long progressions

    Parameters
    ----------
    n : int
        The length of progressions to count
    txt : str
        A comma-separated string of roman numerals

    Returns
    -------
    dict
        Maps sequences in txt of length n to the number of times
        they appear in txt
    """
    seq_dict = dict()

    pieces = txt.split('\n')
    # For every song in the string, which are separated by '\n'
    for piece in pieces:
        roman_numerals = piece.split(',')
        # For every sequence of n roman numerals
        for i in range(len(roman_numerals) - n):
            seq = tuple(roman_numerals[i:i+n])
            # Increment the count for this specific sequence
            seq_dict[seq] = seq_dict.get(seq, 0) + 1
    return seq_dict

def progression_kernel(prog: str, composer: str, with_inversions=False, look_back=2, verbose=False):
    '''
    Returns a list of frequencies of subsets of the progression of fixed length

        Given a progression as a comma-separated string of chords (followed by
    parentheses with the inversion number if the parameter with_inversions=True),
    a composer's last name, and the number of chords to serve as the context of
    the kernel, we apply the sliding kernel to determine the likelihood that the
    composer follows a sequence of chords with the same chord in the given
    progression.
        If verbose is true, prints the information in readable format to the
    console in addition to returning the list of frequencies.

    Parameters
    ----------
    prog : str
        a chord progression formatted as roman numerals separated by commas
    composer : str
        the last name of the composer to reference
    with_inversions : bool, optional
        False for no inversions, True for inversions (default False)
    look_back : int, optional
        (At least 1) The number of chords to serve as the context (default 2)
    verbose : bool, optional
        True to print the information in readable format (default False)

    Returns
    -------
    float[]
        A list of the frequencies for each application of the kernel
    '''
    percentages = []

    # removes any whitespace
    prog = prog.replace(' ', '')

    txt = get_dataset(composer, with_inversions)

    # creates the dictionary given the progression
    prog_list = tuple(prog.split(','))

    if verbose:
        print("Analyzing progression: [{}]".format(prog))

    look_back_dict = build_n_sequence_dictionary(look_back, txt)

    seq_dict = build_n_sequence_dictionary(look_back + 1, txt)

    # For every look_back + 1 sequence in the progression
    for i in range(len(prog_list)-look_back):

        # Total Occurances of look_back
        look_back_occurances = look_back_dict.get((prog_list[i:i+look_back]),0)
        # Num Occurances look back is followed by the next chord
        look_back_with_next_chord = seq_dict.get(prog_list[i:i+look_back+1], 0)

        # Calculate the frequency that a chord follows the n previous
        if look_back_occurances == 0:
            prog_percent = 0
        else:
            prog_percent = look_back_with_next_chord / look_back_occurances

        percentages.append(prog_percent)

        if verbose:
            print("{} follows [{}] with [{}] {:.2f}% of the time".format(
                composer,
                ",".join(prog_list[i:i+look_back]),
                prog_list[i+look_back],
                prog_percent * 100))

    return percentages

def request_composer ():
    """Requests and returns the user's desired composer"""
    # Get the composer from the user
    composer = input("Composer ([monteverdi]/bach): ").lower()
    if len(composer) == 0:
        composer = "monteverdi"
    return composer


if __name__ == "__main__":

    # Get the composer from the user
    valid_composers = ['monteverdi','bach']
    composer = request_composer()
    while composer not in valid_composers:
        composer = request_composer()

    # Get the inversion from the user
    with_inversions = "y" in input ("Use Inversions (y/[n]): ").lower()

    # Length of Context for the Kernel
    context = input ("Size of desired context ([2]): ")
    if len(context) == 0:
        context = '2'
    context = int(context)

    # Get the chord progression from the user
    print("The progression is a comma-separated string of chords.")
    print("  Ex, I,V,I,iv")
    if with_inversions:
        print ("To define inversions, follow each roman numeral with parenthesis.")
        print ("  Ex, V(0) is V in root position, V(1) is first inversion, etc")
    progression = input("Your Chord Progression: ")
    print("")

    res = progression_kernel(progression, composer, with_inversions, context, verbose=True)

    print("\nThe following are places in your progression which are particularly unlikely:")

    split_progression = progression.split(",")

    for i in range(len(res)):
        frequency = res[i]

        if frequency < 0.05:
            bad_prog = ",".join(split_progression[i:i+context+1])
            print ("  Consider looking at the progression: [{}]".format(bad_prog))
            print ("    {} doesn't follow [{}] with [{}] very often."
                .format(composer, ",".join(split_progression[i:i+context]), split_progression[i+context]))
