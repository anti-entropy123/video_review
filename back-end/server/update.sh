cd '/home/ubuntu/yjn/video_review/'
git reset --hard origin/master
git clean -f
git pull
cd 'back-end/server/config'

sudo nginx -s stop
sudo nginx -c `pwd`/nginx.conf

echo 'build end' >> temp.txt