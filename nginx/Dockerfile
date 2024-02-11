FROM nginx:1.23.3-alpine

RUN rm /etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/
COPY ./headman_bot.crt /etc/nginx
COPY ./headman_bot.key /etc/nginx

CMD ["nginx", "-g", "daemon off;"]
