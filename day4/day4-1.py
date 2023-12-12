from datetime import datetime


def readInputFile(inputFile: str):
    with open(inputFile) as file:
        for line in file:
            yield getInputsFromLine(line)


def getInputsFromLine(inputStr: str) -> tuple[list[int], list[int]]:
    lineData = inputStr.split(":")
    # print(f"{lineData[0]}, ", end="")
    winningNumStr, inputNumStr = lineData[1].split("|")
    winningNumArr = [inp for inp in winningNumStr.strip().split(" ") if inp.isnumeric()]
    inputNumArr = [inp for inp in inputNumStr.strip().split(" ") if inp.isnumeric()]
    return winningNumArr, inputNumArr


def solution(inputFile: str):
    sum = 0
    for winningNumArr, inputNumArr in readInputFile(inputFile):
        winningNumberCount = len(set(winningNumArr) & set(inputNumArr))
        points = pow(2, winningNumberCount - 1) if winningNumberCount > 0 else 0
        # print(
        #     f"winningNumArr length: {len(winningNumArr)}, inputNumArr length: {len(inputNumArr)}, winningCount: {winningNumberCount}, points: {points}"
        # )
        sum += points
    return sum


if __name__ == "__main__":
    startTime = datetime.now()
    result = solution("inputs/day4.input.txt")
    print(
        f"result: {result}. Executed in {(datetime.now()-startTime).microseconds / 1000} ms"
    )
