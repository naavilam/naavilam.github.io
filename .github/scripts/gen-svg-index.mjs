import { readdirSync, writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const dir = "assets/svg";
mkdirSync(dir, { recursive: true });

const files = readdirSync(dir)
    .filter(f => f.toLowerCase().endsWith(".svg"))
    .sort((a, b) => a.localeCompare(b));

writeFileSync(join(dir, "index.json"), JSON.stringify({ files }, null, 2));
console.log(`[gen] ${files.length} svgs -> ${dir}/index.json`);