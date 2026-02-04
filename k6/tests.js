import http from 'k6/http';
import { sleep } from 'k6';
import { check } from 'k6';
import { Trend, Counter } from 'k6/metrics';
import { htmlReport } from './utils/convertHTML.js';

import  testInstrumented  from './cases/instrumented.js';
import  testMenuVisibility  from './cases/menu_visibility.js';
import  testPocketsHighlight  from './cases/pockets_highlight.js';
import  testPocketsMain  from './cases/pockets_main.js';


const baseApiUrl = 'https://' + __ENV.HOST;


const instrumentedDuration = new Trend('instrumented_http_duration');
const menu_visibilityDuration = new Trend('menu_visibility_http_duration');
const pockets_highlightDuration = new Trend('pockets_highlight_http_duration');
const pockets_mainDuration = new Trend('pockets_main_http_duration');


export const CounterErrors = new Counter('Errors');

export const options = {

    thresholds: {
        http_req_duration: ['p(95)<200'],
    },
		[`Errors{endpoint:'instrumented'}`]:['count<10'],
		[`Errors{endpoint:'menu_visibility'}`]:['count<10'],
		[`Errors{endpoint:'pockets_highlight'}`]:['count<10'],
		[`Errors{endpoint:'pockets_main'}`]:['count<10'],

    scenarios : {
        instrumented : {
            exec: 'instrumentedScenario',
            executor: 'constant-vus',
            vus: __ENV.vus,
            duration: __ENV.duration,
        },
        menu_visibility : {
            exec: 'menu_visibilityScenario',
            executor: 'constant-vus',
            vus: __ENV.vus,
            duration: __ENV.duration,
        },

        pockets_highlight : {
            exec: 'pockets_highlightScenario',
            executor: 'constant-vus',
            vus: __ENV.vus,
            duration: __ENV.duration,
        },

        pockets_main : {
            exec: 'pockets_mainScenario',
            executor: 'constant-vus',
            vus: __ENV.vus,
            duration: __ENV.duration,
        },
    }
};

export function handleSummary(data) {
    console.log('Preparing the end-of-test summary...');

    return {
       'result_apistore.html': htmlReport(data)
	};
}

export function instrumentedScenario() {
    const response = testInstrumented(baseApiUrl);
	instrumentedDuration.add(response.timings.duration, { endpoint:'instrumented' });
    CounterErrors.add(response.status !== 200, { endpoint:'instrumented' });
}

export function menu_visibilityScenario() {
    const response = testMenuVisibility(baseApiUrl);
    menu_visibilityDuration.add(response.timings.duration, { endpoint:'menu_visibility' });
    CounterErrors.add(response.status !== 200, { endpoint:'menu_visibility' });
}

export function pockets_highlightScenario() {
    const response = testPocketsHighlight(baseApiUrl);
    pockets_highlightDuration.add(response.timings.duration, { endpoint:'pockets_highlight' });
    CounterErrors.add(response.status !== 200, { endpoint:'pockets_highlight' });
}

export function pockets_mainScenario() {
    const response = testPocketsMain(baseApiUrl);
    pockets_mainDuration.add(response.timings.duration, { endpoint:'pockets_main' });
    CounterErrors.add(response.status !== 200, { endpoint:'pockets_main' });
}
