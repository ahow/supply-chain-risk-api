import fs from "fs";
import path from "path";
import https from "https";

const GITHUB_PAT = process.env.GITHUB_PAT;
const OWNER = "ahow";
const REPO = "supply-chain-risk-api";
const BRANCH = "main";

function githubApi(method, endpoint, body = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: "api.github.com",
      path: endpoint,
      method,
      headers: {
        Authorization: `token ${GITHUB_PAT}`,
        "User-Agent": "supply-chain-risk-api",
        "Content-Type": "application/json",
        Accept: "application/vnd.github.v3+json",
      },
    };

    const req = https.request(options, (res) => {
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", () => {
        try {
          resolve({ status: res.statusCode, data: JSON.parse(data || "{}") });
        } catch {
          resolve({ status: res.statusCode, data: {} });
        }
      });
    });
    req.on("error", reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

const IGNORE = new Set([
  "node_modules",
  ".git",
  "dist",
  ".env",
  ".cache",
  ".config",
  ".local",
  ".upm",
  "attached_assets",
  ".replit",
  "replit.nix",
  "replit.md",
  "replit_zip_error_log.txt",
  ".breakpoints",
  "generated-icon.png",
  "scripts",
]);

function collectFiles(dir, base = "") {
  const results = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const rel = base ? `${base}/${entry.name}` : entry.name;
    if (IGNORE.has(entry.name)) continue;
    if (entry.name.startsWith(".")) continue;
    if (entry.isDirectory()) {
      results.push(...collectFiles(path.join(dir, entry.name), rel));
    } else {
      results.push(rel);
    }
  }
  return results;
}

async function createBlob(content) {
  const res = await githubApi("POST", `/repos/${OWNER}/${REPO}/git/blobs`, {
    content: Buffer.from(content).toString("base64"),
    encoding: "base64",
  });
  return res.data.sha;
}

async function run() {
  console.log("Collecting files...");
  const root = "/home/runner/workspace";
  const files = collectFiles(root);
  console.log(`Found ${files.length} files to push`);

  let parentSha = null;
  let baseTreeSha = null;
  try {
    const refRes = await githubApi("GET", `/repos/${OWNER}/${REPO}/git/ref/heads/${BRANCH}`);
    if (refRes.status === 200) {
      parentSha = refRes.data.object.sha;
      const commitRes = await githubApi("GET", `/repos/${OWNER}/${REPO}/git/commits/${parentSha}`);
      baseTreeSha = commitRes.data.tree.sha;
    }
  } catch {}

  console.log("Creating blobs...");
  const treeItems = [];
  const batchSize = 5;
  for (let i = 0; i < files.length; i += batchSize) {
    const batch = files.slice(i, i + batchSize);
    const results = await Promise.all(
      batch.map(async (filePath) => {
        const fullPath = path.join(root, filePath);
        const content = fs.readFileSync(fullPath);
        const sha = await createBlob(content);
        return { path: filePath, mode: "100644", type: "blob", sha };
      })
    );
    treeItems.push(...results);
    process.stdout.write(`  ${Math.min(i + batchSize, files.length)}/${files.length}\r`);
  }
  console.log(`\nCreated ${treeItems.length} blobs`);

  console.log("Creating tree...");
  const treeRes = await githubApi("POST", `/repos/${OWNER}/${REPO}/git/trees`, {
    tree: treeItems,
  });
  const treeSha = treeRes.data.sha;

  console.log("Creating commit...");
  const commitBody = {
    message: "Supply Chain Risk Assessment API v4.0.0 - Full implementation",
    tree: treeSha,
    parents: parentSha ? [parentSha] : [],
  };
  const commitRes = await githubApi("POST", `/repos/${OWNER}/${REPO}/git/commits`, commitBody);
  const newCommitSha = commitRes.data.sha;

  console.log("Updating branch reference...");
  if (parentSha) {
    await githubApi("PATCH", `/repos/${OWNER}/${REPO}/git/refs/heads/${BRANCH}`, {
      sha: newCommitSha,
      force: true,
    });
  } else {
    await githubApi("POST", `/repos/${OWNER}/${REPO}/git/refs`, {
      ref: `refs/heads/${BRANCH}`,
      sha: newCommitSha,
    });
  }

  console.log(`\nPushed to https://github.com/${OWNER}/${REPO}`);
}

run().catch((err) => {
  console.error("Push failed:", err);
  process.exit(1);
});
