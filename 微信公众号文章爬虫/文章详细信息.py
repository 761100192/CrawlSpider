import requests
from lxml import etree



url = 'http://mp.weixin.qq.com/s?__biz=MjM5MjAxNDM4MA==&mid=2666402907&idx=1&sn=747c3543e30804d04331bfac21f6afe7&chksm=bdb67d188ac1f40e5cc69394a9eae30eff2383505a4f00d6d71fb95a3d614a9718ead51653ee#rd'


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    ,"cookie": "pgv_pvid=5093459280; RK=fG5w1UtTn/; ptcz=e892253ea3a2fdd0ee0234b280e7c059348f3bf96406f70be5f9f7eecac3056a; eas_sid=V1a6c0V9W1K4K2M4S4T3f247E9; tvfe_boss_uuid=22a8bf3be7934ce1; ua_id=7RqnrxyGWQruVEaJAAAAAIEHwgkBfboqgMssq3QZzQ8=; iip=0; sd_userid=49931612542003568; sd_cookie_crttime=1612542003568; o_cookie=761100192; openid2ticket_oWBZkuC93LdcDTEVUV5sAfk31sU8=; mm_lang=zh_CN; wxuin=14672111281338; pac_uid=1_761100192; openid2ticket_oIpjZvh5pwNzb6mCN0afISMMITCQ=; ptui_loginuin=761100192; uuid=35c1a3a795994ca8e9bf6fb578a74802; rand_info=CAESINnV5BIXwXmmKKTRyv0jy0YJY8hM0h82aUua/6lH2jyO; slave_bizuin=3201931298; data_bizuin=3201931298; bizuin=3201931298; data_ticket=6k9s9WVEvDFZEQmylukJ69nf25z8czI40UgqwfabYQvV4ygSjwYpBe/BFR0zUxpX; slave_sid=MGdXcUM3aUNudzJGcTBuN1d1Z25Ud2JpUDVqVkVSMDZuOVhJUkpEYks4WE5kek8zQ1ZDOUtVMmtYR01WS0IxTTlLcEo2TXgwYWdPcmVxSWU3cU0wNEdBOWtkNktTTlN6M0VtdHlOYTRhNXlHYzY0RW1QbTRlYnZ5ckJmVnVXTGc0ZDFhaHNwVDUxZWR4RzFK; slave_user=gh_881c261c4e90; xid=cc6b2687733c1932e10616e7f1f1af00; rewardsn=; wxtokenkey=777"
}

response = requests.get(url,headers=headers)
tree = etree.HTML(response.text)