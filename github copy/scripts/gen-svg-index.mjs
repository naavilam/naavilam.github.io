import { readdirSync, statSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const ROOT = "assets/svg";

function walk(dir, base = "") {
    const entries = readdirSync(dir).sort((a, b) => a.localeCompare(b));

    return entries.map(name => {
        const fullPath = join(dir, name);
        const relPath = join(base, name);
        const stat = statSync(fullPath);

        if (stat.isDirectory()) {
            return {
                type: "dir",
                name,
                path: relPath,
                children: walk(fullPath, relPath)
            };
        }

        if (name.toLowerCase().endsWith(".svg")) {
            return {
                type: "file",
                name,
                path: relPath
            };
        }

        return null;
    }).filter(Boolean);
}

const tree = {
    type: "dir",
    name: "svg",
    path: "",
    children: walk(ROOT)
};

writeFileSync(
    join(ROOT, "index.json"),
    JSON.stringify(tree, null, 2)
);

console.log(`[gen] SVG tree index written to ${ROOT}/index.json`);