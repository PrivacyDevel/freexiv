# freexiv - an alternative front-end for pixiv

## Installation

### Debian based systems
```
sudo -i
apt install --no-install-recommends git nginx-core python3-{bottle,waitress,requests}
useradd -ms /bin/bash freexiv
su - freexiv
git clone https://codeberg.org/PrivacyDev/freexiv
cp freexiv/config.py{.example,}
chmod 600 freexiv/config.py
exit
cp /home/freexiv/freexiv/nginx/freexiv /etc/nginx/sites-available/
ln -s /etc/nginx/sites-{available,enabled}/freexiv
cp /home/freexiv/freexiv/freexiv.service /etc/systemd/system/
chown root:root /etc/systemd/system/freexiv.service
```
Adjust the following files as needed:
- /home/freexiv/freexiv/config.py
- /etc/nginx/sites-available/freexiv
- /etc/systemd/system/freexiv.service

Add the following line inside of the http block in `/etc/nginx/nginx.conf`:

`proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_zone:10m max_size=5g use_temp_path=off;`

```
systemctl daemon-reload
systemctl enable --now freexiv
systemctl reload nginx
exit
```

## Update

```
sudo -i
su - freexiv
cd freexiv
git pull
exit
systemctl restart freexiv
exit
```

## Instances

### Clearnet
|Instance                                                 | Cloudflare | Notes             |
|---------------------------------------------------------|------------|-------------------|
|[freexiv.privacydev.net](https://freexiv.privacydev.net) | No         | official instance |

### Tor
|Instance                                                                                                                                                | Notes             |
|--------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
|[freexiv.g4c3eya4clenolymqbpgwz3q3tawoxw56yhzk4vugqrl6dtu3ejvhjid.onion](http://freexiv.g4c3eya4clenolymqbpgwz3q3tawoxw56yhzk4vugqrl6dtu3ejvhjid.onion) | official instance |

## Mirrors
[Codeberg](https://codeberg.org/PrivacyDev/freexiv), [GitHub](https://github.com/PrivacyDevel/freexiv)

## Donations
[Monero (XMR)](https://www.getmonero.org/): `83Ak3unX8ATdAQzWhKWzoDUUQRZX28NZN66r8CoEUEAZZsjxeEJxqfTdYjv6n7m7JkCGvHeKLQffQXNzobaJw4hEQw92rpP` \
[Bitcoin (BTC)](https://bitcoin.org/): `bc1qzmx0gemry0fgn8jcrwp9x00j7zs860hpjy3x9g`

