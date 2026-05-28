#!/usr/bin/env bash
# Freeway Claude Code Toolkit インストーラ (Mac / Linux)
# 使い方: ./install.sh

set -e

cyan='\033[1;36m'
yellow='\033[1;33m'
green='\033[1;32m'
red='\033[1;31m'
nc='\033[0m'

echo -e "${cyan}==========================================================${nc}"
echo -e "${cyan}  Freeway Claude Code Toolkit インストーラ (Mac/Linux)${nc}"
echo -e "${cyan}==========================================================${nc}"
echo ""

# 1. 前提ツール
echo -e "${yellow}[1/6] 前提ツールチェック...${nc}"
check_cmd() {
    if command -v "$1" >/dev/null 2>&1; then
        echo -e "  ${green}OK${nc} $2"
        return 0
    else
        echo -e "  ${red}NG${nc} $2 が見つかりません。${yellow}インストール: $3${nc}"
        return 1
    fi
}

ok=true
check_cmd node "Node.js" "brew install node または https://nodejs.org" || ok=false
check_cmd npm  "npm"     "Node.js に同梱" || ok=false
check_cmd git  "Git"     "brew install git" || ok=false

if [ "$ok" = false ]; then
    echo ""
    echo -e "${red}前提ツールが揃ってません。${nc}"
    exit 1
fi

# 2. Claude Code
echo ""
echo -e "${yellow}[2/6] Claude Code 本体...${nc}"
if ! command -v claude >/dev/null 2>&1; then
    npm install -g @anthropic-ai/claude-code
else
    echo -e "  ${green}OK${nc} 既にインストール済み"
fi

# 3. 設定ファイル
echo ""
echo -e "${yellow}[3/6] 設定ファイルの配置...${nc}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$HOME/.claude"

if [ ! -f "$SCRIPT_DIR/.mcp.json" ]; then
    cp "$SCRIPT_DIR/mcp-config/claude-mcp.example.json" "$SCRIPT_DIR/.mcp.json"
    echo -e "  ${green}作成: .mcp.json${nc}"
    echo -e "  ${yellow}※ EXA_API_KEY や Google 認証情報を .env で設定してください${nc}"
fi

# 4. .env テンプレ
echo ""
echo -e "${yellow}[4/6] .env テンプレート...${nc}"
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    cat > "$SCRIPT_DIR/.env" << 'EOF'
# Freeway Claude Code Toolkit 環境変数
# このファイルは絶対にコミットしないでください

EXA_API_KEY=
FREEWAY_SHEETS_ID=
EOF
    echo -e "  ${green}作成: .env${nc}"
else
    echo -e "  ${green}既存の .env を残しました${nc}"
fi

# 5. Playwright
echo ""
echo -e "${yellow}[5/6] Playwright ブラウザ...${nc}"
npx -y playwright install chromium

# 6. 完了
echo ""
echo -e "${green}[6/6] セットアップ完了${nc}"
echo -e "${cyan}==========================================================${nc}"
echo ""
echo -e "${cyan}次のステップ:${nc}"
echo "  1. .env に EXA_API_KEY と FREEWAY_SHEETS_ID を設定"
echo "  2. Google サービスアカウント JSON を ~/.claude/freeway-google-credentials.json に配置"
echo "  3. 新しいシェルを開いて 'claude' で起動"
echo "  4. 起動後 '/doctor' で動作確認"
echo ""
echo -e "${cyan}困ったら docs/00_onboarding.md を読んでください。${nc}"
