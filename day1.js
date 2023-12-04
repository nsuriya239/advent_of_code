import { Performance } from "perf_hooks";
import { readFileSync } from "node:fs";

// Replace all numeric  words to numeric digits
const replaceNumericWords = (inputLine) =>
	inputLine
		.replaceAll(/one/gi, "1")
		.replaceAll(/two/gi, "2")
		.replaceAll(/three/gi, "3")
		.replaceAll(/four/gi, "4")
		.replaceAll(/five/gi, "5")
		.replaceAll(/six/gi, "6")
		.replaceAll(/seven/gi, "7")
		.replaceAll(/eight/gi, "8")
		.replaceAll(/nine/gi, "9")
		.replaceAll(/zero/gi, "0");

// extractsNumbers from the string
const extractNumbers = (lineInput) => {
	return lineInput.match(/\d/g);
};

// If there is only one digit then convert it to a 2 digit with same value else take the 1st and last values to form a 2 digit value
// Eg: Input is [ '3' ] => '33', Input is ['1','3','6'] => '16'
const generateDigitsToBeCalibrated = (extractedNumberArr) => {
	if (extractedNumberArr.length > 1) {
		return parseInt(`${extractedNumberArr[0]}${extractedNumberArr[extractedNumberArr.length - 1]}`);
	}
	return parseInt(extractedNumberArr[0].repeat(2));
};

// extracts the numbers and generate the 2 digit value based on the condition
const processLineInput = (lineInput) => {
	const processedString = replaceNumericWords(lineInput);
	const extractedNumberArr = extractNumbers(processedString);
	return generateDigitsToBeCalibrated(extractedNumberArr);
};

export const readInput = (fileName) => {
	return readFileSync(fileName, "utf8", (err, data) => {
		if (err) throw err;
		return data.toString();
	});
};

const readAndSplitInputByLine = (inputFile) => {
	return readInput(inputFile).split(/\r?\n/);
};

// Step 1: read the input file

// Step 2: split the input by newline /n

// Step 3: Extract the number from the the inputLine

// Step 4: sum all the extracted values
const findCalibrationValue = (inputFile) => {
	const inputArr = readAndSplitInputByLine(inputFile);
	// const extractedLineValues = inputArr.map(processLineInput);
	const extractedLineValues = inputArr.map(getFirstandLastNumericValue);
	const finalCalibrationValue = extractedLineValues.reduce((sum, lineValue) => sum + lineValue, 0);
	return finalCalibrationValue;
};

// part 2 - need to also consider numeric words
// there are cases were the the words might be overlaped
// eg: nineninesixskjkbhx6nineoneightj ==> here at the end words "one" and "eight" are overlaped
// so to overcome this considered the index to get the first and last values
const getFirstandLastNumericValue = (input) => {
	let firstIndex = input.length - 1;
	let lastIndex = 0;
	let firstValue = "";
	let lastValue = "";

	const numericArr = [
		"one",
		"two",
		"three",
		"four",
		"four",
		"five",
		"six",
		"seven",
		"eight",
		"nine",
		1,
		2,
		3,
		4,
		5,
		6,
		7,
		8,
		9,
	];

	numericArr.forEach((value) => {
		const firstMatchIndex = input.indexOf(value);
		const lastMatchIndex = input.lastIndexOf(value);
		if (firstMatchIndex >= 0 && firstMatchIndex <= firstIndex) {
			firstIndex = firstMatchIndex;
			firstValue = isNaN(value) ? replaceNumericWords(value) : value;
		}
		if (lastMatchIndex >= 0 && lastMatchIndex >= lastIndex) {
			lastIndex = lastMatchIndex;
			lastValue = isNaN(value) ? replaceNumericWords(value) : value;
		}
	});

	return parseInt(`${firstValue}${lastValue}`);
};

let startTime = performance.now();
const result = findCalibrationValue("inputs/day1.input.txt");
let time = performance.now() - startTime;
console.log(`Result: ${result}, Timer: ${time} ms`);
