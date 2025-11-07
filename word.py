import re
import os
import sys

word_of_day = input("\nEnter Wordle Answer: ")
if len(word_of_day) != 5 or not bool(re.match('^[abcdefghijklmnopqrstuvwxyz]+$', word_of_day)):
    print("Invalid word input")
    os.execl(sys.executable, sys.executable, *sys.argv)

print("\nPut 'cancel' at any input to quit the program.")

def check(char_type, char_id, candidate_word, word_of_day):
    if char_type == "#":
        # Yellow: letter is in word_of_day but NOT at this position
        return candidate_word[char_id] in word_of_day and candidate_word[char_id] != word_of_day[char_id]
    else:
        # Grey: letter is NOT in word_of_day
        return candidate_word[char_id] not in word_of_day

while True:
    while True:
        art = input("Enter Line here (# for yellow, _ for a grey space): ")
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

        with open("words.txt", "r") as f:
            words = [word.strip().lower() for word in f if len(word.strip()) == 5 and word.strip().isalpha()]

        valid_words = []
        for candidate_word in words:
            if len(set(candidate_word)) != 5:
                continue
            passes = 0
            for i in range(5):
                if check(art[i], i, candidate_word, word_of_day):
                    passes += 1
            if passes == 5:
                valid_words.append(candidate_word)
        print("Matching words (sample):", valid_words[:int(max_words)])
        print("Total found:", len(valid_words))
