# Mock HTTP Origin

Mock HTTP origin is a Python-based web application built using the [Tornado framework](https://www.tornadoweb.org/). It is primarily used for API and configuration development and testing. The application's core function is to include the HTTP request details in its response body. Additionally, it provides several other features that are helpful for bug replication, failover configuration of multi-layer proxy setups, and as a mock API endpoint. You skim through the current options documented in the help.txt file, navigating to the `.*/help` URL path once the application is running, or see the [application example](https://mock-http-origin.nateroyer.com/help).

See an example response [in your browser](https://mock-http-origin.nateroyer.com/example), or by using `curl`:

    curl -i https://mock-http-origin.nateroyer.com/an/example

An example of a JSON formatted response:

    curl -i --header 'Accept: text/json' https://mock-http-origin.nateroyer.com/another/example
