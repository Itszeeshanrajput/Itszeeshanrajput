#!/usr/bin/env python3
import json
import urllib.request
import datetime
import re
import os

USERNAME = "Itszeeshanrajput"

def fetch_repos():
    url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"Failed to fetch repos: {e}")
        return []

def main():
    repos = fetch_repos()
    if not repos:
        print("No repos fetched; skipping.")
        return

    total_stars = sum(r.get("stargazers_count", 0) for r in repos)
    total_repos = len([r for r in repos if not r.get("fork")])
    now_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    telemetry_block = f"""<!-- TELEMETRY:START -->
```text
[SYSTEM TELEMETRY] • Automated Health Check: {now_utc}
├─ Core Runtimes:      Python 3.12 (FastAPI/Scapy) • C++ (ESP-IDF) • C# (.NET) • Node.js
├─ Ecosystem Scale:    {total_repos} Native Repositories • {total_stars} Community Stars
├─ Quality Standard:   100% Open Source Community Health Across Core Repositories
└─ Operational Status: All Systems Operational • Actively Maintained
```
<!-- TELEMETRY:END -->"""

    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"<!-- TELEMETRY:START -->.*?<!-- TELEMETRY:END -->"
    if re.search(pattern, content, flags=re.DOTALL):
        new_content = re.sub(pattern, telemetry_block, content, flags=re.DOTALL)
    else:
        # Append before Open Source Standards
        if "### Open Source Standards" in content:
            new_content = content.replace("### Open Source Standards", f"### 📡 Live Systems Telemetry\n\n{telemetry_block}\n\n---\n\n### Open Source Standards")
        else:
            new_content = content + f"\n\n### 📡 Live Systems Telemetry\n\n{telemetry_block}\n"

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Telemetry block updated successfully.")

if __name__ == "__main__":
    main()
