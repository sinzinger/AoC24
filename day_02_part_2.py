"""
--- Part Two ---
The engineers are surprised by the low number of safe reports until they realize they forgot to tell you about the Problem Dampener.

The Problem Dampener is a reactor-mounted module that lets the reactor safety systems tolerate a single bad level in what would otherwise be a safe report. It's like the bad level never happened!

Now, the same rules apply as before, except if removing a single level from an unsafe report would make it safe, the report instead counts as safe.

More of the above example's reports are now safe:

7 6 4 2 1: Safe without removing any level.
1 2 7 8 9: Unsafe regardless of which level is removed.
9 7 6 2 1: Unsafe regardless of which level is removed.
1 3 2 4 5: Safe by removing the second level, 3.
8 6 4 4 1: Safe by removing the third level, 4.
1 3 6 7 9: Safe without removing any level.
Thanks to the Problem Dampener, 4 reports are actually safe!

Update your analysis by handling situations where the Problem Dampener can remove a single level from unsafe reports. How many reports are now safe?
"""

def is_safe_report(levels):
    """Check if a report (list of levels) is safe."""
    increasing = all(levels[i] < levels[i + 1] for i in range(len(levels) - 1))
    decreasing = all(levels[i] > levels[i + 1] for i in range(len(levels) - 1))
    valid_difference = all(1 <= abs(levels[i] - levels[i + 1]) <= 3 for i in range(len(levels) - 1))
    return (increasing or decreasing) and valid_difference

def is_safe_with_dampener(levels):
    """Check if a report can be safe by removing one bad level."""
    n = len(levels)
    for i in range(n):
        # Create a new report with the i-th level removed
        modified_levels = levels[:i] + levels[i + 1:]
        # Check if the modified report is safe
        if is_safe_report(modified_levels):
            return True
    return False

def count_safe_reports_with_dampener(file_path):
    """Count the number of safe reports with the Problem Dampener."""
    safe_count = 0

    with open(file_path, 'r') as file:
        for line in file:
            try:
                levels = list(map(int, line.split()))
            except ValueError:
                continue

            # Check if the report is safe directly or with the dampener
            if is_safe_report(levels) or is_safe_with_dampener(levels):
                safe_count += 1

    return safe_count

# Example usage
file_path = 'day_02_input.txt' 
safe_reports_count = count_safe_reports_with_dampener(file_path)
print("Number of safe reports with Problem Dampener:", safe_reports_count)