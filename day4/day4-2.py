from datetime import datetime
from itertools import accumulate

pointMap = {}
cardCountMap = {}


def readInputFile(inputFile: str) -> list[tuple[list[int], list[int]]]:
    with open(inputFile) as file:
        return [getInputsFromLine(line) for line in file]


def getInputsFromLine(inputStr: str) -> tuple[list[int], list[int]]:
    lineData = inputStr.split(":")
    # print(f"{lineData[0]}, ", end="")
    winningNumStr, inputNumStr = lineData[1].split("|")
    winningNumArr = [inp for inp in winningNumStr.strip().split(" ") if inp.isnumeric()]
    inputNumArr = [inp for inp in inputNumStr.strip().split(" ") if inp.isnumeric()]
    return winningNumArr, inputNumArr


def getPoints(arrObj: tuple[list[int], list[int]]) -> int:
    winningNumArr, inputNumArr = arrObj
    return len(set(winningNumArr) & set(inputNumArr))


def getCopyMap(inputArr: list[tuple[list[int], list[int]]]) -> dict[int, list[int]]:
    cardCopyMap = {}
    for idx, arrObj in enumerate(inputArr):
        winningNumberCount = getPoints(arrObj)
        # print(
        #     f"index:{idx}, winningNumberCount: {winningNumberCount}, rangeStart: {idx} -> rangeEnd: {winningNumberCount +idx+ 2}"
        # )
        cardCopyMap[idx + 1] = list(range(idx + 2, winningNumberCount + idx + 2))
    return cardCopyMap


def calculateNumberCards(inputArr: list[int]):
    global pointMap
    for idx in inputArr:
        # print(f"incrementing count for card no: {idx}")
        cardCountMap[idx] = cardCountMap.get(idx, 0) + 1
        calculateNumberCards(pointMap.get(idx, []))


def solution(inputFile: str):
    global pointMap
    inputArr = readInputFile(inputFile)
    pointMap = getCopyMap(inputArr)
    # print(f"cardCopyMap: {pointMap}")
    for key, value in pointMap.items():
        cardCountMap[key] = cardCountMap.get(key, 0) + 1
        calculateNumberCards(value)
    # print(f"cardCountMap: {cardCountMap}")
    return list(accumulate(cardCountMap.values()))[-1]


if __name__ == "__main__":
    startTime = datetime.now()
    result = solution("inputs/day4.input.txt")
    print(
        f"result: {result}. Executed in {(datetime.now()-startTime).microseconds / 1000} ms"
    )
