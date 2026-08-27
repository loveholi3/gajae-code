import { describe, it, expect } from "bun:test";
import { attemptScopesEqual, type AttemptScope } from "../src/attempt-scope.ts";

describe("attemptScopesEqual", () => {
	it("should return true when all properties match", () => {
		const scopeA: AttemptScope = { attemptId: "123", generation: 1, lineage: "main" };
		const scopeB: AttemptScope = { attemptId: "123", generation: 1, lineage: "main" };
		expect(attemptScopesEqual(scopeA, scopeB)).toBe(true);
	});

	it("should return false when attemptId differs", () => {
		const scopeA: AttemptScope = { attemptId: "123", generation: 1, lineage: "main" };
		const scopeB: AttemptScope = { attemptId: "456", generation: 1, lineage: "main" };
		expect(attemptScopesEqual(scopeA, scopeB)).toBe(false);
	});

	it("should return false when generation differs", () => {
		const scopeA: AttemptScope = { attemptId: "123", generation: 1, lineage: "main" };
		const scopeB: AttemptScope = { attemptId: "123", generation: 2, lineage: "main" };
		expect(attemptScopesEqual(scopeA, scopeB)).toBe(false);
	});

	it("should return false when lineage differs", () => {
		const scopeA: AttemptScope = { attemptId: "123", generation: 1, lineage: "main" };
		const scopeB: AttemptScope = { attemptId: "123", generation: 1, lineage: "side:abc" };
		expect(attemptScopesEqual(scopeA, scopeB)).toBe(false);
	});

	it("should return false when all properties differ", () => {
		const scopeA: AttemptScope = { attemptId: "123", generation: 1, lineage: "main" };
		const scopeB: AttemptScope = { attemptId: "456", generation: 2, lineage: "side:xyz" };
		expect(attemptScopesEqual(scopeA, scopeB)).toBe(false);
	});
});
