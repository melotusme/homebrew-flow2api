#!/usr/bin/env python3
"""Regenerate the pinned cask from a published private release. Refuses drafts."""
import json
import subprocess
import tempfile
from pathlib import Path

repo = "melotusme/flow2api-releases"
asset = "Flow2API.app.tar.gz"
release = json.loads(subprocess.check_output(
    ["gh", "release", "view", "--repo", repo, "--json", "tagName,isDraft"],
))
if release["isDraft"]:
    raise SystemExit("正式 Release 还不存在，不写入 cask")
tag = release["tagName"]
with tempfile.TemporaryDirectory() as tmp:
    subprocess.run(
        ["gh", "release", "download", tag, "--repo", repo, "--pattern", "SHA256SUMS", "--dir", tmp],
        check=True,
    )
    sums = {}
    for line in (Path(tmp) / "SHA256SUMS").read_text().splitlines():
        digest, name = line.split(None, 1)
        sums[name.strip().lstrip("*")] = digest.strip()
missing = [name for name in (asset, "Flow2API.windows.x64.exe") if name not in sums]
if missing:
    raise SystemExit("SHA256SUMS 缺少 " + "、".join(missing))
sha = sums[asset]
if sha == sums["Flow2API.windows.x64.exe"]:
    raise SystemExit("macOS 与 Windows 校验值相同，拒绝写入 cask")
assert len(sha) == 64 and all(c in "0123456789abcdef" for c in sha)
version = tag.removeprefix("v")
assert version and all(c in "0123456789." for c in version)
text = '''require_relative "../lib/private_release_download_strategy"

cask "flow2api" do
  version "VERSION"
  sha256 "SHA"

  url "https://github.com/melotusme/flow2api-releases/releases/download/v#{version}/Flow2API.app.tar.gz",
      using: Flow2apiPrivateDownloadStrategy
  name "Flow2API"
  desc "Local Flow API desktop app with manual WebDAV preference sync"
  homepage "https://github.com/TheSmallHanCat/flow2api"

  depends_on macos: :monterey
  depends_on formula: "gh"

  auto_updates true

  app "Flow2API.app"

  caveats do
    <<~EOS
      需要已登录、且能读取 melotusme/flow2api-releases 的 GitHub CLI。
      这是通用 macOS 包，支持 Apple Silicon 和 Intel。Windows 不在这个 cask 里。
      应用是 ad-hoc 签名，没有 Apple 公证。
      WebDAV 在每台电脑的设置里单独配置，密码留在系统凭据库。
    EOS
  end
end
'''.replace("VERSION", version).replace("SHA", sha)
destination = Path(__file__).resolve().parents[1] / "Casks" / "flow2api.rb"
destination.parent.mkdir(exist_ok=True)
destination.write_text(text)
print("Updated cask", version)
