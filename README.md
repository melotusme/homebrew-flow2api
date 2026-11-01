# Flow2API private Homebrew tap

通用 macOS 包同时支持 Apple Silicon 和 Intel，最低 macOS 12。Windows x64 不在这个 tap 里，安装包是私有 [melotusme/flow2api-releases](https://github.com/melotusme/flow2api-releases) 的 `Flow2API.windows.x64.exe`。不要把这个仓库改成公开。

当前还没有 cask。第一次两个平台都正式发布之后，在这个仓库执行：

```sh
python3 scripts/update-cask.py
```

核对生成的 `Casks/flow2api.rb`，确认版本、URL 和 SHA-256 来自正式 Release，再提交。在那之前下面的安装命令会找不到 cask。

```sh
brew install gh
gh auth login
gh auth setup-git
brew tap melotusme/flow2api https://github.com/melotusme/homebrew-flow2api.git
brew trust --cask melotusme/flow2api/flow2api
brew install --cask melotusme/flow2api/flow2api
```

GitHub 账号必须能读取这个 tap 和 `flow2api-releases`。下载走本机 `gh`，令牌不进入 URL、cask 或参数。cask 固定版本并校验 SHA-256。macOS 使用 ad-hoc 签名，不是 Developer ID 公证。

更新已安装的 cask：`brew update`，然后 `brew upgrade --cask melotusme/flow2api/flow2api`。

WebDAV 在每台电脑的设置里单独配置。可以导入本机 Clash Verge，或填写坚果云目录、账号和应用密码。密码留在系统凭据库。先在一台电脑上传，再在其他电脑下载。同步是手动的，不要两台同时上传。
