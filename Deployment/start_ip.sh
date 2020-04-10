sh bash/gunicorn.sh
echo "Gunicorn Configured"

sh bash/nginx.sh "$1"
echo "Nginx Configured"