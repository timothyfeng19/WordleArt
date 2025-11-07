import sys
from collections import Counter, defaultdict


def get_word_list(filename="words.txt"):
    """
    Loads a list of 5-letter words from a text file.
    Each word should be on a new line.
    """
    try:
        with open(filename, 'r') as f:
            words = [line.strip().upper() for line in f]
            # Filter for 5-letter words just in case
            words = [word for word in words if len(word) == 5 and word.isalpha()]
        if not words:
            print(f"Error: Word list '{filename}' is empty or not found.")
            print("Please create this file and add 5-letter words to it.")
            sys.exit(1)
        return words
    except FileNotFoundError:
        print(f"Error: Word list file '{filename}' not found.")
        print("Please create this file in the same directory and add 5-letter words.")
        sys.exit(1)


def calculate_pattern(target, guess):
    """
    Calculates the Wordle color pattern for a guess against a target.
    G = Green, Y = Yellow, B = Black/Gray
    """
    pattern = ["B"] * 5
    target_counts = Counter(target)

    # 1. First pass: Find Greens (G)
    for i in range(5):
        if guess[i] == target[i]:
            pattern[i] = "G"
            target_counts[guess[i]] -= 1

    # 2. Second pass: Find Yellows (Y) and Blacks (B)
    for i in range(5):
        if pattern[i] == "G":
            continue
        if guess[i] in target_counts and target_counts[guess[i]] > 0:
            pattern[i] = "Y"
            target_counts[guess[i]] -= 1

    return "".join(pattern)


def hamming_distance(s1, s2):
    """Calculates the number of differing characters between two strings."""
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))


def build_pattern_map(target_word, word_list):
    """
    Pre-calculates all possible patterns for a target word.
    Returns a map: { "BGYBB": ["WORD1", "WORD2"], "GGGBB": ["WORD3"] }
    """
    pattern_map = defaultdict(list)
    for guess_word in word_list:
        pattern = calculate_pattern(target_word, guess_word)
        pattern_map[pattern].append(guess_word)
    return pattern_map


def find_guesses_for_art(target_word, art_patterns, word_list):
    """
    Finds guesses for art patterns and suggests alternatives if not found.
    """
    print(f"Pre-calculating all possible patterns for target: {target_word}...")
    # 1. Create the map of all possible patterns
    possible_patterns_map = build_pattern_map(target_word, word_list)
    print(f"Found {len(possible_patterns_map)} unique patterns.\n")

    results = []

    for requested_pattern in art_patterns:
        # 2. Check if the exact pattern exists
        if requested_pattern in possible_patterns_map:
            # Found it!
            guess = possible_patterns_map[requested_pattern][0]  # Get the first word
            results.append({
                "status": "found",
                "requested": requested_pattern,
                "guess": guess
            })
        else:
            # 3. Not found. Time to find alternatives.
            alternatives = {}
            # We search for patterns with a Hamming distance of 1 (off-by-one)
            for possible_pattern, guess_list in possible_patterns_map.items():
                if hamming_distance(requested_pattern, possible_pattern) == 1:
                    alternatives[possible_pattern] = guess_list[0]  # Get first word

            results.append({
                "status": "not_found",
                "requested": requested_pattern,
                "alternatives": alternatives  # This will be {} if none are found
            })

    return results


# --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# --- MAIN PART: CONFIGURE YOUR ART HERE ---
# --- --- --- --- --- --- --- --- --- --- --- --- --- ---

if __name__ == "__main__":
    # 1. GET YOUR WORD LIST
    ALL_WORDS = get_word_list("words.txt")

    # 2. SET YOUR TARGET WORD
    TARGET_WORD = "GUISE"

    # 3. DEFINE YOUR ART
    # B = Black, G = Green, Y = Yellow
    ART_TO_CREATE = [
        "YBYYY",  # Example: "CHILD"
        "YBYBB",  # Example: "MIGHT"
        "YYYYY",  # Example: "RIGHT"
        "BBYBY",  # Example: "CHILD"
        "YYYBY"
    ]

    # --- Run the solver ---
    final_guesses = find_guesses_for_art(TARGET_WORD, ART_TO_CREATE, ALL_WORDS)

    # --- Print the results ---
    print("--- 🎨 Your Wordle Art Plan ---")
    print(f"Target Word: {TARGET_WORD}\n")

    for result in final_guesses:
        if result["status"] == "found":
            print(f"✅ For pattern {result['requested']}, use guess: **{result['guess']}**")

        elif result["status"] == "not_found":
            print(f"❌ For pattern {result['requested']}, **NO GUESS FOUND**.")

            if result["alternatives"]:
                print("   **Did you mean one of these?** (off by 1 square)")
                for alt_pattern, alt_guess in result["alternatives"].items():
                    print(f"   - Pattern: {alt_pattern} (use guess: **{alt_guess}**)")
            else:
                print("   (No close alternatives were found either.)")

        print("---")  # Separator