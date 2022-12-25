#!/usr/bin/env python3

char_to_val = {"=": -2, "-": -1, "0": 0, "1": 1, "2": 2}
val_to_char = {}
for (k, v) in char_to_val.items():
    val_to_char[v] = k

cur_sum = "0"
with open("day25.txt") as infile:
    for line in infile:
        addend = line.rstrip()
        # Rather than convert to and back from decimal, I'm going to do all the addition in this base
        # This is probably a silly way of doing things, but it's more fun

        new_val = ""

        # equalize lengths, just to make life easier
        if len(cur_sum) < len(addend):
            cur_sum = '0'*(len(addend)-len(cur_sum)) + cur_sum
        if len(addend) < len(cur_sum):
            addend = '0'*(len(cur_sum)-len(addend)) + addend

        carry = 0
        for i in range(len(cur_sum)-1, -1, -1):
            digit_sum = char_to_val[cur_sum[i]] + char_to_val[addend[i]] + carry
            carry = 0
            while digit_sum > 2:
                digit_sum -= 5
                carry += 1
            while digit_sum < -2:
                digit_sum += 5
                carry -= 1

            new_val = val_to_char[digit_sum] + new_val

        if carry != 0:
            new_val = val_to_char[carry] + new_val

        cur_sum = new_val

print("Total sum is", cur_sum)
