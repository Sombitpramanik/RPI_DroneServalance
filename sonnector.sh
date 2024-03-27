
git config --global user.email "m.sombitpramanik@gmail.com"
git config --global user.name "Sombit Pramanik"
echo "# RPI_DroneServalance" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/Sombitpramanik/RPI_DroneServalance.git
git push -u origin main