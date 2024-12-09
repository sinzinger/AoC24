"""
--- Part Two ---
Upon completion, two things immediately become clear. First, the disk definitely has a lot more contiguous free space, just like the amphipod hoped. Second, the computer is running much more slowly! Maybe introducing all of that file system fragmentation was a bad idea?

The eager amphipod already has a new plan: rather than move individual blocks, he'd like to try compacting the files on his disk by moving whole files instead.

This time, attempt to move whole files to the leftmost span of free space blocks that could fit the file. Attempt to move each file exactly once in order of decreasing file ID number starting with the file with the highest file ID number. If there is no span of free space to the left of a file that is large enough to fit the file, the file does not move.

The first example from above now proceeds differently:

00...111...2...333.44.5555.6666.777.888899
0099.111...2...333.44.5555.6666.777.8888..
0099.1117772...333.44.5555.6666.....8888..
0099.111777244.333....5555.6666.....8888..
00992111777.44.333....5555.6666.....8888..
The process of updating the filesystem checksum is the same; now, this example's checksum would be 2858.

Start over, now compacting the amphipod's hard drive using this new method instead. What is the resulting filesystem checksum?
"""

def parse_disk_map(filename):
    # e.g. 2333133121414131402
    file_content = open(filename).read()
    disk_map = []
    for i, d in enumerate(file_content, start=1):
        first_value = i // 2 + 1 if i % 2 else 0
        second_value = int(d)
        disk_map.append((first_value, second_value))
    return disk_map

def compact_disk(disk_map):
    for i in range(len(disk_map))[::-1]:
        for j in range(i):
            i_data, i_size = disk_map[i]
            j_data, j_size = disk_map[j]

            if i_data and not j_data and i_size <= j_size:
                disk_map[i] = (0, i_size)
                disk_map[j] = (0, j_size - i_size)
                disk_map.insert(j, (i_data, i_size))   
    return disk_map

def calculate_checksum(disk_map):
    # create a flattened list from the disk map
    flattened_disk_map = []
    for data, size in disk_map:
        # Repeat each file ID (data) according to its size
        flattened_disk_map.extend([data] * size)
    print (flattened_disk_map)

    checksum = 0
    for index, file_id in enumerate(flattened_disk_map):
        if file_id:
            checksum += index * (file_id - 1)

    print(checksum)

def main():
    disk_map = parse_disk_map("./day_09/day_09_input.txt")
    disk_map = compact_disk(disk_map)
    calculate_checksum(disk_map)
    
if __name__ == "__main__":
    main()