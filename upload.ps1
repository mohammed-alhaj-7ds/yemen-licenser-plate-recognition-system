# ================== CONFIG ==================
$GITHUB_USER = "mohammed-alhaj-7ds"
$REPO_NAME   = "yemen-licenser-plate-recognition-system"
$REPO_URL    = "https://github.com/$GITHUB_USER/$REPO_NAME.git"
$BRANCH      = "main"
$COMMIT_MSG  = "upload project files"
# ============================================

function Abort($msg) {
    Write-Host "ERROR: $msg"
    exit 1
}

Write-Host "Checking git installation..."
git --version
if ($LASTEXITCODE -ne 0) { Abort "Git is not installed." }

Write-Host "Checking git identity..."
$uname  = git config --global user.name
$uemail = git config --global user.email

if (-not $uname -or -not $uemail) {
    Write-Host "Setting git identity..."
    git config --global user.name "Mohammed Alhaj"
    git config --global user.email "malborwa@gmail.com"
}

Write-Host "Initializing repository..."
if (-not (Test-Path ".git")) {
    git init
    if ($LASTEXITCODE -ne 0) { Abort "git init failed" }
}

Write-Host "Adding files..."
git add .
if ($LASTEXITCODE -ne 0) { Abort "git add failed" }

Write-Host "Committing..."
git commit -m $COMMIT_MSG
if ($LASTEXITCODE -ne 0) {
    Write-Host "Nothing to commit, continuing..."
}

Write-Host "Setting branch..."
git branch -M $BRANCH
if ($LASTEXITCODE -ne 0) { Abort "branch failed" }

Write-Host "Setting remote..."
git remote remove origin 2>$null
git remote add origin $REPO_URL
if ($LASTEXITCODE -ne 0) { Abort "remote failed" }

Write-Host "Pushing to GitHub..."
git push -u origin $BRANCH
if ($LASTEXITCODE -ne 0) { Abort "push failed" }

Write-Host ""
Write-Host "SUCCESS: Project uploaded to GitHub"
Write-Host "https://github.com/$GITHUB_USER/$REPO_NAME"
