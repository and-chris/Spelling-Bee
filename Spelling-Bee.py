# CS1210: HW1
######################################################################
# Complete the signed() function, certifying that:
#  1) the code below is entirely your own work, and
#  2) it has not been shared with anyone outside the intructional team.
#
def signed():
    return(["awchristopher"])

######################################################################
# In this homework, you will be implementing a spelling bee game,
# inspired by the that appears in the New York Times. The purpose of
# the game is to find as many possible words from a display of 7
# letters, where each word must meet the following criteria:
#   1. it must consist of four or more letters; and
#   2. it must contain the central letter of the display.
# So, for example, if the display looks like:
#    T Y
#   B I L
#    M A
# where I is the "central letter," the words "limit" and "tail" are
# legal, but "balmy," "bit," and "iltbma" are not.
#
# We'll approach the construction of our system is a step-by-step
# fashion; for this homework, I'll provide specs and function
# signatures to help you get started. If you stick to these specs and
# signatures, you should soon have a working system.
#
# First, we'll need a few functions from the random module. Read up on
# these at docs.python.org.
from random import choice, randint, sample

######################################################################
# fingerprint(W) takes a word, W, and returns a fingerprint of W
# consisting of an ordered set of the unique character constituents of
# the word. You have already encountered fingerprint(W) so I will
# provide the reference solution here for you to use elsewhere.
def fingerprint(W):
    return(''.join(sorted(set(W))))

######################################################################
# score(W) takes a word, W, and returns how many points the word is
# worth. The scoring rules here are straightforward:
#   1. four letter words are worth 1 point;
#   2. each additional letter adds 1 point up to a max of 9; and
#   3. pangrams (use all 7 letters in display) are worth 10 points.
# So, for example:
#      A L
#     O B Y
#      N E
#   >>> score('ball')
#   1
#   >>> score('balloon')
#   4
#   >>> score('baloney')
#   10     # Pangram!
#
def score(W):
    points=0
    if len(W) == 4:  
        return(1)
    elif len(W) > 4 and len(fingerprint(W)) != 7:  #Enter this loop when the word has more than 4 letters and the fingerprint does not have 7 letters
        points = 1
        for i in W[4:]:  # Iterates through all the letters in the word after the 4th letter
            if points != 9:
                points=points + 1
    elif len(fingerprint(W)) == 7: # Enters this loop and gives ten points if the word is a pangram
        return(10)
    else:
        return(0)
    return points
######################################################################
# jumble(S, i) takes a string, S, having exactly 7 characters and an
# integer index i where 0<=i<len(S). The string describes a puzzle,
# while i represents the index of S corresponding to the "central"
# character in the puzzle. This function doesn't return anything, but
# rather prints out a randomized representation of the puzzle, with
# S[i] at the center and the remaining characters randomly arrayed
# around S[i]. So, for example:
#    >>> jumble('abelnoy', 1)
#     A L
#    O B Y
#     N E
#    >>> jumble('abelnoy', 1)
#     N Y
#    L B A
#     E O
#
def jumble(S, i):
    jumbled= ""
    newS = S[:i] + S[i+1:] #Makes a new list without the ith element
    while newS:             #Loops as long as newS has elements in it. Loop picks a random letter and adds it to the jumbled string, then sets newS equal to newS from that letter on.
        position = randint(0, len(newS)-1) #Picks a random index position
        jumbled += newS[position]  #Indexes the random index position and adds it to the string jumbled           
        newS = newS[:position] + newS[(position + 1):] #Changes newS to everything in newS without the indexed position
    print(" ", jumbled.upper()[0], " ", jumbled.upper()[1])
    print(jumbled.upper()[2], " ", S.upper()[i], " ", jumbled.upper()[3])
    print(" ", jumbled.upper()[4], " ", jumbled.upper()[5])
    return ""
######################################################################
# readwords(filename) takes the name of a file containing a dictionary
# of English words and returns two values, a dictionary of legal words
# (those having 4 or more characters and fingerprints of 7 of fewer
# characters), with fingerprints as keys and values consisting of sets
# of words with that fingerprint, as well as a list, consisting of all
# of the unique keys of the dictionary having exactly 7 characters (in
# no particular order).
#
# Your function should provide some user feedback. So, for example:
#    >>> D,S=readwords('words.txt')
#    113809 words read: 82625 usable; 33830 unique fingerprints.
#    >>> len(S)
#    13333
#    >>> S[0]
#    'abemort'
#    >>> D[S[0]]
#    {'barometer', 'bromate'}
#
def readwords(filename):
    wordstxt = open(filename, 'r')
    newList = [ ]
    for line in wordstxt:
        newList.append(line.strip())
    usable = [y for y in newList if len(fingerprint(y)) <= 7 and len(y) >= 4]    #Makes a list of all the usable words 
    uniqueFing = set([fingerprint(z) for z in usable])    #Makes a set of all the unique fingerprints in the usable words
    network = {key:set([]) for key in uniqueFing}    #Makes a dictionary with the unique fingerprints as keys
    sevenList = [x for x in uniqueFing if len(x) == 7]    #Makes a list of all the keys in the dictionary that has 7 letters
    for i in range(len(usable)):    #Iterates through all the index positions of the usable words and appends them to the dictionary in the correct spot
        network[fingerprint(usable[i])].add(usable[i])
    wordstxt.close()
    print(len(newList), "words read:", len(usable), "usable:", len(uniqueFing), "unique fingerprints")
    return(network, sevenList)
readwords('words.txt')
######################################################################
# round(D, S) takes two arguments, corresponding to the values
# returned by readwords(), randomly selects a puzzle seed from the
# list S and a central letter from within S. It then shows the puzzle
# and enters a loop where the user can:
#    1. enter a new word for scoring;
#    2. enter / to rescramble and reprint the puzzle;
#    3. enter + for a new puzzle; or
#    4. enter . to end the game.
# When a word is entered, it is checked for length (must be longer
# than 4 characters and its fingerprint must be contained within the
# puzzle seed). The word is then checked against D, and if found, is
# scored and added to the list of words.
#
# Here is a sample interactive transcript of round() in action:
#    >>> D,S = readwords('words.txt')
#    >>> round(D,S)
#     R F
#    E S I
#     H T
#    Input words, or: '/'=scramble; ':'=show; '+'=new puzzle; '.'=quit
#    sb> this
#    Bravo! +1
#    sb> these
#    Bravo! +2
#    sb> :
#    2 words found so far:
#      these
#      this
#    sb> there
#    Word must include 's'
#    sb> /
#     H E
#    T S F
#     R I
#    sb> +
#    You found 2 of 392 possible words: you scored 3 points.
#     U H
#    G A Q
#     O S
#    Input words, or: '/'=scramble; ':'=show; '+'=new puzzle; '.'=quit
#    sb> .
#    You found 0 of 46 possible words: you scored 0 points.
#    True
#
def round(D, S):
    print("This is the spelling bee. Construct as make words as you can from the puzzle!")
    print("Words must be at least 4 characters long and must include the center character. Have fun!")
    #initialization of variables
    randoNum = randint(1,5) #Random index position for the center element of the seed word
    randomWord = S[randint(0,len(S))] #Random word from the list of keys of the dictionary that have 7 letters
    usedWords = [] #List of used words
    posswords = [] #List of possible words
    totalScore = 0 #Keeps track of score
    newList = []
    jumble(randomWord, randoNum)
    print("Input words, or: '/'=scramble; ':'=show; '+'=new puzzle; '.'=quit")
    userI = ''
    randomInt = randint(1,5)
    n = 0
    numRight = 0
    #Iterates through every key in the dictionary, then compares every letter in the keys of the dictionary 
    #to the fingerprint of the puzzle seed word, if every letter is in the seed word, add the key to the list
    for z in D.keys():#
        countq=0
        for q in z:#
            if q in fingerprint(randomWord):
                countq +=1
            if countq == len(z) and randomWord[randoNum] in z:
                posswords.append(D[z])
    posswords = [val for sets in posswords for val in sets]
    #Loops through this while n=0, n does not change so it continuously loops. The loop ends when it returns false(parameter in play())
    while n == 0:
        userI = input()
        if userI == '/':
            jumble(randomWord, randoNum)
            print("Input words, or: '/'=scramble; ':'=show; '+'=new puzzle; '.'=quit")
        elif userI == '.':
            print("Total score:", totalScore)
            print("You found", numRight, "out of", len(posswords), "possible words!")
            return False
        elif userI == ':':
            print("Words found so far:")
            for i in usedWords:
                print(i)
        elif userI == '+':
            return True
        elif fingerprint(userI) not in D.keys():
            print("Choose another word!")
        #Checks if the user input word is in the dictionary and has not previously been used
        elif userI in posswords and userI not in usedWords:
            if randomWord[randoNum] in userI:
                print("Nice job! +", score(userI))
                usedWords.append(userI)
                totalScore = totalScore + score(userI)
                numRight += 1
            elif randomWord[randoNum] not in userI:   #Checks if the center character is not in the user input word
                print('Incorrect. Word needs to include:', randomWord[randoNum])
        elif userI not in D[fingerprint(userI)]:  #Checks if the user input word is not in the dictionary
            print("Pick another word!")
        elif userI in usedWords:  #Checks if the user input word has already been used
            print("That word has already been used. Pick another word!")
    return False

######################################################################
# play(filename='words.txt') takes a single optional argument filename
# (defaults to 'words.txt') that gives the name of the file containing
# the dictionary of legal words. After invoking readwords(), it
# repeatedly invokes rounds() until it obtains a False, indicating the
# game is over.
#
def play(filename='words.txt'):
    print('File name of the dictionary of legal words: ', str(filename))
    D,S=readwords(filename)
    while round(D,S) == True: #Repeatedly invokes round() unless round() returns false, which ends the game
        pass
    else:
        return 'The End.'
    
