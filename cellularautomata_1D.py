
# cellular automata/algorithm development process:
# 1 make the rule (rule number > lookup table)
#     □ turn the input rule number (0-255) into a lookup table
#         ® turn rule number into 8 binary digits
#             ◊ add zeros to the front if shorter than 8 digits
#         ® list the 8 possible inputs in wolfram's order
#             ◊ every neighborhood possibility, from 111 to 000
#         ® pair each input with its output digit
#             ◊ 111-> 0 or 1, etc.
#                 } deterministic: set rule appllies the output digit to the neighborhood based on the rule and it doesn't change
#                 } stochastic: set rule applies the output digit to the neighborhood based on the rule and it changes based on a probability 
#                     – the probability could be based on the rule number, based on neighbors, based on some external thing... look into this further if you decide to try this
#                 } etc.?

# 2 set up the start (create an initial row of cells, set middle cell to 1 for ex)
# 3 step forward (build each new row from the old one)
# 4 draw it (visually represent the output of this)



# Wolfram code:
    # for a 3 bit neighborhood, all possible combinations of the neighborhood are as follows in key 1:
    # key 1: 
    # 111 110 101 100 011 010 001 000 
    
    # key 2:
    # the above key lines up with the below key:
    # the below key's possible combinations are any number between 0 and 255 represented in binary
    # from 0
    #  0   0   0   0   0   0   0   0
    # to 1
    #  0   0   0   0   0   0   0   1
    # all the way to 255 (2^8 -1)
    #  1   1   1   1   1   1   1   1

    # therefore, to line up a neighborhood with a bit value, we just need to:
    # take the rule number between 0 and 255,
    # convert it to its binary form
    # assign each bit one by one to key 1

# functions
def init(w, initial_pos):
    """
    Set up the first generation
    """
    w = int(w)
    initial_pos = int(initial_pos)
    if initial_pos > w:
        raise Exception("Initial position must be inside the width of the grid")

    row = []
        
    for i in range(w):
        if i == initial_pos-1:
            row.append(1)
        else:
            row.append(0)

    return row

# main function - overall logic, run other functions

def set_rule(n, neighborhood_size = 3):
    n = int(n)
    if (n < 0 or n > 255):
        raise Exception("Rule number must be between 0 and 255")

    # TODO autogenerate this ruleset instead, 
    # look into if there's a better data storage method for this than dict

    ruleset = {
        "111": 0,
        "110": 0,
        "101": 0,
        "100": 0,
        "011": 0,
        "010": 0,
        "001": 0,
        "000": 0
    }

    binary_rule = list(str(bin(n))[2:])
    l = len(binary_rule)
    rule_key = list('00000000')
    if l < 8:
        start = 8-l
        for i in range(l):
            rule_key[i+start] = binary_rule[i]
        # print(l)
    else:
        rule_key = binary_rule

    
    # print(binary_rule)
    # print(rule_key)


    i=0
    for key, value in ruleset.items():
        ruleset.update({key: rule_key[i]})
        i+=1

    # print(ruleset)

    return ruleset
    

def try_set_rule(rule):
    rule = int(rule)
    ruleset_accepted = 0
    while ruleset_accepted != 1:
        try:
            ruleset = set_rule(rule)
            ruleset_accepted = 1
        except Exception as e:
            print(f"Error: {e}")
            rule = input("Choose a rule set between 0 and 255:")
    return ruleset


def print_row(row):
    for bit in row:
        if bit:
            print("█", end="")
        else:
            print(" ", end="")
    print()


def determine_next_row(grid_width, prev_row, ruleset):
    # take grid width
    # 1 by one, for each item i in the grid
    # look at prev_row[i-1], prev_row[i], and prev_row[i+1]
        # if i is 0, then ?
            # take i, i+1, i+2?
            # consider i-1 as 0?
            # TODO - test both and decide based on behavior compared to online demos of this experiment which you would like to go with
        # if i is 99, then ^ opposite of above
    # compare that

    next_row = []

    max_pixel = int(grid_width)
    # print(f"MAX PIXEL: {max_pixel}")

    # print(f"PREVIOUS ROW: {prev_row}")

    for i in range(max_pixel):
        neighborhood = ''
        if i == 0:
            neighborhood+=f"0{prev_row[i]}{prev_row[i+1]}"
        elif i==max_pixel-1:
            neighborhood+=f"{prev_row[i-1]}{prev_row[i]}0"
        elif i<max_pixel:
            neighborhood+=f"{prev_row[i-1]}{prev_row[i]}{prev_row[i+1]}"

        # print(f"{i}:")

        for key , value in ruleset.items():
            # RESOLVED bug - not finding this match - 
            # print(str(key)) # key returns 000
            # print(str(neighborhood)) # neighborhood returns [1, 0, 0]
            # solution: initiate neighborhood as an empty string rather than a list, concatenate it rather than appending it
            # potential better solutions: store key and neighborhood as lists, or:
            # store both as ints and use math to compare - most likely better performance than string comparison
            if str(key) == str(neighborhood):
                # print(f"key neighborhood match found: {key} {neighborhood}")
                next_row.append(int(value))
                # print(next_row)
                # print(f":{i}")
                break
               

    # print(f"NEXT ROW: {next_row}")
    return next_row



def main():

# INITIALIZE FIRST ROW
    rows = []

    grid_width = int(input("Choose grid width: "))
    initial_pos = int(input("Choose starting position of seed block: "))
    init_row = init(grid_width, initial_pos)

    rows.append(init_row)
    # print(f"ROWS: {rows}")

# SET RULE
    rule = int(input("Choose a rule set between 0 and 255:"))
    ruleset = try_set_rule(rule)

    # print(f"Rule set {rule} selected")
    # print(f"RULESET KEY: {ruleset}")

# GENERATE ROWS

    h = int(input("Choose number of generations for simulation: "))
    for i in range(h):
        next_row = determine_next_row(grid_width, rows[i], ruleset)
        rows.append(next_row)
        

    # print(f"ROWS: {rows}")

# DISPLAY ROWS:
    for i in range(len(rows)):
        print_row(rows[i])
    



# main block
if __name__ == '__main__':
    main()