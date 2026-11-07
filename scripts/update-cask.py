#!/usr/bin/env python3
"""Regenerate the pinned cask from the latest public release. Refuses drafts and prereleases."""
import json
import urllib.request
from pathlib import Path

REPO = "melotusme/flow2api-releases"
ASSET = "Flow2API.app.tar.gz"
OTHER = "Flow2API.windows.x64.exe"  # a different platform's package; its checksum must differ
CASK = "flow2api"
TEMPLATE = '''cask "flow2api" do
  version "VERSION"
  sha256 "SHA"

  url "https://github.com/melotusme/flow2api-releases/releases/download/v#{version}/Flow2API.app.tar.gz"
  name "Flow2API"
  desc "Local Flow API desktop app with manual WebDAV preference sync"
  homepage "https://github.com/melotusme/flow2api"

  depends_on macos: :monterey

  auto_updates true

  app "Flow2API.app"

  caveats do
    <<~EOS
      这是通用 macOS 包，支持 Apple Silicon 和 Intel。Windows 不在这个 cask 里。
      应用是 ad-hoc 签名，没有 Apple 公证。
      WebDAV 在每台电脑的设置里单独配置，密码留在系统凭据库。
    EOS
  end
end
'''


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "homebrew-tap-update", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


release = json.loads(fetch(f"https://api.github.com/repos/{REPO}/releases/latest"))
if release.get("draft") or release.get("prerelease"):
    raise SystemExit("最新 Release 不是正式版，不写入 cask")
tag = release["tag_name"]
sums_url = next((a["browser_download_url"] for a in release["assets"] if a["name"] == "SHA256SUMS"), None)
if not sums_url or not sums_url.startswith(f"https://github.com/{REPO}/releases/download/{tag}/"):
    raise SystemExit("Release 缺少 SHA256SUMS")
sums = {}
for line in fetch(sums_url).decode().splitlines():
    digest, name = line.split(None, 1)
    sums[name.strip().lstrip("*")] = digest.strip()
missing = [name for name in (ASSET, OTHER) if name not in sums]
if missing:
    raise SystemExit("SHA256SUMS 缺少 " + "、".join(missing))
sha = sums[ASSET]
if sha == sums[OTHER]:
    raise SystemExit("不同平台的校验值相同，拒绝写入 cask")
assert len(sha) == 64 and all(c in "0123456789abcdef" for c in sha)
version = tag.removeprefix("v")
assert version and all(c in "0123456789." for c in version)
destination = Path(__file__).resolve().parents[1] / "Casks" / f"{CASK}.rb"
destination.parent.mkdir(exist_ok=True)
destination.write_text(TEMPLATE.replace("VERSION", version).replace("SHA", sha))
print("Updated cask", version, sha)
