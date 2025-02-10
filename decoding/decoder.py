# Dictionary for  all morse symbols
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
    ".-..." : "&",
    "--..--": ",",
    ".-.-.-": ".",
    "-.-.--": "!",
    "..--..": "?",
    "---...": ":",
    ".----.": "'",
    "-....-": "-",
    ".-..-.": '"',
    ".--.-.": "@",
    "-.--.-": ")",
    "-.--." : "(",
    "-...-" : "=",
    ".-.-." : "+",
    "-..-." : "/"
}


def decode_morse(morseCode):
    """
    Receive a morse code as strings of '. -' and break it down into the individual symbomls the OCR recognised
    Then recombine the individual letters 
    """
    translation_failed = False
    output = ""
    codesign_failed_list = []
    # if ocr engine fails and returns an empty string, return and pass an error message to the UI
    if not morseCode:
        output = "Error: didn't receive a proper code to decode. This can happen if the OCR engine failed to recognise the image.\nTry to center the code under the camera, or write it again."
        return output
    
    #1 Take morse code input and disassemple into nested lists of lines, words, and symbols
    codeLines = morseCode.splitlines()
    codeWords = []

    for line in codeLines:
        codeWords.append( list(filter(None, line.split("/"))) ) # split at word separators '/' and filter any empty lists that split("/") creates

    tmpin = [[ [] for j in range(len(codeWords[i]))] for i in range(len(codeWords))]

    for i in range(len(codeLines)):
        for j in range(len(codeWords[i])):
            word = codeWords[i][j].split(" ")
            tmpin[i][j] = word
    #print(tmpin)   #test

    #2 Reassemble text while translating morse code symbols to characters
    tmpout = [[ [] for j in range(len(tmpin[i]))] for i in range(len(tmpin))]           # dont need this, too much nesting [ [] for k in range(len(tmp[i][j]))]

    for i in range(len(tmpin)):
        for j in range(len(tmpin[i])):
            for sign in tmpin[i][j]:
                # find symbol key in dictionary, or produce 
                letter = morse_dict.get(sign)
                if letter:                      # If key pair found add letter to current word list
                    tmpout[i][j].append(letter)
                else:                           # If key not found, give default char '⚠' and output warning
                    tmpout[i][j].append('\u26A0')
                    translation_failed = True
                    codesign_failed_list.append(sign)
                    print("WARNING: Code symbol not found in translation dictionary: " + sign)
    del tmpin # mark to free memory
    #print(tmpout) #test

    if translation_failed:
        output = "Oops, the decoder failed to recognise all or part of the code:\n"
        for sign in codesign_failed_list:
            output += sign + "\n"
        output += "\nCode translation:\n\n"
    #3 Re-combine into string and provide output
    for i in tmpout:
        for j in i:
            jword = "".join(j)
            jword += " "
            output += jword
        #output += "\n" #don't restore new lines from ocr as it can make the text block huge!
        
    del tmpout # mark to free memory
    return output