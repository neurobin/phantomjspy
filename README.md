[![Build Status](https://travis-ci.org/neurobin/phantomjspy.svg?branch=release)](https://travis-ci.org/neurobin/phantomjspy)

PhantomJS wrapper in Python

# Pre requisites

1. **phantomjs:** `phantomjs` command line tool.
2. **Python 3**

# Install

```bash
pip install phantomjs
```

# Usage

## Using with a custom phantomjs script:

```python

from phantomjs import Phantom

phantom = Phantom()

conf = {
    'url': 'http://example.com/',   # Mandatory field
}
output = phantom.download_page(conf, js_path='/my/phantomjs/script/path')
```

In your phantomjs script, you can take the url as:

```javascript
var system = require('system');
var json = JSON.parse(system.args[1]);
var url = json.url;
```

## Using the default phantomjs script provided with this package:

```python

from phantomjs import Phantom

phantom = Phantom()

conf = {
    'url': 'http://example.com/',   # Mandatory field
    'output_type': 'html',          # json for json
    'min_wait': 1000,               # 1 second
    'max_wait': 30000,              # 30 seconds
    'selector': '',                 # CSS selector if there's any
    'resource_timeout': 3000,       # 3 seconds
    'headers': {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.72 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Sec-Fetch-Mode": "navigate",
        'Sec-Fetch-Site': 'same-origin',
        'Upgrade-Insecure-Requests': '1',
    },
    'cookies': [
        {'name': '_Country', 'value': 'US', 'domain': '.google.com',},
        {'name': '_Currency', 'value': 'USD', 'domain': '.google.com',},
    ],
    'functions': [
        'function(){window.location.replace("http://icanhazip.com/");}',
    ],
}


output = phantom.download_page(conf)
```
