# Nginx 

```
openssl req -x509 -newkey rsa:4096 -sha256 -nodes -keyout pri.key -out pub.crt -subj "/CN=test.local.local" -days 5421


echo -n 'sammy:' >> /etc/nginx/.htpasswd
openssl passwd -apr1 >> /etc/nginx/.htpasswd





tree /usr/share/nginx/

|-- html
|   |-- 50x.html
|   `-- index.html
|-- notfound.html
|   `-- 404.html
`-- site1
    |-- about
    |   `-- about.html
    |-- images
    |   `-- index.html
    `-- index.html

6 directories, 6 files


curl http://IP:8080/ -u "sammy:sammy"

curl http://localhost:9090/var?apikey=1234

```


# This is a sample configuration for reverse proxy 
```
user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log notice;
pid        /var/run/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    limit_req_zone $request_uri zone=MYZONE:1m rate=50r/m;

    sendfile        on;
    #tcp_nopush     on;
    server_tokens off;
    keepalive_timeout  65;

    #gzip  on;

    include /etc/nginx/conf.d/*.conf;



    server {

        listen 80;
        server_name localhost;
        root /usr/share/nginx/site1;

        error_page 404 /notfound.html;

        location / {
                index NO_EXISTENT_INDEX;
                autoindex on;
        }


        location /about/ {
                index about.html;
        }

        location /images/ {
                index index.html;
                auth_basic "Restricted Content";
                auth_basic_user_file /etc/nginx/.htpasswd;
        }

        location /notfound.html {

                root /usr/share/nginx/;
                index 404.html;
        }
    }


    server {

        listen 8080 ssl;
        server_name test.local.local;
        ssl_certificate /etc/ssl/tls.crt;
        ssl_certificate_key /etc/ssl/tls.key;



        location / {

                proxy_pass http://IP:8000;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                auth_basic "Restricted Content";
                auth_basic_user_file /etc/nginx/.htpasswd;
                limit_req zone=MYZONE;
        }

    }


    server {

        listen 9090 ssl;
        server_name site2;
        ssl_certificate /etc/ssl/tls.crt;
        ssl_certificate_key /etc/ssl/tls.key;

        root /usr/share/nginx/site2;

        auth_basic "Restricted Content";
        auth_basic_user_file /etc/nginx/.htpasswd;

        set $weekend 'No';

        #if ( $arg_apikey != 1234 ) {
        #        return 401 "Incorect apikey";
        #}

        if ( $date_local ~ 'Saturday|Sunday' ) {
                        set $weekend 'Yes';
        }


        location / {
                root /usr/share/nginx/site2;
                index NO_EXISTENT_INDEX;
                autoindex on;

        }


        location /test {


        }

        location /var {

                return 200 "host is: $host\n uri is : $uri \n args is : $args \n weekend: $weekend \n $date_local";
        }


    }

}
```
