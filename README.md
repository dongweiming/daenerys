
## Getting started

```python
❯ git clone https://github.com/dongweiming/daenerys
❯ cd daenerys
❯ virtualenv venv
❯ source venv/bin/activate
❯ pip install -r requirements.txt
# 安装配置Redis和MongoDB
❯ cd demo
❯ python worker.py # 启动worker(默认5个进程)
❯ python beat.py  # 新开启一个终端，启动Beat服务生成任务
❯ ipython  # 发布一个需要获取执行结果的任务
In [1]: from messaging import sync_get

In [2]: sync_get('flask')
PUT flask
Out[2]:
{u'author': u'Armin Ronacher',
 u'download_url': u'https://pypi.python.org/packages/24/6e/11b9c57e46f276a8a8da85a2fa7ada62b0463b68693616c7ab5df356fa/Flask-0.12.1.tar.gz',
 u'name': u'flask',
 u'version': u'0.12.1'}
```
