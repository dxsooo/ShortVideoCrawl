# ShortVideoCrawl

[![GitHub](https://img.shields.io/github/license/dxsooo/ShortVideoCrawl)](./LICENSE)
[![CodeFactor](https://www.codefactor.io/repository/github/dxsooo/shortvideocrawl/badge)](https://www.codefactor.io/repository/github/dxsooo/shortvideocrawl)

Short video crawler based on [scrapy](https://github.com/scrapy/scrapy), currently supports:

- [kuaishou](https://www.kuaishou.com/)

## Usage

requirements:

- python 3.10
- poetry

### prepare

```bash
git clone https://github.com/dxsooo/ShortVideoCrawl
poetry install
poetry shell
```

### run

For example:

```bash
cd shortvideocrawl
# query: query word
# count: target video count
scrapy crawl kuaishou -a query='蔡徐坤' -a count=50
```

videos are saved in `./videos`, named with video id
