import { describe, expect, it, spyOn } from "bun:test";
import * as fs from "node:fs/promises";
import * as path from "node:path";
import { sha256File } from "../bench/composer-evidence-report";

describe("composer-evidence-report", () => {
	describe("sha256File", () => {
		it("returns undefined when fs.readFile throws an error", async () => {
			const readFileSpy = spyOn(fs, "readFile").mockRejectedValue(new Error("Mocked read error"));

			try {
				const result = await sha256File("non-existent-file.txt");
				expect(result).toBeUndefined();
			} finally {
				readFileSpy.mockRestore();
			}
		});

		it("returns the correct sha256 hash for an existing file", async () => {
			const tempFilePath = path.join(import.meta.dir, "temp-test-file.txt");
			await fs.writeFile(tempFilePath, "hello world");

			try {
				const result = await sha256File(tempFilePath);
				// echo -n "hello world" | sha256sum -> b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9
				expect(result).toBe("b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9");
			} finally {
				await fs.unlink(tempFilePath);
			}
		});
	});
});
