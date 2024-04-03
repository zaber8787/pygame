echo Commit Message:
read commit
git init
git add .
git commit -m $commit
git branch -M main
git remote add origin https://github.com/zaber8787/pygame.git
git push -u origin main
read -p "Finished"