FROM nginx:1.22.1

WORKDIR /usr/share/nginx
RUN mkdir -p kuber_net && \
    mkdir -p kuber_com

COPY kuber_com/* kuber_com/
COPY kuber_net/* kuber_net/
COPY site.conf /etc/nginx/conf.d/
COPY nginx.conf /etc/nginx/nginx.conf


CMD ["/usr/sbin/nginx", "-g", "daemon off;"]