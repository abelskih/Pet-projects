import { browser } from 'k6/browser';
import { check } from 'k6';
import { htmlReport } from './utils/convertHTML.js';


export const options = {
  scenarios: {
	  ui: {
		  executor: 'constant-vus',
		  vus: 5, // number of VUs
		  duration: '30s', // test duration
		  options: {
			  browser: {
				  type: 'chromium',
			  },
		 },
	 },
  },
 // hosts: {
  //'userapi.predprod.cloud.vkplay.ru': '10.220.153.5',
  //'predprod.cloud.vkplay.ru': '10.220.153.5',}
  };

export default async function () {
  const context = await browser.newContext({ });
  const page = await context.newPage();

  try {
    await page.goto('https://'+__ENV.HOST+'/');
	page.waitForNavigation(),
    await page.locator('a[href="https://'+__ENV.HOST+'/play/"][data-id="store"]').click()
	const searchResults = await page.locator('h1[class*="TitleBlockNew-module__title"]').textContent();
    await check(searchResults, {
    'Filter title is correct': (result) => result === 'Каталог игр',
	});
  } catch (error) {
	  console.error('An error occurred:', error);
  }
  finally {
    await page.close(); } }

export function handleSummary(data) {
    console.log('Preparing the end-of-test summary...');

    return {
       'result_webstore.html': htmlReport(data)
	};
}
