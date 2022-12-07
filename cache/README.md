```
server {
        listen 80;
        server_name site.example.com;

        location / {
                root /usr/share/nginx/site;
                index  index.html;
        }

        location ~ \.(png) {
                root /usr/share/nginx/site;
                add_header Cache-Control no-store;
        }

}
```