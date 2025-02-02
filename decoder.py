

morse_dict = {
    ".-"    : "a",
    "-..."  : "b",
    "-.-."  : "c",
    "-.."   : "d",
    "."     : "e",
    "..-."  : "f",
    "--."   : "g",
    "...."  : "h",
    ".."    : "i",
    ".---"  : "j",
    "-.-"   : "k",
    ".-.."  : "l",
    "--"    : "m",
    "-."    : "n",
    "---"   : "o",
    ".--."  : "p",
    "--.-"  : "q",
    ".-."   : "r",
    "..."   : "s",
    "-"     : "t",
    "..-"   : "u",
    "...-"  : "v",
    ".--"   : "w",
    "-..-"  : "x",
    "-.--"  : "y",
    "--.."  : "z",
    "-----" : "0",
    ".----" : "1",
    "..---" : "2",
    "...--" : "3",
    "....-" : "4",
    "....." : "5",
    "-...." : "6",
    "--..." : "7",
    "---.." : "8",
    "----." : "9",
}

def decode_morse(morseCode):
    # 1. take morse code input and disassemple into nested list of lines, words, and symbols
    codeLines = morseCode.splitlines()
    codeWords = []

    for line in codeLines:
        codeWords.append(line.split("/"))

    tmpin = [[ [] for j in range(len(codeWords[i]))] for i in range(len(codeWords))]

    for i in range(len(codeLines)):
        #print("i:" + str(i))
        for j in range(len(codeWords[i])):
            #print("i, j: ", str(i), str(j))
            word = codeWords[i][j].split(" ")
            tmpin[i][j] = word
    # print(tmpin)

    # 2. reassemble text while translating morse code symbols to characters
    tmpout = [[ [] for j in range(len(tmpin[i]))] for i in range(len(tmpin))]           # dont need this, too much nesting [ [] for k in range(len(tmp[i][j]))]
    # print(tmpout)

    for i in range(len(tmpin)):
        for j in range(len(tmpin[i])):
            for sign in tmpin[i][j]:
                # find symbol key in dictionary
                letter = morse_dict.get(sign)
                if letter:
                    tmpout[i][j].append(letter)
                # If key not found, give default char and output warning
                else:
                    tmpout[i][j].append("( ͡° ͜ʖ ͡°)")    # TODO: Set an actual default char here, e.g. " " :P
                    print("WARNING: Code symbol not found in translation dictionary: " + sign)
    del tmpin # mark to free memory
    # print(tmpout)

    # 3. re-combine into string and provide output
    output = ""
    for i in tmpout:
        for j in i:
            jword = "".join(j)
            jword += " "
            output += jword
        output += "\n"

    print(output)


# TEST here
test_code = "--- ..- -.-. .... / .----\n.-.. --- .-.." #ouch 1\nlol
decode_morse(test_code)
