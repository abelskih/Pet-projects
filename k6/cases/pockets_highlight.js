import http from 'k6/http';
import {check} from 'k6';
import {randomIntBetween} from '../utils/random.js';
import {URLSearchParams} from '../utils/UrlParam.js'

export default function (url_host) {
    const params = {
        headers: {
            'X-MyHeader': 'k6test',
            'X-Example-Header': 'instrumented/get'
        },
    };
    const url_high = new URL(url_host + '/play/pockets/play-highlight/');
    const res = http.get(url_high.toString(), {});
    check(res, {'status is 200': (r) => r.status === 200});
	return res;
}
