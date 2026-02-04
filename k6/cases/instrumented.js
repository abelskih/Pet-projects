import http from 'k6/http';
import {check} from 'k6';
import {URLSearchParams} from '../utils/UrlParam.js';

export default function (url_host) {
    const params = {
        headers: {
            'X-MyHeader': 'k6test',
            'X-Example-Header': 'instrumented/get'
        },
    };
    //const url_host = 'https://' + __ENV.HOST;
    const array = ['archeage', 'caliber', 'atomic_heart', 'korabli_su', 'warface', 'lost_ark', 'baldurs_gate_3_cloud', 'allody_onlajn'];
    const randomIndex = Math.floor(Math.random() * array.length);
    const randomElement = array[randomIndex];
    const url = new URL(url_host + '/play/games/get/?full_cost_info=1&check_register=1&slug=' + randomElement);
    const res = http.get(url.toString(), {});
    check(res, {'status is 200': (r) => r.status === 200});
	return res;
}
