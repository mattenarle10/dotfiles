#!/bin/zsh

# Colors
BLUE='\033[1;34m'
YELLOW='\033[1;33m'
RESET='\033[0m'

# Banner
echo ""
printf "${BLUE}"
figlet -f chunky "MATT"
printf "${RESET}\n"

# Minimal welcome
printf "${YELLOW}Welcome back, Matt!${RESET}\n"
printf "Type ${BLUE}help${RESET} to see quick commands.\n"
echo ""

