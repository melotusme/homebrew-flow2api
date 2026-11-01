# frozen_string_literal: true
require "download_strategy"

# Uses the user's gh session. Credentials never appear in the URL or argv.
class Flow2apiPrivateDownloadStrategy < AbstractFileDownloadStrategy
  def fetch(timeout: nil)
    gh = [HOMEBREW_PREFIX/"bin/gh", Pathname.new("/opt/homebrew/bin/gh"), Pathname.new("/usr/local/bin/gh")].find(&:executable?)
    raise "Install GitHub CLI and run gh auth login first" unless gh
    match = url.match(%r{\Ahttps://github\.com/melotusme/flow2api-releases/releases/download/(v[0-9.]+)/([^/]+)\z})
    raise "Unexpected private release URL" unless match
    lock = DownloadLock.new(temporary_path)
    begin
      lock.lock_or_wait
      unless cached_location.exist?
        cached_location.dirname.mkpath
        system_command! gh, args: ["release", "download", match[1], "--repo", "melotusme/flow2api-releases", "--pattern", URI.decode_www_form_component(match[2]), "--output", temporary_path.to_s, "--clobber"]
        temporary_path.rename(cached_location)
      end
      create_symlink_to_cached_download(cached_location)
    ensure
      lock.unlock(unlink: true)
    end
  end
end
