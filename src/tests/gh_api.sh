# Test Github API CodeQL with sarif upload
response=$(gh api \
  --method POST \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  /repos/pamelafox/pamelafox-site/code-scanning/sarifs \
  -f commit_sha='d9b327639e4e84337b9edd297a8cfb098bbfeefa' \
 -f ref='refs/heads/a11y' \
 -f sarif=$(gzip -c src/tests/axe_results.sarif | base64 -b 0))
url=$(echo $response | grep -o '"url": *"[^"]*"' | cut -d '"' -f 4)
gh api \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  $url
