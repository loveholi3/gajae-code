import { describe, expect, it } from "bun:test";
import { parseManifest } from "../bench/composer-evidence-report";

describe("composer-evidence-report parseManifest", () => {
	it("returns parsed manifest for valid JSON object", () => {
		const manifest = {
			schemaVersion: 1,
			composer_scenarios_version: "v1",
			capture_mode: "print",
			planned_records: 10,
		};
		const result = parseManifest(JSON.stringify(manifest));
		expect(result).toEqual(manifest);
	});

	it("returns undefined for empty string", () => {
		expect(parseManifest("")).toBeUndefined();
	});

	it("returns undefined for whitespace-only string", () => {
		expect(parseManifest("   \n\t  ")).toBeUndefined();
	});

	it("returns undefined for invalid JSON", () => {
		expect(parseManifest("{ invalid json ]")).toBeUndefined();
	});

	it("returns undefined when JSON is an array", () => {
		const result = parseManifest(JSON.stringify([{ schemaVersion: 1 }]));
		expect(result).toBeUndefined();
	});

	it("returns undefined when JSON is a primitive string", () => {
		const result = parseManifest(JSON.stringify("some string"));
		expect(result).toBeUndefined();
	});

	it("returns undefined when JSON is a primitive number", () => {
		const result = parseManifest(JSON.stringify(42));
		expect(result).toBeUndefined();
	});

	it("returns undefined when JSON is null", () => {
		const result = parseManifest("null");
		expect(result).toBeUndefined();
	});
});
