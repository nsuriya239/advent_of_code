from datetime import datetime
import re


def readInputFile(inputFile):
    with open(inputFile) as file:
        input_data = [line.rstrip() for line in file]
    return input_data


def getLastPeriodIndex(inputStr):
    return inputStr.rfind(".")


def getFirstPeriodIndex(inputStr):
    return inputStr.find(".")


def findSymbolIndex(inputStr):
    return re.search("[*]", inputStr)


def replaceSymbolWithPeriod(inputStr, symbolIndex):
    return f"{inputStr[:symbolIndex]}.{inputStr[symbolIndex + 1:]}"


def checkForTwoPartNumbers(
    left, right, top, topLeft, topRight, bottom, bottomLeft, bottomRight
):
    counter = 0
    gearRatio = 1
    # print(
    #     f"left:{left} right: {right} top: {top} topLeft: {topLeft} topRight: {topRight} bottom: {bottom} bottomLeft: {bottomLeft} bottomRight: {bottomRight}"
    # )
    if left > 0:
        counter += 1
        gearRatio *= left
    if right > 0:
        counter += 1
        gearRatio *= right
    if top > 0:
        counter += 1
        gearRatio *= top
    if topLeft > 0:
        counter += 1
        gearRatio *= topLeft
    if topRight > 0:
        counter += 1
        gearRatio *= topRight
    if bottom > 0:
        counter += 1
        gearRatio *= bottom
    if bottomLeft > 0:
        counter += 1
        gearRatio *= bottomLeft
    if bottomRight > 0:
        counter += 1
        gearRatio *= bottomRight
    return counter, gearRatio


def getLeftNumber(symbolIndex, inputStr):
    if inputStr[symbolIndex - 1] == "." or not inputStr[symbolIndex - 1].isalnum():
        return -1
    periodIndex = getLastPeriodIndex(inputStr=inputStr[:symbolIndex])
    startIndex = periodIndex + 1 if periodIndex != -1 else 0
    return int(inputStr[startIndex:symbolIndex])


def getRightNumber(symbolIndex, inputStr):
    if inputStr[symbolIndex + 1] == "." or not inputStr[symbolIndex + 1].isalnum():
        return -1
    periodIndex = getFirstPeriodIndex(inputStr=inputStr[symbolIndex + 1 :])
    endIndex = symbolIndex + periodIndex + 1 if periodIndex != -1 else len(inputStr)
    return int(inputStr[symbolIndex + 1 : endIndex])


def getVerticalNumber(symbolIndex, inputStr):
    startIndex = getLastPeriodIndex(inputStr[:symbolIndex])
    endIndex = getFirstPeriodIndex(inputStr[symbolIndex:])
    return int(inputStr[startIndex + 1 : symbolIndex + endIndex])


def getDiagonalOrVerticalNumber(symbolIndex, inputStr):
    if not inputStr[symbolIndex].isalnum():
        return (
            -1,
            getLeftNumber(symbolIndex, inputStr),
            getRightNumber(symbolIndex, inputStr),
        )
    return getVerticalNumber(symbolIndex, inputStr), -1, -1


def getGearRatio(symbolIndex, lineIndex, input_data):
    gearRatio = 1
    leftNumber = getLeftNumber(symbolIndex, input_data[1])
    rightNumber = getRightNumber(symbolIndex, input_data[1])
    topNumber, topLeft, topRight = getDiagonalOrVerticalNumber(
        symbolIndex, input_data[0]
    )
    bottomNumber, bottomLeft, bottomRight = getDiagonalOrVerticalNumber(
        symbolIndex, input_data[2]
    )
    counter, gearRatio = checkForTwoPartNumbers(
        leftNumber,
        rightNumber,
        topNumber,
        topLeft,
        topRight,
        bottomNumber,
        bottomLeft,
        bottomRight,
    )
    # print(
    #     f"gearRatio around index: {symbolIndex} at line: {lineIndex}, gearRatio: {gearRatio}, counter: {counter}"
    # )

    return gearRatio * 1 if counter == 2 else 0


def processLine(inputStr, lineIndex, input_data, gearRatio=0):
    if findSymbolIndex(inputStr) is None:
        # print(f"No symbols in line: {lineIndex}")
        return 0
    symbolIndex = findSymbolIndex(inputStr).start()
    # print(
    #     f"checking for GearRatio at line: {lineIndex}, symbol: {inputStr[symbolIndex]}, index: {symbolIndex}"
    # )
    gearRatio += getGearRatio(symbolIndex, lineIndex, input_data)
    gearRatio += processLine(
        replaceSymbolWithPeriod(inputStr, symbolIndex), lineIndex, input_data
    )
    return gearRatio


def solution(inputFile):
    sum = 0
    input_data = readInputFile(inputFile)
    for lineIndex, line in enumerate(input_data):
        lineSumOfGearRatio = processLine(
            line, lineIndex, input_data[lineIndex - 1 : lineIndex + 2]
        )
        # print(f"index: {lineIndex}, lineSum: {lineSumOfGearRatio}")
        sum += lineSumOfGearRatio
    return sum


if __name__ == "__main__":
    startTime = datetime.now()
    result = solution("inputs/day3.input.original.txt")
    print(
        f"result: {result}. Executed in {(datetime.now()-startTime).microseconds / 1000} ms"
    )
