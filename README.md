# Wireguard Webconfig

**WARNING:** Do NOT expect this project to be secure! It was NOT reviewed, it MAY leak your WireGuard config file. Without HTTPS, your access credentials can be easily sniffed and your config file modified. Preferably allow access only over established VPN links. Proceed with caution! 

## Instalation

`pip` is expected to be Python3

```bash
pip install git+https://github.com/vakabus/wireguard-webconfig.git


cp /etc/wireguard/wg0.example.conf /etc/wireguard/wg0.conf

# edit configuration file /etc/wireguard/wg0.conf

systemctl enable wireguard-webconfig
systemctl start wireguard-webconfig

# Web interface should be running at http://127.0.0.1:51821/
```

## Source code

Everything is contained in file `webconfig.py`. Anything else is technically unnecessary. The code is quite messy, but it works. I might clean it up some day.