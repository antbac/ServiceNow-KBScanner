# ServiceNow-KBScanner
Someone recently notified me that our organization had accidentally exposed some internal ServiceNow knowledge base articles on the internet for anyone to read. We quickly fixed the configuration on our end and now I decided to share this free tool to easily tell if you too have publicly available knowledge base articles.

> The tool can only tell you whether or not you have publicly available knowledge bases, it is up to you to evaluate if they are public by design.

In order to run the tool you must first have `python` installed on your system. Additionally you may have to install the <b>requests</b> module for python using `pip install requests` or `python -m pip install requests`. The tool may then be run using `python ./main.py`.

<b>config.json</b> contains 4 customizable properties:
- <b>mode</b>: can be run in either "basic", "deep" or "complete". <i>basic</i> will only tell you whether or not you have publicly available knowledge base articles whereas <i>deep</i> and <i>complete</i> will provide more information on what is actually available
- <b>timeout</b>: the time in seconds to wait before considering a site unreachable
- <b>parallelScans</b>: the number of parallel threads you wish to use in case you scan multiple domains
- <b>domains</b>: a list of domains to scan