""" --- Part Two ---
Your analysis only confirmed what everyone feared: the two lists of location IDs are indeed very different.

Or are they?

The Historians can't agree on which group made the mistakes or how to read most of the Chief's handwriting, but in the commotion you notice an interesting detail: a lot of location IDs appear in both lists! Maybe the other numbers aren't location IDs at all but rather misinterpreted handwriting.

This time, you'll need to figure out exactly how often each number from the left list appears in the right list. Calculate a total similarity score by adding up each number in the left list after multiplying it by the number of times that number appears in the right list.

Here are the same example lists again:

3   4
4   3
2   5
1   3
3   9
3   3
For these example lists, here is the process of finding the similarity score:

The first number in the left list is 3. It appears in the right list three times, so the similarity score increases by 3 * 3 = 9.
The second number in the left list is 4. It appears in the right list once, so the similarity score increases by 4 * 1 = 4.
The third number in the left list is 2. It does not appear in the right list, so the similarity score does not increase (2 * 0 = 0).
The fourth number, 1, also does not appear in the right list.
The fifth number, 3, appears in the right list three times; the similarity score increases by 9.
The last number, 3, appears in the right list three times; the similarity score again increases by 9.
So, for these example lists, the similarity score at the end of this process is 31 (9 + 4 + 0 + 0 + 9 + 9).

Once again consider your left and right lists. What is their similarity score?"""

import bisect
from collections import Counter

def process_file(file_path):
    # Initialize sorted lists for the first and second numbers
    first_numbers = []
    second_numbers = []

    # Read the file line by line
    with open("day_01_input.txt", 'r') as file:
        for line in file:
            # Parse the two numbers in the line
            try:
                num1, num2 = map(int, line.split())
            except ValueError:
                print(f"Skipping invalid line: {line.strip()}")
                continue

            # Insert each number into the respective sorted list
            bisect.insort(first_numbers, num1)
            bisect.insort(second_numbers, num2)

    return first_numbers, second_numbers

def calculate_similarity_score(first_list, second_list):
    # Count occurrences of each number in the second list
    second_list_counts = Counter(second_list)

    # Calculate the similarity score
    similarity_score = 0
    for number in first_list:
        frequency = second_list_counts.get(number, 0)  # Get the count of the number in the second list
        similarity_score += number * frequency

    return similarity_score

file_path = 'day_01_input.txt'  # Replace with the path to your file
sorted_first, sorted_second = process_file(file_path)
similarity_score = calculate_similarity_score(sorted_first, sorted_second)
print("Similarity score:", similarity_score)