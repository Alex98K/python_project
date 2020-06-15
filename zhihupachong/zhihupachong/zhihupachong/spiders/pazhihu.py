# -*- coding: utf-8 -*-
import scrapy
import json
from zhihupachong.items import ZhihupachongItem
import re


class PazhihuSpider(scrapy.Spider):
    name = 'pazhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = []
    for i in range(0, 1000, 5):
        start_url = "https://www.zhihu.com/api/v4/questions/29815334/answers?include=data%5B%2A%5D.is_normal" \
                    "%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail" \
                    "%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment" \
                    "%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission" \
                    "%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship" \
                    ".is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D" \
                    ".mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5" \
                    "&offset={}&platform=desktop&sort_by=default".format(str(i))
        start_urls.append(start_url)

    def parse(self, response):
        js_tep = json.loads(response.body.decode("utf-8"))
        js = js_tep["data"]
        for url in js:
            item = ZhihupachongItem()
            pp = url["content"]
            kk = re.compile(r'[a-zA-z]+://[^\s]*png')
            item["image_urls"] = kk.findall(pp)
        return item
