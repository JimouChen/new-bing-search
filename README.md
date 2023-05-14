# new-bing-search

<div align="center">
  <img width="417" alt="image" src="https://github.com/JimouChen/new-bing-search/assets/63119239/451014a7-57d6-4750-b010-8639779d44bf">

<a>English</a> -
<a href="https://github.com/JimouChen/new-bing-search/blob/main/README_CN.md">简体中文</a>
</div>

- Use the New Bing counterattack cracking library interface to encapsulate the api, which is convenient for reading questions from files and searching for answers
- The question can be multiple questions placed in the file to read, or it can be a question to directly call the api

## Environment description
- Install third-party libraries
> Requires `python3.8+`

```bash
pip3 install -r requirements.txt
```

## How to get cookies.json
- Install the cookies plugin, as shown in the figure below
- Export the json format, and then paste it in the cookies.json file 
<img width="1156" alt="image" src="https://github.com/JimouChen/new-bing-search/assets/63119239/b14779d7-40ef-4f82-88d6-17d29f59c2f8">

## Prompt format
### Use excel format
- The column name is Q, which can be defined by yourself and modified in the code 
<img width="567" alt="image" src="https://github.com/JimouChen/new-bing-search/assets/63119239/d1d9d4aa-b534-49e6-8d85-64578fefcbfa">

### Use json format
- If it is a json format prompt, you can directly refer to the answer folder under the answer.json file format

## Reference
[EdgeGPT counterattack cracking library](https://github.com/acheong08/EdgeGPT)
