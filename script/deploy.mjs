import { execSync } from "child_process";
import { readFileSync } from "fs";
import https from "https";

const GITHUB_REPO = "ahow/supply-chain-risk-api";

const GITHUB_PAT = process.env.GITHUB_PAT;

if (!GITHUB_PAT) {
  console.error("GITHUB_PAT secret is not set");
  process.exit(1);
}

function githubApi(method, endpoint, body = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: "api.github.com",
      path: endpoint,
      method,
      headers: {
        Authorization: `token ${GITHUB_PAT}`,
        "User-Agent": "deploy-script",
        Accept: "application/vnd.github.v3+json",
        ...(body ? { "Content-Type": "application/json" } : {}),
      },
    };

    const req = https.request(options, (res) => {
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(data ? JSON.parse(data) : {});
        } else if (res.statusCode === 404) {
          resolve(null);
        } else {
          reject(
            new Error(
              `GitHub API ${method} ${endpoint} returned ${res.statusCode}: ${data}`
            )
          );
        }
      });
    });
    req.on("error", reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

async function ensureGithubRepo() {
  console.log(`Checking GitHub repo ${GITHUB_REPO}...`);
  const repo = await githubApi("GET", `/repos/${GITHUB_REPO}`);
  if (repo) {
    console.log("GitHub repo exists.");
    return;
  }
  console.log("Creating GitHub repo...");
  const repoName = GITHUB_REPO.split("/")[1];
  await githubApi("POST", "/user/repos", {
    name: repoName,
    private: false,
    description:
      "Supply Chain Risk Assessment API - Multi-dimensional risk exposure analysis",
  });
  console.log("GitHub repo created.");
}

async function pushToGithub() {
  console.log("\nPushing code to GitHub...");

  const filesToInclude = execSync(
    'find . -type f ' +
    '-not -path "./.git/*" ' +
    '-not -path "./node_modules/*" ' +
    '-not -path "./dist/*" ' +
    '-not -path "./.local/*" ' +
    '-not -path "./.cache/*" ' +
    '-not -path "./.config/*" ' +
    '-not -path "./.upm/*" ' +
    '-not -path "./attached_assets/*" ' +
    '-not -path "./.replit" ' +
    '-not -path "./.nix-*" ' +
    '-not -path "./replit.nix" ' +
    '-not -path "./replit.md" ' +
    '-not -path "./.env*" ' +
    '-not -name "*.lock" ' +
    '| sort',
    { encoding: "utf-8" }
  ).trim().split("\n").filter(Boolean);

  console.log(`Found ${filesToInclude.length} files to push.`);

  let ref;
  try {
    ref = await githubApi("GET", `/repos/${GITHUB_REPO}/git/ref/heads/main`);
  } catch (e) {
    ref = null;
  }

  const treeItems = [];
  for (const filePath of filesToInclude) {
    const relativePath = filePath.replace(/^\.\//, "");
    const content = readFileSync(filePath);

    let isText = true;
    for (let i = 0; i < Math.min(content.length, 8000); i++) {
      if (content[i] === 0) {
        isText = false;
        break;
      }
    }

    const blob = await githubApi(
      "POST",
      `/repos/${GITHUB_REPO}/git/blobs`,
      {
        content: isText ? content.toString("utf-8") : content.toString("base64"),
        encoding: isText ? "utf-8" : "base64",
      }
    );
    treeItems.push({
      path: relativePath,
      mode: "100644",
      type: "blob",
      sha: blob.sha,
    });
  }

  console.log(`Created ${treeItems.length} blobs.`);

  const tree = await githubApi(
    "POST",
    `/repos/${GITHUB_REPO}/git/trees`,
    { tree: treeItems }
  );
  console.log(`Created tree: ${tree.sha}`);

  const commitData = {
    message: `Deploy: ${new Date().toISOString()}`,
    tree: tree.sha,
  };
  if (ref && ref.object) {
    commitData.parents = [ref.object.sha];
  }

  const commit = await githubApi(
    "POST",
    `/repos/${GITHUB_REPO}/git/commits`,
    commitData
  );
  console.log(`Created commit: ${commit.sha}`);

  if (ref && ref.object) {
    await githubApi(
      "PATCH",
      `/repos/${GITHUB_REPO}/git/refs/heads/main`,
      { sha: commit.sha, force: true }
    );
  } else {
    await githubApi("POST", `/repos/${GITHUB_REPO}/git/refs`, {
      ref: "refs/heads/main",
      sha: commit.sha,
    });
  }

  console.log("Code pushed to GitHub successfully.");
  console.log("GitHub Actions will automatically deploy to Heroku.");
  console.log(`\nCheck status: https://github.com/${GITHUB_REPO}/actions`);
  console.log("App URL: https://supply-chain-risk-api-7567b2b7e4c5.herokuapp.com");
}

async function main() {
  console.log("=== Push to GitHub (auto-deploys to Heroku) ===\n");

  try {
    await ensureGithubRepo();
    await pushToGithub();
    console.log("\n=== Done! ===");
  } catch (err) {
    console.error("\nFailed:", err.message);
    process.exit(1);
  }
}

main();
