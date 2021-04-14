cookie = "citycode=%7B%22provinceName%22%3A%22%E5%B9%BF%E4%B8%9C%E7%9C%81%22%2C%22cityName%22%3A%22%E4%BD%9B%E5%B1%B1%E5%B8%82%22%2C%22provinceCode%22%3A440000%2C%22cityCode%22%3A440600%7D; zkhst=73263483dffa4bf3a89d0e8b3900a11f; gr_user_id=8ed75b07-8d3f-4391-9a55-5545ca5138f6; 8ccf9443d38f1ead_gr_session_id=5832e99e-62a1-487b-be59-05ac3a11271e; _bl_uid=8mkmtkCqdg1gs5eUt59Oypjxdb86; grwng_uid=721b5112-3eca-4e2d-b2e1-6211f72e8186; 8ccf9443d38f1ead_gr_session_id_5832e99e-62a1-487b-be59-05ac3a11271e=true"
function h(t) {
        t = cookie.match(new RegExp("(^| )".concat(t, "=([^;]*)(;|$)")));
        return null != t ? decodeURIComponent(t[2]) : null
    }
