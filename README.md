# ScrapyCrawler
## Description
自作のクローラーをコマンドラインを用いて起動するプログラム  
フレームワーク「Scrapy」に独自のロジックを加えました  

## Requirement
* pandas 1.3.1
* beautifulsoup4 4.9.3
* readability-lxml 0.8.1
* scrapy 2.4.1
* protego 0.1.16 

## Installation
- Pandas  
```pip install pandas```  
- protego  
```pip install protego```
- readability-lxml  
```pip install readability-lxml```
- Scrapy  
```pip install Scrapy```
- beautifulsoup4  
```pip install beautifulsoup4```



## Setup
1. 元データを「ScrapyCrawler/data/orign」にセットする  
- ファイル形式は「csv」 or 「excel」で以下のように設定してください。
- ヘッダーは任意の値で構いませんが列に対応する内容だけは遵守してください。  
- 元データを複数設定しても問題ないですが、ファイル名に重複がないようしてください。元データのファイル名に基づいて処理を行います。  

|列番号|ヘッダー|内容|備考|
|:---|:---|:---|:---|
|1|index|インデックス番号を記載してください|一意の値を設定すること|
|2|meta|その他の情報追加欄||
|3|url|urlを記載してください|ドメインに重複しないようにしてください|

2. テキストアンカーのリストを「ScrapyCrawler/data/txt」におく

- ファイル形式は「csv」で以下のように設定してください。
- txt列以外の列を追加しても処理に問題はありません
- 行番号の降順のテキストアンカーの方が優先して判断されます。

ファイル内容は以下のようにしてください
|列番号|ヘッダー|内容|備考|
|:---|:---|:---|:---|
|1|txt|テキストアンカーを記載してください|一意の値を設定すること|

3. パスのパターンリストを「ScrapyCrawler/data/path」におく

- ファイル形式は「csv」で以下のように設定してください。
- txt列以外の列を追加しても処理に問題はありません
- 行番号の降順のテキストアンカーの方が優先して判断されます。

ファイル内容は以下のようにしてください
|列番号|ヘッダー|内容|備考|
|:---|:---|:---|:---|
|1|path|パスのパターンを記載してください|一意の値を設定すること|

## Usage
サイトを複数階層辿る必要がある場合 
```python main.py -f```  

サイトの階層を辿る必要のない場合
```python main.py```  

## Note
