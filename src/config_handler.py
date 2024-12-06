import logging
import os

def create_new_config(route: str, host: str, port: str) -> str:
    conf = (
    """
location /{route} {
    rewrite ^/{route}/?$ /$1/ break;  # Ezt adjuk hozzá
    proxy_pass http://{host}:{port};
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
    """
            .replace("{route}", route)
            .replace("{host}", host)
            .replace("{port}", port))

    with open(f"/etc/nginx/conf.d/{host}.conf","w") as file:
        file.write(conf)
        logging.info(f"Configuration file created: /etc/nginx/conf.d/{host}.conf")

    return conf

def delete_config(host: str):
    logging.info(f"Deleting /etc/nginx/conf.d/{host}.conf")
    os.remove(f"/etc/nginx/conf.d/{host}.conf")