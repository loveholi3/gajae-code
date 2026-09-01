import { describe, expect, it } from "bun:test";
import { type AttemptScope, createLineageCurrentness } from "../src/attempt-scope.js";

describe("createLineageCurrentness", () => {
	it("should initialize with current generation 0 and no current attempt", () => {
		const auth = createLineageCurrentness("main");
		expect(auth.lineage).toBe("main");
		expect(auth.current).toBe(0);

		// Initially, no valid scope can be current since currentAttemptId is undefined
		// but AttemptScope requires attemptId to be a string.
		const scope: AttemptScope = { lineage: "main", generation: 0, attemptId: "any" };
		expect(auth.isCurrent(scope)).toBe(false);
	});

	it("should advance generation and track current attempt id", () => {
		const auth = createLineageCurrentness("main");

		const nextGeneration = auth.advance("attempt-1");
		expect(nextGeneration).toBe(1);
		expect(auth.current).toBe(1);

		const validScope: AttemptScope = { lineage: "main", generation: 1, attemptId: "attempt-1" };
		expect(auth.isCurrent(validScope)).toBe(true);
	});

	it("should return false for isCurrent when lineage does not match", () => {
		const auth = createLineageCurrentness("main");
		auth.advance("attempt-1");

		const wrongLineageScope: AttemptScope = { lineage: "side:abc", generation: 1, attemptId: "attempt-1" };
		expect(auth.isCurrent(wrongLineageScope)).toBe(false);
	});

	it("should return false for isCurrent when generation does not match", () => {
		const auth = createLineageCurrentness("main");
		auth.advance("attempt-1");

		const wrongGenerationScope: AttemptScope = { lineage: "main", generation: 0, attemptId: "attempt-1" };
		expect(auth.isCurrent(wrongGenerationScope)).toBe(false);
	});

	it("should return false for isCurrent when attemptId does not match", () => {
		const auth = createLineageCurrentness("main");
		auth.advance("attempt-1");

		const wrongAttemptScope: AttemptScope = { lineage: "main", generation: 1, attemptId: "attempt-2" };
		expect(auth.isCurrent(wrongAttemptScope)).toBe(false);
	});

	it("should supersede the previous attempt when advanced", () => {
		const auth = createLineageCurrentness("main");

		auth.advance("attempt-1");
		const prevScope: AttemptScope = { lineage: "main", generation: 1, attemptId: "attempt-1" };
		expect(auth.isCurrent(prevScope)).toBe(true);

		// Advance again
		const nextGeneration = auth.advance("attempt-2");
		expect(nextGeneration).toBe(2);
		expect(auth.current).toBe(2);

		// Previous scope is no longer current
		expect(auth.isCurrent(prevScope)).toBe(false);

		// New scope is current
		const newScope: AttemptScope = { lineage: "main", generation: 2, attemptId: "attempt-2" };
		expect(auth.isCurrent(newScope)).toBe(true);
	});
});
