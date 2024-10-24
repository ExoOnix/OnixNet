# OnixNet
<div align="center">
  <a href="https://github.com/ExoOnix/OnixNet">
    <img src="https://img.shields.io/github/stars/ExoOnix/OnixNet?style=for-the-badge" alt="GitHub stars" />
  </a>
  <a href="https://github.com/ExoOnix/OnixNet/fork">
    <img src="https://img.shields.io/github/forks/ExoOnix/OnixNet?style=for-the-badge" alt="GitHub forks" />
  </a>
  <a href="https://github.com/ExoOnix/OnixNet/issues">
    <img src="https://img.shields.io/github/issues/ExoOnix/OnixNet?style=for-the-badge" alt="GitHub issues" />
  </a>
<a href="https://opensource.org/license/mit">
  <img src="https://img.shields.io/badge/license-MIT-lightgrey.svg?style=for-the-badge" alt="MIT License" />
</
</div>




## Running

```
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt

cd OnixNet
python3 manage.py migrate
python3 manage.py runserver
```

Make sure to add OnixNet/media as a destination to your server configuration

