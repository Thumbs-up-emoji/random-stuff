import pyperclip

def modify_string(s):
    # Prepend "wa.me/91" to the string
    return "wa.me/91" + s

strings = []
print("Enter the strings one by one, and an empty line when done.")
while True:
    line = input()
    if line:
        strings.append(line)
    else:
        break

modified_strings = [modify_string(s) for s in strings]

result = '\n'.join(modified_strings)

pyperclip.copy(result)