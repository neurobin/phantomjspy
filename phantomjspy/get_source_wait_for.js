
/**
* Wait until the test condition is true or a timeout occurs. Useful for waiting
* on a server response or for a ui change (fadeIn, etc.) to occur.
*
* @param testFx javascript condition that evaluates to a boolean,
* it can be passed in as a string (e.g.: "1 == 1" or "$('#bar').is(':visible')" or
* as a callback function.
* @param onReady what to do when testFx condition is fulfilled,
* it can be passed in as a string (e.g.: "1 == 1" or "$('#bar').is(':visible')" or
* as a callback function.
* @param timeOutMillis the max amount of time to wait. If not specified, 3 sec is used.
*/

function waitFor(testFx, onReady, timeOutMillis) {
var maxtimeOutMillis = timeOutMillis ? timeOutMillis : 3000, //< Default Max Timout is 3s
    start = new Date().getTime(),
    condition = false,
    minTime = 250, //250 ms must be passed initially before trying to run testFx
    interval = setInterval(function() {
        var nowTime = new Date().getTime();
        if ( (nowTime - start >= minTime) && (nowTime - start < maxtimeOutMillis) && !condition ) {
            // If not time-out yet and condition not yet fulfilled
            condition = testFx(); //<    defensive code
        } else if(nowTime - start >= minTime) {
            //if condition is fulfilled or timeout reached, return the page
            onReady();
            clearInterval(interval); //< Stop this interval
        }
    }, 250); //< repeat check every 250ms
};

var system = require('system');
var page   = require('webpage').create();
// system.args[0] is the filename, so system.args[1] is the first real argument
var url    = system.args[1];
var selector = system.args[2];
var timeout = system.args[3];

//settings
page.settings.resourceTimeout = 3000;
page.settings.userAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.72 Safari/537.36';

page.customHeaders = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Sec-Fetch-Mode": "navigate",
    'Sec-Fetch-Site': 'same-origin',
    'Upgrade-Insecure-Requests': '1',
  };
  

var cookies = [
    {'name': '_Country', 'value': 'US'},
    {'name': '_Currency', 'value': 'USD'},
    {'name': '_Country_Name', 'value': 'United+States'},
    {'name': 'Drupal.visitor.commerce_currency', 'value': 'USD'}
];

for(var i in cookies){
    page.addCookie(cookies[i]);
    // phantom.addCookie(cookies[i]);
}


// page.onConsoleMessage = function(msg, lineNum, sourceId) {
//     console.error('CONSOLE: ' + msg + ' (from line #' + lineNum + ' in "' + sourceId + '")');
//   };

// page.onError = function(msg, trace) {

//     var msgStack = ['ERROR: ' + msg];
  
//     if (trace && trace.length) {
//       msgStack.push('TRACE:');
//       trace.forEach(function(t) {
//         msgStack.push(' -> ' + t.file + ': ' + t.line + (t.function ? ' (in function "' + t.function +'")' : ''));
//       });
//     }
  
//     console.error(msgStack.join('\n'));
  
//   };

// page.onResourceError = function(resourceError) {
//     console.error('Unable to load resource (#' + resourceError.id + ' URL:' + resourceError.url + ')');
//     console.error('Error code: ' + resourceError.errorCode + '. Description: ' + resourceError.errorString);
// };

// http://phantomjs.org/api/webpage/handler/on-resource-timeout.html
// page.onResourceTimeout = function(request) {
//     console.error('Response Timeout (#' + request.id + '): ' + JSON.stringify(request));
// };

// render the page, and run the callback function
page.open(url, function (status) {
    if(status == 'success'){
        //~ console.log('Selector: '+selector);
        //~ console.log('Timeout: '+ timeout/1000+ ' seconds');
        var testFx = function (){
            return page.evaluate(function(selector) {
                if(selector == '.dummy') return false;
                var isVisible = function(elem){
                    if(!!elem){
                        return !!( elem.offsetWidth || elem.offsetHeight || elem.getClientRects().length );
                    } else {
                        return false;
                    }
                };
                return isVisible(document.querySelector(selector));
            }, selector);
        };
        var onReady = function (){
            console.log(page.content);
            phantom.exit();
        };
        waitFor(testFx, onReady, timeout);
        // phantom.exit();
    } else{
        console.log("E: Phantomjs failed to open page: " + url);
        phantom.exit();
    }
});
