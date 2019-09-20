import requests
from lxml import etree


headers= {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    "Cookie": "uuid'"
}

# 获取详情页面的url
def get_detail_urls(url):
    # 2.获取页面内容
    resp = requests.get(url, headers=headers)
    text = resp.content.decode("utf-8")
    # print(text)

    # 3.解析网页
    html = etree.HTML(text)
    ul = html.xpath('//ul[@class="carlist clearfix js-top"]')[0]
    # print(ul)
    lis = ul.xpath('./li')
    # print(lis)
    detail_urls = []
    for li in lis:
        detail_url = li.xpath('./a/@href')
        detail_url = 'https://www.guazi.com' + detail_url[0]
        # https://www.guazi.com/cd/936748ddd7df16dfx.htm#fr_page=list&fr_pos=city&fr_no=0
        # print(detail_url)
        detail_urls.append(detail_url)
    return detail_urls

# 解析详情页面内容
def parse_detail_url(url):
    resp = requests.get(url, headers=headers)
    text = resp.content.decode('utf-8')
    html = etree.HTML(text)
    # print(html)
    title = html.xpath('//div[@class="product-textbox"]/h2/text()')[0]
    title = title.replace(r'\r\n', '').strip()
    # print(title)
    infos= {}
    info = html.xpath('//div[@class="product-textbox"]/ul/li/span/text()')
    print(info)
    infos['title'] = title
    infos['card_time'] = info[0]
    infos['km'] = info[1]
    if info[2] == '成都':
        infos['displacement'] = info[2].replace('成都', info[3]).strip()
        infos['gearbox'] = info[4]
    else:
        infos['displacement'] = info[2]
        infos['gearbox'] = info[3]
    return infos

def main():
    # 1.目标url

    base_url = 'https://www.guazi.com/cd/buy/o{}/#bread'
    with open('guazi_cd.csv', 'a', encoding='utf-8') as fp:
        for i in range(1, 51):
            url = base_url.format(i)
            detail_urls = get_detail_urls(url)
            # print(detail_urls)
            for detail_url in detail_urls:
                infos = parse_detail_url(detail_url)
                fp.write('{},{},{},{},{}\n'.format(infos['title'], infos['card_time'],infos['km'], infos['displacement'],infos['gearbox']))



if __name__ == '__main__':
    main()
