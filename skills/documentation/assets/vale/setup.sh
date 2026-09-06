#!/usr/bin/env bash
set -euo pipefail
shopt -s inherit_errexit

download_and_verify() {
    local release_url="$1"
    local archive_file="$2"
    local expected_digest="$3"
    curl --fail --location --silent --show-error "$release_url" --output "$archive_file"
    printf '%s  %s\n' "$expected_digest" "$archive_file" | sha256sum --check --status
}

install_vale() {
    local assets_directory="$1"
    local download_directory="$2"
    download_and_verify \
        https://github.com/vale-cli/vale/releases/download/v3.20.0/vale_3.20.0_Linux_64-bit.tar.gz \
        "$download_directory/vale.tar.gz" \
        f59e7030c5d4ace6cf915497d0d076a1699d61e876142765963237e6867c9712
    download_and_verify \
        https://github.com/errata-ai/Google/releases/download/v0.7.1/Google.zip \
        "$download_directory/Google.zip" \
        4b67fca1f2a88595b2a578ab98bbf3017a23af677b04f93e862843f3ea1a9a0b
    mkdir -p "$assets_directory/bin" "$assets_directory/styles"
    tar -xzf "$download_directory/vale.tar.gz" -C "$assets_directory/bin" vale LICENSE README.md
    unzip -oq "$download_directory/Google.zip" -d "$assets_directory/styles"
    "$assets_directory/bin/vale" --version
}

main() {
    if [[ "$(uname -s)" != Linux || "$(uname -m)" != x86_64 ]]; then
        printf '%s\n' 'This setup supports Linux x86_64; use the matching official Vale 3.20.0 release for other platforms.' >&2
        return 2
    fi
    local assets_directory
    assets_directory="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
    local download_directory
    download_directory="$(mktemp -d)"
    trap 'rm -rf -- "$download_directory"' EXIT
    install_vale "$assets_directory" "$download_directory"
    rm -rf -- "$download_directory"
    trap - EXIT
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
    main "$@"
fi
