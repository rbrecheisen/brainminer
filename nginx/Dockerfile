FROM gliderlabs/alpine:3.3

MAINTAINER Ralph Brecheisen <ralph.brecheisen@gmail.com>

ENV NGINX_VERSION nginx-1.10.1

RUN apk --update add openssl-dev pcre zlib pcre-dev zlib-dev wget curl build-base git vim bash \
    && mkdir -p /tmp/src \
	&& cd /tmp/src \
    && git clone http://luajit.org/git/luajit-2.0.git \
    && cd luajit-2.0 \
    && make \
    && make install \
    && cd .. \
	&& wget http://nginx.org/download/${NGINX_VERSION}.tar.gz \
	&& tar -zxvf ${NGINX_VERSION}.tar.gz \
    && git clone https://github.com/simpl/ngx_devel_kit.git \
    && git clone https://github.com/openresty/lua-nginx-module.git \
    && git clone https://github.com/pgaertig/nginx-big-upload.git \
	&& cd /tmp/src/${NGINX_VERSION} \
	&& ./configure \
		--with-http_ssl_module \
		--with-http_gzip_static_module \
		--with-http_auth_request_module \
		--prefix=/usr/local/nginx \
		--http-log-path=/var/log/nginx/access.log \
		--error-log-path=/var/log/nginx/error.log \
		--sbin-path=/usr/local/sbin/nginx \
        --add-module=../ngx_devel_kit \
        --add-module=../lua-nginx-module \
	&& make \
	&& make install \
	&& ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stderr /var/log/nginx/error.log \
	&& mkdir -p /mnt/shared/files \
    && mkdir -p /usr/local/nginx/modules \
	&& mv ../nginx-big-upload /usr/local/nginx/modules \
	&& apk del build-base openssl-dev pcre-dev zlib-dev wget git \
	&& rm -rf /tmp/src \
	&& rm -rf /var/cache/apk/*

EXPOSE 80 443

CMD ["nginx"]