import { execSync } from "child_process";
import { readFileSync, createReadStream, statSync, existsSync } from "fs";
import { createGzip } from "zlib";
import https from "https";
import { pipeline } from "stream/promises";
import { createWriteStream } from "fs";
import path from "path";

const GITHUB_REPO = "ahow/supply-chain-risk-api";
const HEROKU_APP = "supply-chain-risk-api";

const GITHUB_PAT = process.env.GITHUB_PAT;
const HEROKU_API_KEY = process.env.HEROKU_API_KEY;

if (!GITHUB_PAT) {
  console.error("GITHUB_PAT secret is not set");
  process.exit(1);
}
if (!HEROKU_API_KEY) {
  console.error("HEROKU_API_KEY secret is not set");
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

function herokuApi(method, endpoint, body = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: "api.heroku.com",
      path: endpoint,
      method,
      headers: {
        Authorization: `Bearer ${HEROKU_API_KEY}`,
        Accept: "application/vnd.heroku+json; version=3",
        "Content-Type": "application/json",
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
              `Heroku API ${method} ${endpoint} returned ${res.statusCode}: ${data}`
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

function uploadToHeroku(url, filePath) {
  execSync(`curl -sf -X PUT -H "Content-Type:" --data-binary @${filePath} "${url}"`, {
    stdio: "pipe",
    timeout: 60000,
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
  const [owner] = GITHUB_REPO.split("/");
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

    if (isText) {
      const blob = await githubApi(
        "POST",
        `/repos/${GITHUB_REPO}/git/blobs`,
        {
          content: content.toString("utf-8"),
          encoding: "utf-8",
        }
      );
      treeItems.push({
        path: relativePath,
        mode: "100644",
        type: "blob",
        sha: blob.sha,
      });
    } else {
      const blob = await githubApi(
        "POST",
        `/repos/${GITHUB_REPO}/git/blobs`,
        {
          content: content.toString("base64"),
          encoding: "base64",
        }
      );
      treeItems.push({
        path: relativePath,
        mode: "100644",
        type: "blob",
        sha: blob.sha,
      });
    }
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
  return commit.sha;
}

async function deployToHeroku() {
  console.log("\nDeploying to Heroku...");

  let app = await herokuApi("GET", `/apps/${HEROKU_APP}`);
  if (!app) {
    console.log(`Creating Heroku app: ${HEROKU_APP}...`);
    app = await herokuApi("POST", "/apps", {
      name: HEROKU_APP,
      stack: "heroku-24",
    });
    console.log("Heroku app created.");

    await herokuApi("PUT", `/apps/${HEROKU_APP}/buildpack-installations`, {
      updates: [{ buildpack: "heroku/nodejs" }],
    });
    console.log("Node.js buildpack set.");
  } else {
    console.log("Heroku app exists.");
  }

  console.log("Creating source tarball...");
  execSync(
    'tar czf /tmp/deploy.tar.gz ' +
    '--exclude=".git" ' +
    '--exclude="node_modules" ' +
    '--exclude="dist" ' +
    '--exclude=".local" ' +
    '--exclude=".cache" ' +
    '--exclude=".config" ' +
    '--exclude=".upm" ' +
    '--exclude="attached_assets" ' +
    '--exclude=".replit" ' +
    '--exclude=".nix-*" ' +
    '--exclude="replit.nix" ' +
    '--exclude="replit.md" ' +
    '--exclude=".env*" ' +
    '--exclude="*.lock" ' +
    '-C . .'
  );

  const tarSize = statSync("/tmp/deploy.tar.gz").size;
  console.log(`Tarball size: ${(tarSize / 1024 / 1024).toFixed(2)} MB`);

  console.log("Requesting source upload URL...");
  const source = await herokuApi(
    "POST",
    `/apps/${HEROKU_APP}/sources`
  );

  console.log("Uploading source...");
  await uploadToHeroku(source.source_blob.put_url, "/tmp/deploy.tar.gz");
  console.log("Source uploaded.");

  console.log("Triggering build...");
  const build = await herokuApi("POST", `/apps/${HEROKU_APP}/builds`, {
    source_blob: {
      url: source.source_blob.get_url,
      version: new Date().toISOString(),
    },
  });

  console.log(`Build started: ${build.id}`);
  console.log(`Status: ${build.status}`);

  let buildStatus = build;
  while (buildStatus.status === "pending") {
    await new Promise((r) => setTimeout(r, 5000));
    buildStatus = await herokuApi(
      "GET",
      `/apps/${HEROKU_APP}/builds/${build.id}`
    );
    console.log(`Build status: ${buildStatus.status}`);
  }

  if (buildStatus.status === "succeeded") {
    console.log("\nBuild succeeded!");
    console.log(`App URL: ${app.web_url || `https://${HEROKU_APP}.herokuapp.com`}`);
  } else {
    console.error("\nBuild failed!");
    if (buildStatus.output_stream_url) {
      console.log(`Build log: ${buildStatus.output_stream_url}`);
    }
    process.exit(1);
  }
}

async function setHerokuConfigVars() {
  console.log("\nChecking Heroku config vars...");
  const config = await herokuApi("GET", `/apps/${HEROKU_APP}/config-vars`);

  const varsToSet = {};
  const envKeys = [
    "GEMINI_API_KEY",
    "CLAUDE_API_KEY",
    "DEEPSEEK_API_KEY",
    "MINIMAX_API_KEY",
    "SESSION_SECRET",
  ];

  for (const key of envKeys) {
    if (process.env[key] && (!config || config[key] !== process.env[key])) {
      varsToSet[key] = process.env[key];
    }
  }

  if (!config || !config.NODE_ENV) {
    varsToSet.NODE_ENV = "production";
  }

  if (Object.keys(varsToSet).length > 0) {
    console.log(`Setting config vars: ${Object.keys(varsToSet).join(", ")}`);
    await herokuApi("PATCH", `/apps/${HEROKU_APP}/config-vars`, varsToSet);
    console.log("Config vars updated.");
  } else {
    console.log("Config vars are up to date.");
  }
}

async function main() {
  console.log("=== Supply Chain Risk API Deployment ===\n");

  try {
    await ensureGithubRepo();
    await pushToGithub();
    await setHerokuConfigVars();
    await deployToHeroku();
    console.log("\n=== Deployment complete! ===");
  } catch (err) {
    console.error("\nDeployment failed:", err.message);
    process.exit(1);
  }
}

main();
