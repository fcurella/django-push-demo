django: gunicorn django_push_demo.wsgi:application -k socketio.sgunicorn.GeventSocketIOWorker -b 0.0.0.0:5000
nginx: nginx -c $PWD/config/nginx.conf
redis: redis-server $PWD/config/redis.conf
redis-monitor: sleep 2 && redis-cli MONITOR
