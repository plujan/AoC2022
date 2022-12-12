#!/usr/bin/env python3

# This would probably better be done with a proper tree structure, but we're doing it the janky way. Each
# directory has an array of two dictionaries. The first contains files, where the value is just the size; the
# second contains other directories, where the value is another similar structure, all the way down.

directory_structure = {"/": [{}, {}]}
cur_path = [directory_structure["/"]]
cur_loc = cur_path[0]

with open("day7.txt") as infile:
    for line in infile:
        fields = line.rstrip().split(" ")
        if fields[0] != "$":
            print("Error: found not a command when expecting one")
            continue
        
        # Handle ls first so we can fall back into cd; this won't work if we have two ls's in a row
        # but that wouldn't make sense anyway
        if fields[1] == "ls":
            while True:
                try:
                    line = next(infile)
                except StopIteration:
                    break
                fields = line.rstrip().split(" ")
                if line[0] == "$":
                    if fields[1] == "ls":
                        print("Found ls after ls, this case won't be handled properly!")
                    break
                if fields[0] == "dir":
                    cur_loc[1][fields[1]] = [{}, {}]
                else:
                    cur_loc[0][fields[1]] = int(fields[0])

        if fields[1] == "cd":
            if fields[2] == "/":
                continue # we handled this in initialization
            elif fields[2] == "..":
                del cur_path[-1]
                cur_loc = cur_path[-1]
            else:
                cur_loc = cur_loc[1][fields[2]]
                cur_path.append(cur_loc)


tot_small_directories = 0
                
def compute_directory_size(d):
    global tot_small_directories
    cur_size = 0
    for i in d[0]:
        cur_size += d[0][i]
    for i in d[1]:
        cur_size += compute_directory_size(d[1][i])
    if cur_size <= 100000:
        tot_small_directories += cur_size
    return cur_size

# Now traverse!
compute_directory_size(directory_structure['/'])

print("Total small directory size is", tot_small_directories)
