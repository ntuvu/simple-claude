#!/usr/bin/env zsh

input=$(cat)
model=$(printf "%s" "$input" | jq -r '.model.display_name // .model.id // .model // "unknown"')
branch=$(git branch --show-current 2>/dev/null)
[ -z "$branch" ] && branch=$(git rev-parse --short HEAD 2>/dev/null)
context_left=$(printf "%s" "$input" | jq -r '
  (.context_window.remaining_percentage // .contextWindow.remainingPercentage // .context_window.remaining_percent // .context_window.remainingPercent // .context.remaining_percent // .context.remainingPercent // .contextRemainingPercent // .usage.context_window.remaining_percentage // .usage.contextWindow.remainingPercentage // .usage.context_window.remaining_percent // .usage.contextWindow.remainingPercent // empty) as $p
  | if $p != null and $p != "" then
      (if ($p|type) == "number" then
        (if $p <= 1 then (((($p * 100) | round) | tostring) + "%") else ((($p | round) | tostring) + "%") end)
      else $p end)
    else
      (.context_window.remaining_tokens // .contextWindow.remainingTokens // .context.remaining_tokens // .context.remainingTokens // .usage.context_window.remaining_tokens // .usage.contextWindow.remainingTokens // empty
      | if . == null or . == "" then empty else (tostring + " tok") end)
    end
')
[ -z "$context_left" ] && context_left="--"

print -P "%F{244}user:%f %n@%m"
print -P "%F{244}path:%f %~"
if [ -n "$branch" ]; then
  print -P "%F{244}git:%f ${branch}"
fi
print -P "%F{244}model:%f ${model}"
print -P "%F{244}context:%f ${context_left}"
