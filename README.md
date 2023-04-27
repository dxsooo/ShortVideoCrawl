# ShortVideoCrawl

[![GitHub](https://img.shields.io/github/license/dxsooo/ShortVideoCrawl)](./LICENSE)
[![CodeFactor](https://www.codefactor.io/repository/github/dxsooo/shortvideocrawl/badge)](https://www.codefactor.io/repository/github/dxsooo/shortvideocrawl)

Short video crawler based on [scrapy](https://github.com/scrapy/scrapy), crawling with search query. 

Supports:

|Site|Name|Status|
|-|-|-|
|<img src="https://static.yximgs.com/udata/pkg/frontend-explore/material-lib-www/word-logo-1-min.png" height=40 />| [kuaishou](https://www.kuaishou.com/)| :heavy_check_mark: |
|<img src="https://pic.rmb.bdstatic.com/baidu-rmb-video-cover-1/2022-2/1645100826352/418a3aceca30.png" height=40 />|[haokan](https://haokan.baidu.com/)| :heavy_check_mark: |
|<img src="https://quanmin.baidu.com/web/publish/static/logo-du.9f546c46.png" height=40 />|quanmin| :clipboard: |
<!-- |梨视频|pearvideo| :clipboard: | -->
<!-- | m3u8 格式<img src="https://a.msstatic.com/huya/main3/static/img/logo.png" height=40 />|huya| :clipboard: | -->

## Usage

requirements:

- python 3.10+
- poetry

### prepare

```bash
git clone https://github.com/dxsooo/ShortVideoCrawl
poetry install --only main
poetry shell
```

### run

For example:

```bash
cd shortvideocrawl

# main parameters:
#   query: query word
#   count: target video count

# kuaishou
scrapy crawl kuaishou -a query='蔡徐坤' -a count=50

# haokan, with highest resolution
scrapy crawl haokan -a query='蔡徐坤' -a count=50
```

videos are saved in `./videos`, named with video id of source.
