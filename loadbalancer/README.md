# Nginx as a load Balancer
```

upstream backend {
	server 172.16.197.2:80;
	server 172.16.197.3:81;
}




server {
        listen 80;
        server_name qqq.net;
        location / {
                proxy_pass http://backend;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header Host $host;

        }

}

```

**One of the important capability of a LoadBalancer is the health checks of the backend servers** \
Two types of health checks supported by Nginx:
* Active Health-checks --> nginx plus
* Passive Health-checks --> nginx

In Passive Health Checks, Nginx monitors the communication between client and the upstream server.

If The upstream server is not responding or rejecting connections, the passive health checks will consider the server to be unhealthy.
```
upstream backend {
        least_conn; #forward request to a backend which has minimum active connection
        server 172.16.197.4:80 max_fails=2 fail_timeout=20s weight=2;
        server 172.16.197.4:81 weight=1;
}


server {
        listen 80;
        server_name qqq.net;
        location / {
                proxy_pass http://backend;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header Host $host;

        }

}

```
in active monitoring the server try to connect the backend server (5 second by default) if the backend server doesn't responsed, Nginx doesn't send any request to backend server.


**all worker processes in nginx use a shared memory, because they have to use the same information about the backend server**

```
upstream backend {
        server 172.16.197.4:80 max_fails=2 fail_timeout=20s;
        server 172.16.197.4:81;
        zone backend 64k
}

match server_test {
  status 200-399;
  body ~ healthz;
  }


server {
        listen 80;
        server_name qqq.net;
        location / {
                proxy_pass http://backend;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header Host $host;
                health_check interval=2 uri=/healthz match=server_test;

        }

}


```

# Load Balancing Algorithm
