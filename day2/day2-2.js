import { Performance } from "perf_hooks";
import { readFileSync } from "node:fs";

const readInput = (fileName) => {
	return readFileSync(fileName, "utf8", (err, data) => {
		if (err) throw err;
		return data.toString();
	});
};

const readAndSplitInputByLine = (inputFile) => {
	return readInput(inputFile).split(/\r?\n/);
};

const getCubeValues = (gameSet, cubePowers) => {
	const cubeArr = gameSet.split(",");
	cubeArr.map((cube) => {
		const trimmedCube = cube.trim();
		const [value, color] = trimmedCube.split(" ");
		if (parseInt(value) > cubePowers[color]) cubePowers[color] = parseInt(value);
	});
};

const getGameIdAndSets = (line) => {
	const lineArr = line.split(":");
	const gameId = lineArr[0];
	const gameSets = lineArr[1].split(";");
	return { gameId, gameSets };
};

const getCubePowers = (acc, input) => {
	const cubePowers = {
		red: 0,
		blue: 0,
		green: 0,
	};
	const { gameId, gameSets } = getGameIdAndSets(input);
	gameSets.map((gameSet) => {
		getCubeValues(gameSet, cubePowers);
	});
	const result = Object.values(cubePowers).reduce((acc, val) => acc * val, 1);
	return (acc += result);
};

const getSumOfCubePowers = (inputFile) => {
	const inputArr = readAndSplitInputByLine(inputFile);
	console.log(`length of file: ${inputArr.length}`);
	const sumOfGameIds = inputArr.reduce(getCubePowers, 0);
	return sumOfGameIds;
};

let startTime = performance.now();
const result = getSumOfCubePowers("inputs/day2.input.txt");
let time = performance.now() - startTime;
console.log(`Result: ${result}, Timer: ${time} ms`);

// console.log(
// 	getCubePowers(
// 		0,
// 		"Game 2: 3 blue, 1 green, 2 red; 2 red, 2 green, 5 blue; 3 green, 10 blue; 8 red, 1 blue; 3 red, 1 green, 5 blue; 1 blue, 5 red, 3 green"
// 	)
// );
