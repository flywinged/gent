from typing import List

def recursiveSplit(text: str, width: int, currentIndex = 0, lastWordIndex: int = 0, lastLineIndex: int = 0, returnValue: List[str] = None) -> List[str]:
    '''

    '''

    # Create the list input if it doesn't exist
    if returnValue == None:
        returnValue = []

    # Base case
    if currentIndex >= len(text):
        returnValue.append(text[lastLineIndex:])
        return returnValue
    
    # Whatever the current character is
    char = text[currentIndex]

    # If we've reached the end of the line
    if (currentIndex - lastLineIndex >= width and (char != "\n" and char != " ")):
        
        if lastWordIndex != lastLineIndex:
            returnValue.append(text[lastLineIndex:lastWordIndex])

        return recursiveSplit(text, width, currentIndex + 1, lastWordIndex, lastWordIndex, returnValue)
    
    else:

        # We are at a newline
        if char == "\n":
            returnValue.append(text[lastLineIndex:currentIndex + 1])
            return recursiveSplit(text, width, currentIndex + 1, currentIndex + 1, currentIndex + 1, returnValue)

        # We are at a space
        if char == " ":
            return recursiveSplit(text, width, currentIndex + 1, currentIndex + 1, lastLineIndex, returnValue)

        # Some other character
        return recursiveSplit(text, width, currentIndex + 1, lastWordIndex, lastLineIndex, returnValue)