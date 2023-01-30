# ShortVideoCrawl

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
scrapy crawl kuaishou --query 蔡徐坤
```

videos are saved in `./videos`, named with video id
