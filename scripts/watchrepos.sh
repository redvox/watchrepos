#!/usr/bin/env bash
SCRIPT_DIR=$(dirname $0)
C="\x1b[1m"
CO="\x1b[1m\x1b[38;5;208m"
CB="\x1b[1m\x1b[34m"
CR="\x1b[1m\x1b[31m"
CG="\x1b[1m\x1b[32m"
CY="\x1b[1m\x1b[93m"
CLB="\x1b[1m\x1b[94m"
CC="\x1b[0m"

TMP_DIRECTORY=/tmp/

while true; do
    for directory in ~/otto/* ; do
        if [ -d ${directory}/.git ]; then
            REPO_NAME=$(basename ${directory})
            cd ${directory};
            git fetch -q

            UPSTREAM=${1:-'@{u}'}
            LOCAL=$(git rev-parse @)
            REMOTE=$(git rev-parse "${UPSTREAM}")
            BASE=$(git merge-base @ "${UPSTREAM}")
            CHANGES=$(git diff-index --name-only HEAD -- | wc -l)
            UNTRACKED=$(git ls-files --others --exclude-standard | wc -l)

#            if ( [ "${LOCAL}" == "${REMOTE}" ] || [ "${CHANGES}" == "" ] ); then
#                continue
#            fi
            echo -en "${C}$REPO_NAME${CC} \t";
            if [ "${CHANGES}" != "0" ]; then
                echo -en "[${CR}dirty${CC} ${CHANGES}] "
            fi
            if [ "${UNTRACKED}" != "0" ]; then
                echo -en "[${CLB}untracked${CC} ${UNTRACKED}] "
            fi
            if [ ${LOCAL} = ${REMOTE} ]; then
                echo -en "${CG}Up-to-date${CC}"
            elif [ ${LOCAL} = ${BASE} ]; then
                echo -en "${CY}Need to pull${CC}"
            elif [ ${REMOTE} = ${BASE} ]; then
                echo -en "${CR}Need to push${CC}"
            else
                echo -en "${CR}Diverged${CC}"
            fi

            AHEAD=$(git rev-list --count origin/master..master)
            BEHIND=$(git rev-list --count master..origin/master)
            echo -e " ${CY}-${BEHIND}${CC}|${CG}+${AHEAD}${CC}";

            git status -s
        fi
    done
    sleep 60
done
