import re
import os
import sys

word_of_day = input("\nEnter Wordle Answer: ")
if len(word_of_day) != 5 or not bool(re.match('^[abcdefghijklmnopqrstuvwxyz]+$', word_of_day)):
    print("Invalid word input")
    os.execl(sys.executable, sys.executable, *sys.argv)

print("\nPut 'cancel' at any input to quit the program.")
word = []
word_letters = []
def check(char_type, char_id):
    if char_type == "#":
        if word[char_id] in word_letters:
            return True
        else:
            return False
    else:
        if word[char_id] not in word_letters:
            return True
        else:
            return False
    
while True:
    while True:
        art = input("Enter Line here (# for green/yellow, _ for a grey space): ")
        if art == "cancel":
            quit()
        if len(art) != 5 or not bool(re.match('^[#_]+$', art)):
            print("Invalid line input")
            break

        max_words = input("Maximum Amount of Words Given: ")
        if max_words == "cancel":
            quit()
        if not bool(re.match('^[0123456789]+$', max_words)):
            print("Invalid max input")
            break

        word_letters = set(word_of_day)
        non_word_letters = set("abcdefghijklmnopqrstuvwxyz") - word_letters

        valid_words = []

        with open("words.txt", "r") as f:
            words = [word.strip().lower() for word in f if len(word.strip()) == 5 and word.strip().isalpha()]

        for word in words:
            if len(set(word)) != 5:
                continue

            first = word[0] in word_letters
            second = word[1] in word_letters
            third = word[2] in word_letters
            fourth = word[3] in word_letters
            fifth = word[4] in word_letters

            passes = 0
            for i in range(5):
                if check(art[i], i):
                    passes += 1
            if passes == 5:
                valid_words.append(word)
                
        print("Matching words (sample):", valid_words[:int(max_words)])
        print("Total found:", len(valid_words))
        