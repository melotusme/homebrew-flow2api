require_relative "../lib/private_release_download_strategy"

cask "flow2api" do
  version "0.3.1"
  sha256 "12fa75a05f3f6a27cb78bcd135e34780d02644867f4d4de0c62de8e494a01dfb"

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
