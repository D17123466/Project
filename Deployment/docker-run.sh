sudo apt-get update
sudo apt-get install -y docker.io

# cd /home/ubuntu/Project/Deployment
docker-compose build
docker-compose up