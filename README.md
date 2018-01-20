# spider-python-demo-movie
这是使用python,requests,windows平台来爬取电影网站，使用redis存图片的入门demo

https://github.com/MicrosoftArchive/redis/tags
windows下安装redis


python内置的是unicode,所以我们必须将获得的html代码，假设它是('gb2312')，那么我们要decode一下，HTML.decode('gb2312')将其按照gb2312的规则，解析成unicode，这样我们就能在python中看到了，如果我们想让他变成utf-8编码呢，那么我们就text.encode('utf-8')即可

所以说unicode是字符编码转换的中间层，我们利用unicode进行字符编码的转换
