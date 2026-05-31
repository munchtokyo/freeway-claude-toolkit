# Freeway Claude Code Toolkit インストーラ (Windows PowerShell)
# 使い方: 管理者として実行された PowerShell で .\install.ps1

$ErrorActionPreference = "Stop"
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Freeway Claude Code Toolkit インストーラ (Windows)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

# 1. 前提ツールのチェック
Write-Host "[1/6] 前提ツールチェック..." -ForegroundColor Yellow

function Check-Command {
    param($cmd, $name, $installHint)
    if (Get-Command $cmd -ErrorAction SilentlyContinue) {
        Write-Host "  OK $name" -ForegroundColor Green
        return $true
    } else {
        Write-Host "  NG $name が見つかりません" -ForegroundColor Red
        Write-Host "     インストール: $installHint" -ForegroundColor Yellow
        return $false
    }
}

$nodeOk = Check-Command "node" "Node.js" "winget install OpenJS.NodeJS"
$npmOk  = Check-Command "npm"  "npm"     "Node.jsに同梱"
$gitOk  = Check-Command "git"  "Git"     "winget install Git.Git"

if (-not ($nodeOk -and $npmOk -and $gitOk)) {
    Write-Host ""
    Write-Host "前提ツールが揃ってません。上記コマンドでインストールしてから再実行してください。" -ForegroundColor Red
    exit 1
}

# 2. Claude Code 本体のインストール
Write-Host ""
Write-Host "[2/6] Claude Code 本体..." -ForegroundColor Yellow
if (-not (Get-Command "claude" -ErrorAction SilentlyContinue)) {
    Write-Host "  Claude Code をインストール中..."
    npm install -g "@anthropic-ai/claude-code"
} else {
    Write-Host "  OK Claude Code は既にインストール済み" -ForegroundColor Green
}

# 3. 設定ファイルのコピー
Write-Host ""
Write-Host "[3/6] 設定ファイルの配置..." -ForegroundColor Yellow
$claudeDir = "$env:USERPROFILE\.claude"
if (-not (Test-Path $claudeDir)) {
    New-Item -ItemType Directory -Path $claudeDir | Out-Null
}

# .mcp.json はプロジェクトディレクトリにコピー（リポ内のサンプルから）
$mcpExample = "$PSScriptRoot\mcp-config\claude-mcp.example.json"
$mcpTarget  = "$PSScriptRoot\.mcp.json"
if (-not (Test-Path $mcpTarget)) {
    Copy-Item $mcpExample $mcpTarget
    Write-Host "  作成: $mcpTarget" -ForegroundColor Green
    Write-Host "  ※ EXA_API_KEY や Google 認証情報を .env で設定してください" -ForegroundColor Yellow
}

# 4. .env テンプレ作成
Write-Host ""
Write-Host "[4/6] .env テンプレート作成..." -ForegroundColor Yellow
$envFile = "$PSScriptRoot\.env"
if (-not (Test-Path $envFile)) {
    @"
# Freeway Claude Code Toolkit 環境変数
# このファイルは絶対にコミットしないでください (.gitignore で除外済)

EXA_API_KEY=
FREEWAY_SHEETS_ID=
"@ | Out-File -FilePath $envFile -Encoding UTF8
    Write-Host "  作成: .env (空のテンプレート)" -ForegroundColor Green
} else {
    Write-Host "  既存の .env を残しました" -ForegroundColor Green
}

# 5. Playwright ブラウザのインストール
Write-Host ""
Write-Host "[5/7] Playwright ブラウザ..." -ForegroundColor Yellow
npx -y playwright install chromium

# 6. OS 層配置 (hooks/rules/skills/memory) を ~/.claude/ にコピー
Write-Host ""
Write-Host "[6/7] OS 層を ~/.claude/ に配置..." -ForegroundColor Yellow
$claudeHooks  = "$env:USERPROFILE\.claude\hooks"
$claudeRules  = "$env:USERPROFILE\.claude\rules"
$claudeSkills = "$env:USERPROFILE\.claude\skills"
$claudeMemory = "$env:USERPROFILE\.claude\memory"

New-Item -ItemType Directory -Force -Path $claudeHooks,$claudeRules,$claudeSkills,$claudeMemory | Out-Null

Copy-Item -Recurse -Force "$PSScriptRoot\hooks\*" $claudeHooks
Write-Host "  hooks 配置 (save-session / load-session / learning-observer / governance-capture など)" -ForegroundColor Green

Copy-Item -Recurse -Force "$PSScriptRoot\rules\*" $claudeRules
Write-Host "  rules 配置 (edit-policy / factcheck / no-dashes / safety / security-discipline / powerpoint-composition + Freeway 専用 2 本)" -ForegroundColor Green

Copy-Item -Recurse -Force "$PSScriptRoot\skills\*" $claudeSkills
Write-Host "  skills 配置 (skill-creator / self-improving-agent + Document Skills: pdf / docx / xlsx / pptx)" -ForegroundColor Green

if (-not (Test-Path "$claudeMemory\MEMORY.md")) {
    Copy-Item "$PSScriptRoot\memory\MEMORY.md.template" "$claudeMemory\MEMORY.md"
    Write-Host "  MEMORY.md 初期化" -ForegroundColor Green
}

# 7. 動作確認案内
Write-Host ""
Write-Host "[7/7] セットアップ完了" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "次のステップ:" -ForegroundColor Cyan
Write-Host "  1. .env に EXA_API_KEY と FREEWAY_SHEETS_ID を設定"
Write-Host "  2. Google サービスアカウント JSON を ~/.claude/freeway-google-credentials.json に配置"
Write-Host "  3. PowerShell を開き直して 'claude' で起動"
Write-Host "  4. 起動後 '/doctor' で動作確認"
Write-Host ""
Write-Host "困ったら docs\00_onboarding.md を読んでください。" -ForegroundColor Cyan
