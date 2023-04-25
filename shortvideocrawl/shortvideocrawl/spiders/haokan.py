import json

import scrapy
from urllib.parse import urlencode, quote
from ..items import ShortvideocrawlItem

SEARCH_API = "https://haokan.baidu.com/haokan/ui-search/pc/search/video"
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "*/*",
    "Sec-Fetch-Site": "same-origin",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Sec-Fetch-Mode": "cors",
    "Cache-Control": "no-cache",
    "Host": "haokan.baidu.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4.1 Safari/605.1.15",
    "Referer": "https://haokan.baidu.com/web/search/page?query=%E8%94%A1%E5%BE%90%E5%9D%A4",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
}

cookies = {
    "RT": '"z=1&dm=baidu.com&si=b1e3eebf-bc17-4ba8-80c4-981450a88da7&ss=lgupdtuj&sl=3&tt=1pb&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=1rak&ul=cind&hd=cipz"',
    "ariaDefaultTheme": "undefined",
    "Hm_lpvt_4aadd610dfd2f5972f1efee2653a2bc5": "1682332626",
    "Hm_lvt_4aadd610dfd2f5972f1efee2653a2bc5": "1682332585",
    "hkpcSearch": "%u8521%u5F90%u5764",
    "ab_sr": "1.0.1_NGJmMjMyNzg2YWZjMDQ2YzhmZGM4MGI3YjMxZDgzNWIyNzU1NTFjNWY3NTM4MDkzNTdiNDkyZWQ2MzJmNDJmYzFiM2M0NDQ1MGExNmZjZTMyZTg5MmE3MGJkNDVjZDc5NGQ4ZjBmNzMxYTIxMzlkZTVkOGJmZWQ2YjJmNDIyNzc3OWNjNjQ0ODIzM2M0NWNmMjBjODMzOTE0OGMyZDI5Mg==",
    "reptileData": "%7B%22data%22%3A%2207365175041eb5a237beae3fe59b0a8611b6c16a31f5fbb2caa721fa9bc1f08467a1330751f52ccd88684810a3e551c34507d070bdd750eeea2ffc0c70d4d9a718f2fcd92e58052565c79aa7ef94a71a29bce541848099f2c48d26e361d97e12%22%2C%22key_id%22%3A%2230%22%2C%22sign%22%3A%22253b5d4c%22%7D",
    "ZFY": "OH1XubtMO4gg4WiLnLXhu2DDldqY6bdQGEFwTst4XLw:C",
    "BAIDUID": "47480F23FB5D94E35D7D21F63797455F:FG=1",
    "BIDUPSID": "AE72DD69FA755190B5172FD5C667F888",
    "PSTM": "1638979955",
}


class HaokanSpider(scrapy.Spider):
    name = "haokan"
    allowed_domains = ["haokan.baidu.com"]

    query = "蔡徐坤"
    count = 30

    def start_requests(self):
        yield self.request(1)

    def request(self, page: int):
        st = 1682411075882
        s = sign(page, self.query, st)
        # print(s)

        query = {
            "pn": page,
            "rn": 10,
            "type": "video",
            "query": self.query,
            # "sign": "9cb60910441a1e1afde1e4d73de14a45",
            "sign": s,
            "version": 1,
            "timestamp": st,
        }
        return scrapy.Request(
            SEARCH_API + "?" + urlencode(query),
            meta={"page": page},
            headers=headers,
            cookies=cookies,
        )

    def parse(self, response):
        resp = json.loads(response.body)
        # print(resp)
        data = resp["data"]

        if "list" in data:
            for l in data["list"]:
                print(l["vid"])

            if data["has_more"] != 0:
                # not enough, theoretically 10 per page
                if response.meta["page"] * 10 < self.count:
                    yield self.request(response.meta["page"] + 1)
        # else:
        #     print(data)


# following funs are translated from search.c9e205.chunk.js
def sign(o, i, l) -> str:
    s = "_".join([str(o), quote(i), "10", str(l), "1"])
    u = p(m(s))
    return u


def p(e):
    n = ""
    for c in range(0, len(e)):
        t = ord(e[c])
        n += (
            "0123456789abcdef"[(unsigned_right_shift(t, 4) & 0xFFFFFFFF) & 15]
            + "0123456789abcdef"[15 & t]
        )
    return n


def m(e):
    return v(h(f(e), 8 * len(e)))


def v(e):
    c = ""
    n = 32 * len(e)
    for t in range(0, n, 8):
        c += chr((unsigned_right_shift(e[t >> 5], t % 32) & 0xFFFFFFFF) & 255)
    return c


def h(e, t):
    f1 = t >> 5
    if f1 >= len(e):
        e.extend([0] * (f1 - len(e) + 1))
    e[f1] = 128 << t % 32
    f2 = 14 + ((unsigned_right_shift(t + 64, 9) & 0xFFFFFFFF) << 4)
    if f2 >= len(e):
        e.extend([0] * (f2 - len(e) + 1))
    e[f2] = t
    if len(e) < 16:
        e.extend([0] * (16 - len(e)))
    v = 1732584193
    f = -271733879
    p = -1732584194
    d = 271733878
    for c in range(0, len(e), 16):
        n = v
        r = f
        i = p
        h = d
        v = a(v, f, p, d, e[c], 7, -680876936)
        # print("v:", v)
        d = a(d, v, f, p, e[c + 1], 12, -389564586)
        # print("d:", d)
        p = a(p, d, v, f, e[c + 2], 17, 606105819)
        # print("p:", p)
        f = a(f, p, d, v, e[c + 3], 22, -1044525330)
        # print("f:", f)
        v = a(v, f, p, d, e[c + 4], 7, -176418897)
        # print("v:", v)
        d = a(d, v, f, p, e[c + 5], 12, 1200080426)
        # print("d:", d)
        p = a(p, d, v, f, e[c + 6], 17, -1473231341)
        # print("p:", p)
        f = a(f, p, d, v, e[c + 7], 22, -45705983)
        # print("f:", f)
        v = a(v, f, p, d, e[c + 8], 7, 1770035416)
        d = a(d, v, f, p, e[c + 9], 12, -1958414417)
        p = a(p, d, v, f, e[c + 10], 17, -42063)
        f = a(f, p, d, v, e[c + 11], 22, -1990404162)
        v = a(v, f, p, d, e[c + 12], 7, 1804603682)
        d = a(d, v, f, p, e[c + 13], 12, -40341101)
        p = a(p, d, v, f, e[c + 14], 17, -1502002290)
        f = a(f, p, d, v, e[c + 15], 22, 1236535329)
        v = l(v, f, p, d, e[c + 1], 5, -165796510)
        d = l(d, v, f, p, e[c + 6], 9, -1069501632)
        p = l(p, d, v, f, e[c + 11], 14, 643717713)
        f = l(f, p, d, v, e[c], 20, -373897302)
        v = l(v, f, p, d, e[c + 5], 5, -701558691)
        d = l(d, v, f, p, e[c + 10], 9, 38016083)
        p = l(p, d, v, f, e[c + 15], 14, -660478335)
        f = l(f, p, d, v, e[c + 4], 20, -405537848)
        v = l(v, f, p, d, e[c + 9], 5, 568446438)
        d = l(d, v, f, p, e[c + 14], 9, -1019803690)
        p = l(p, d, v, f, e[c + 3], 14, -187363961)
        f = l(f, p, d, v, e[c + 8], 20, 1163531501)
        v = l(v, f, p, d, e[c + 13], 5, -1444681467)
        d = l(d, v, f, p, e[c + 2], 9, -51403784)
        p = l(p, d, v, f, e[c + 7], 14, 1735328473)
        f = l(f, p, d, v, e[c + 12], 20, -1926607734)
        v = s(v, f, p, d, e[c + 5], 4, -378558)
        d = s(d, v, f, p, e[c + 8], 11, -2022574463)
        p = s(p, d, v, f, e[c + 11], 16, 1839030562)
        f = s(f, p, d, v, e[c + 14], 23, -35309556)
        v = s(v, f, p, d, e[c + 1], 4, -1530992060)
        d = s(d, v, f, p, e[c + 4], 11, 1272893353)
        p = s(p, d, v, f, e[c + 7], 16, -155497632)
        f = s(f, p, d, v, e[c + 10], 23, -1094730640)
        v = s(v, f, p, d, e[c + 13], 4, 681279174)
        d = s(d, v, f, p, e[c], 11, -358537222)
        p = s(p, d, v, f, e[c + 3], 16, -722521979)
        f = s(f, p, d, v, e[c + 6], 23, 76029189)
        v = s(v, f, p, d, e[c + 9], 4, -640364487)
        d = s(d, v, f, p, e[c + 12], 11, -421815835)
        p = s(p, d, v, f, e[c + 15], 16, 530742520)
        f = s(f, p, d, v, e[c + 2], 23, -995338651)
        v = u(v, f, p, d, e[c], 6, -198630844)
        d = u(d, v, f, p, e[c + 7], 10, 1126891415)
        p = u(p, d, v, f, e[c + 14], 15, -1416354905)
        f = u(f, p, d, v, e[c + 5], 21, -57434055)
        v = u(v, f, p, d, e[c + 12], 6, 1700485571)
        d = u(d, v, f, p, e[c + 3], 10, -1894986606)
        p = u(p, d, v, f, e[c + 10], 15, -1051523)
        f = u(f, p, d, v, e[c + 1], 21, -2054922799)
        v = u(v, f, p, d, e[c + 8], 6, 1873313359)
        d = u(d, v, f, p, e[c + 15], 10, -30611744)
        p = u(p, d, v, f, e[c + 6], 15, -1560198380)
        f = u(f, p, d, v, e[c + 13], 21, 1309151649)
        v = u(v, f, p, d, e[c + 4], 6, -145523070)
        d = u(d, v, f, p, e[c + 11], 10, -1120210379)
        p = u(p, d, v, f, e[c + 2], 15, 718787259)
        f = u(f, p, d, v, e[c + 9], 21, -343485551)
        v = o(v, n)
        f = o(f, r)
        p = o(p, i)
        d = o(d, h)
    # print(v, f, p, d)
    return [v, f, p, d]


def f(e):
    c = [0] * (len(e) >> 2)
    n = 8 * len(e)
    for t in range(0, n, 8):
        c[t >> 5] |= (255 & ord(e[int(t / 8)])) << t % 32
    return c


def o(e, t):
    # print(e, t)
    c = (65535 & e) + (65535 & t)
    return int_overflow((e >> 16) + (t >> 16) + (c >> 16) << 16) | 65535 & c


def i(e, t, c, n, r, i):
    a = o(o(t, e), o(n, i))
    l = r
    # print("a:", a)
    # print(int_overflow(a << l) | (unsigned_right_shift(a, 32 - l) & 0xFFFFFFFF))
    # print(c)
    return o(int_overflow(a << l) | (unsigned_right_shift(a, 32 - l) & 0xFFFFFFFF), c)


def a(e, t, c, n, r, o, a):
    return i(t & c | ~t & n, e, t, r, o, a)


def l(e, t, c, n, r, o, a):
    return i(t & n | c & ~n, e, t, r, o, a)


def s(e, t, c, n, r, o, a):
    return i(t ^ c ^ n, e, t, r, o, a)


def u(e, t, c, n, r, o, a):
    return i(c ^ (t | ~n), e, t, r, o, a)


# def unsigned_right_shift(x, n):
#     # 将 x 转换成 32 位二进制数的补码形式
#     binary_str = bin(x & 0xFFFFFFFF)[2:].zfill(32)
#     # 将二进制字符串向右移动 n 位
#     shifted_str = binary_str[n:].zfill(32)
#     # 将新的二进制字符串转换回整数并返回
#     return int(shifted_str, 2)

import ctypes


def unsigned_right_shift(n, i):
    # 数字小于0，则转为32位无符号uint
    if n < 0:
        n = ctypes.c_uint32(n).value
    # 正常位移位数是为正数，但是为了兼容js之类的，负数就右移变成左移好了
    if i < 0:
        return -int_overflow(n << abs(i))
    # print(n)
    return int_overflow(n >> i)


def int_overflow(val):
    maxint = 2147483647
    if not -maxint - 1 <= val <= maxint:
        val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
    return val
