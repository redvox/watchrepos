#!/usr/bin/env bash
AHEAD=$(git rev-list --count origin/master..master)
BEHIND=$(git rev-list --count master..origin/master)
echo "${BEHIND}|${AHEAD}";