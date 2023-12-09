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
    return re.search("[^a-zA-Z.\d\s:]", inputStr)


def replaceSymbolWithPeriod(inputStr, symbolIndex):
    return f"{inputStr[:symbolIndex]}.{inputStr[symbolIndex + 1:]}"


def getLeftNumber(symbolIndex, inputStr):
    if inputStr[symbolIndex - 1] == "." or not inputStr[symbolIndex - 1].isalnum():
        # print(f"symbolIndex: {symbolIndex} Has no left adjacent number")
        return 0
    periodIndex = getLastPeriodIndex(inputStr=inputStr[:symbolIndex])
    startIndex = periodIndex + 1 if periodIndex != -1 else 0
    leftNumber = int(inputStr[startIndex:symbolIndex])
    # print(
    #     f"left: PeriodIndex: {periodIndex}, symbolIndex: {symbolIndex}, Number: {leftNumber}"
    # )
    return leftNumber


def getRightNumber(symbolIndex, inputStr):
    if inputStr[symbolIndex + 1] == "." or not inputStr[symbolIndex + 1].isalnum():
        # print(f"symbolIndex: {symbolIndex} Has no right adjacent number")
        return 0
    periodIndex = getFirstPeriodIndex(inputStr=inputStr[symbolIndex + 1 :])
    endIndex = symbolIndex + periodIndex + 1 if periodIndex != -1 else len(inputStr)
    rightNumber = int(inputStr[symbolIndex + 1 : endIndex])
    # print(
    #     f"Right: PeriodIndex: {periodIndex}, symbolIndex: {symbolIndex}, Number: {rightNumber}"
    # )
    return rightNumber


def getVerticalNumber(symbolIndex, inputStr):
    startIndex = getLastPeriodIndex(inputStr[:symbolIndex])
    endIndex = getFirstPeriodIndex(inputStr[symbolIndex:])
    # print(
    #     f"vertical: symbolIndex: {symbolIndex}, startIndex: {startIndex}, endIndex: {endIndex}"
    # )
    verticalNumber = int(inputStr[startIndex + 1 : symbolIndex + endIndex])
    # print(f"vertical: symbolIndex: {symbolIndex}, Number: {verticalNumber}")
    return verticalNumber


def getDiagonalOrVerticalNumber(symbolIndex, inputStr):
    if not inputStr[symbolIndex].isalnum():
        # print(f"symbolIndex: {symbolIndex} Has no direct vertical number")
        return getLeftNumber(symbolIndex, inputStr) + getRightNumber(
            symbolIndex, inputStr
        )
    return getVerticalNumber(symbolIndex, inputStr)


def getSurrondingSum(symbolIndex, lineIndex, input_data):
    sum = 0
    sum += getLeftNumber(symbolIndex, input_data[1])
    sum += getRightNumber(symbolIndex, input_data[1])
    sum += getDiagonalOrVerticalNumber(symbolIndex, input_data[0])
    sum += getDiagonalOrVerticalNumber(symbolIndex, input_data[2])
    # print(f"sum around index: {symbolIndex} at line: {lineIndex}, sum: {sum}")
    return sum


def processLine(inputStr, lineIndex, input_data, sum=0):
    if findSymbolIndex(inputStr) is None:
        # print(f"No symbols in line: {lineIndex}")
        return 0
    symbolIndex = findSymbolIndex(inputStr).start()
    # print(
    #     f"checking for surrounding sum at line: {lineIndex}, symbol: {inputStr[symbolIndex]}"
    # )
    sum += getSurrondingSum(symbolIndex, lineIndex, input_data)
    # print(f"sum at line: {lineIndex}, sum: {sum}")
    sum += processLine(
        replaceSymbolWithPeriod(inputStr, symbolIndex), lineIndex, input_data
    )
    return sum


def solution(inputFile):
    sum = 0
    input_data = readInputFile(inputFile)
    for lineIndex, line in enumerate(input_data):
        lineSum = processLine(
            line, lineIndex, input_data[lineIndex - 1 : lineIndex + 2]
        )
        # print(f"index: {lineIndex}, lineSum: {lineSum}")
        sum += lineSum
    return sum


if __name__ == "__main__":
    startTime = datetime.now()
    result = solution("inputs/day3.input.original.txt")
    print(
        f"result: {result}. Executed in {(datetime.now()-startTime).microseconds / 1000} ms"
    )
