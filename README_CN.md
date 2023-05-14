# new-bing-search
<div align="center">
  <img width="417" alt="image" src="https://github.com/JimouChen/new-bing-search/assets/63119239/451014a7-57d6-4750-b010-8639779d44bf">

<a>简体中文</a> -
<a href="https://github.com/JimouChen/new-bing-search/blob/main/README.md">English</a>
</div>

- 使用New Bing的逆袭破解库接口封装api，便于从文件中读取问题，进行搜索回答
- 问题可以是多个问题放在文件中读取，也可使一个问题直接调api

## 环境说明
- 安装第三方库
> 要求python3.8 +

```bash
pip3 install -r requirements.txt
```

### cookies.json的获取
- 安装`cookies`插件，用法如下图
- 导出`json`格式的即可，然后黏贴在`cookies.json`文件
<img width="1156" alt="image" src="https://github.com/JimouChen/new-bing-search/assets/63119239/b14779d7-40ef-4f82-88d6-17d29f59c2f8">


## prompt格式
- 用`excel`格式
  - 列名为`Q`，可自己定义，在代码中修改即可
<img width="567" alt="image" src="https://github.com/JimouChen/new-bing-search/assets/63119239/d1d9d4aa-b534-49e6-8d85-64578fefcbfa">

- 用`json`格式
  - 如是`json`格式的`prompt`，可直接参考`answer`文件夹下的`answer.json`文件格式

## 参考
- [EdgeGPT逆袭破解库](https://github.com/acheong08/EdgeGPT)
