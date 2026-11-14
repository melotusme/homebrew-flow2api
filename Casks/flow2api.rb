cask "flow2api" do
  version "0.3.7"
  sha256 "9465eec1c9d7541408551db023e2d2e215554994ed9223e2004a4f933acee2e0"

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
