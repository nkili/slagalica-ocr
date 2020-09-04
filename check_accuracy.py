import sys
import os
import re

from colorama import Fore, Back, Style
from collections import defaultdict

# Print guesses
PRINT_GUESSES = False
# Print correct guesses if PRINT_GUESSES is set to True
PRINT_CORRECT_GUESSES = False
# Print skipped guesses if PRINT_GUESSES is set to True
PRINT_SKIPPED_GUESSES = True
# Print wrong guesses if PRINT_GUESSES is set to True
PRINT_WRONG_GUESSES = True
# Print distribution of wrongs per field
PRINT_WRONGS_PER_FIELD = False
# Print stats for correct, skipped and wrong guesses for every file
PRINT_PER_FILE_STATS = False
# Print which guess files didn't have a correct file counterpart
PRINT_SKIPPED_FILES = True

wrongs_per_field = defaultdict(lambda: 0)

def check_line(predicted, correct):
    if predicted == correct:
        return (1, 0, 0)
    predicted = predicted.replace("?", r"\?")
    predicted_regex = re.compile(predicted.replace(".", ".+"))
    if predicted_regex.fullmatch(correct):
        return (0, 1, 0)
    else:
        return (0, 0, 1)

def check(predicted, solution):
    if type(predicted) == str:
        predicted = predicted.splitlines()
    if type(solution) == str:
        solution = solution.splitlines()
    for ind, line in enumerate(predicted):
        if line[:2] == "А1":
            predicted = [x.strip() for x in predicted[ind:] if x.strip() != ""]
            break
    for ind, line in enumerate(solution):
        if line[:2] == "А1":
            solution = [x.strip() for x in solution[ind:] if x.strip() != ""]
            break
    
    (correct_guesses, skipped_guesses, wrong_guesses) = (0, 0, 0)

    for predicted_line, solution_line in zip(predicted, solution):
        result = check_line(predicted_line, solution_line)
        correct_guesses += result[0]
        skipped_guesses += result[1]
        wrong_guesses += result[2]
        if (result[2] == 1):
            if (solution_line[:2] == "??aБ3"):
                print(predicted_line)
            wrongs_per_field[solution_line[:2]] += 1
        if (PRINT_GUESSES):
            if (result[0] == 1):
                if (PRINT_CORRECT_GUESSES):
                    print(Fore.GREEN + predicted_line + Style.RESET_ALL)
                    print(solution_line)
            elif (result[1] == 1):
                if (PRINT_SKIPPED_GUESSES):
                    print(Fore.YELLOW + predicted_line + Style.RESET_ALL)
                    print(solution_line)
            elif (result[2] == 1):
                if (PRINT_WRONG_GUESSES):
                    print(Fore.RED + predicted_line + Style.RESET_ALL)
                    print(solution_line)
    return correct_guesses, skipped_guesses, wrong_guesses

def check_files(prediction_file, solution_file):
    with open(prediction_file) as f:
        predicted = f.read()
    with open(solution_file) as f:
        solution = f.read()
    return check(predicted, solution)

if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print ("Usage: python check_accuracy.py PREDICTION_DIR SOLUTION_DIR")
        exit()
    prediction_dir = sys.argv[1]
    solution_dir = sys.argv[2]
    prediction_files = sorted(os.listdir(prediction_dir))
    solution_files = os.listdir(solution_dir)
    checked_files = 0
    skipped_files = []
    solution_line, skipped, wrong = (0, 0, 0)
    completely_correct, completely_wrong = (0, 0)
    for prediction_file in prediction_files:
        if prediction_file[-4:] != ".txt":
            continue
        if prediction_file not in solution_files:
            skipped_files += [prediction_file,]
        else:
            checked_files += 1
            result = check_files(os.path.join(prediction_dir, prediction_file), os.path.join(solution_dir, prediction_file))
            if (PRINT_PER_FILE_STATS): print(prediction_file, result)
            if result[0] == 0: completely_wrong += 1
            if result[2] == 0: completely_correct += 1
            solution_line += result[0]
            skipped += result[1]
            wrong += result[2]
    if (PRINT_GUESSES or PRINT_PER_FILE_STATS): print()
    print(f"Num of files checked: {checked_files}")
    if (PRINT_SKIPPED_FILES):
        print(f"Skipped files: {len(skipped_files)}")
        for skipped_file in skipped_files:
            print(" ", Fore.MAGENTA, skipped_file, Style.RESET_ALL)
    print(f"Completely correct files: {completely_correct}, Completely wrong files: {completely_wrong}")
    print(f"Correct: {solution_line}, Skipped: {skipped}, Wrong: {wrong}")
    print(f"Accuracy: {round(100*(solution_line+skipped)/(solution_line+skipped+wrong),4)}%")
    if (PRINT_WRONGS_PER_FIELD):
        print("Distribution of wrongs per field:")
        print(sorted(wrongs_per_field.items(), key= lambda x: x[0]))
