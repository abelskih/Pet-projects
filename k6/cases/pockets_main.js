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

    const url_pockets = new URL(url_host + '/play/pockets/play-main/');

    const searchParams = new URLSearchParams([
        ['page', randomIntBetween(1, 2)],
        ['limit', 12]
    ]);
    url_pockets.search = searchParams.toString();
    const res = http.get(url_pockets.toString(), {});
    check(res, {'status is 200': (r) => r.status === 200});
	return res;
}
