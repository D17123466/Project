sudo rm -r /home/ubuntu/Project/Demo
sudo rm -r /home/ubuntu/Project/Development

sudo apt-get update
sudo apt-get install -y docker.io docker-compose

sudo docker-compose build
sudo docker-compose up
