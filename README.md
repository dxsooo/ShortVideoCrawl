# ShortVideoCrawl

[![GitHub](https://img.shields.io/github/license/dxsooo/ShortVideoCrawl)](./LICENSE)
[![CodeFactor](https://www.codefactor.io/repository/github/dxsooo/shortvideocrawl/badge)](https://www.codefactor.io/repository/github/dxsooo/shortvideocrawl)

Short video crawler based on [scrapy](https://github.com/scrapy/scrapy), crawling with search query.

Supports:

|Site|Name|Status|
|-|-|-|
|<img src="https://static.yximgs.com/udata/pkg/frontend-explore/material-lib-www/word-logo-1-min.png" height=40 />| [kuaishou](https://www.kuaishou.com/)| :heavy_check_mark:(not stable) |
|<img src="https://lf3-cdn-tos.bdxiguastatic.com/obj/ixigua-static/xigua_fe/xigua_video_web_pc/static/media/logo.6aae7c46.svg" height=40 />| [ixigua](https://www.ixigua.com/)| :heavy_check_mark:(not stable) |
|<img src="https://pic.rmb.bdstatic.com/baidu-rmb-video-cover-1/2022-2/1645100826352/418a3aceca30.png" height=40 />|[haokan](https://haokan.baidu.com/)| :construction: |
|<img src="https://quanmin.baidu.com/web/publish/static/logo-du.9f546c46.png" height=40 />|[quanmin](https://quanmin.baidu.com)| :heavy_check_mark: |
<!-- |梨视频|pearvideo| :clipboard: | -->
<!-- | m3u8 格式<img src="https://a.msstatic.com/huya/main3/static/img/logo.png" height=40 />|huya| :clipboard: | -->

> not stable: means mostly it works but sometime fails, retry may help

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

# xigua, with highest resolution and size smaller than 16MB, duration smaller than 5 min
scrapy crawl ixigua -a query='蔡徐坤' -a count=50

# haokan, with highest resolution
scrapy crawl haokan -a query='蔡徐坤' -a count=50

# quanmin
scrapy crawl quanmin -a query='蔡徐坤' -a count=50
```

videos are saved in `./videos`, named with video id of source platform.
