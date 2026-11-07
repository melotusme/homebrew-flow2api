# Flow2API Homebrew tap

通用 macOS 包，同时支持 Apple Silicon 和 Intel，最低 macOS 12。Windows x64 和 Linux x64 安装包在公开的 [melotusme/flow2api-releases](https://github.com/melotusme/flow2api-releases/releases/latest)。

```sh
brew tap melotusme/flow2api
brew install --cask melotusme/flow2api/flow2api
```

cask 固定版本并校验 SHA-256。macOS 使用 ad-hoc 签名，不是 Developer ID 公证。应用自带自动更新；也可以 `brew update` 后 `brew upgrade --cask melotusme/flow2api/flow2api`。

维护：发行仓库发布新版本后运行 `python3 scripts/update-cask.py`，核对 `Casks/flow2api.rb` 的版本、URL 和 SHA-256，再提交。

WebDAV 在每台电脑的设置里单独配置。可以导入本机 Clash Verge，或填写坚果云目录、账号和应用密码。密码留在系统凭据库。先在一台电脑上传，再在其他电脑下载。同步是手动的，不要两台同时上传。
