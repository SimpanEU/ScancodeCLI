cd /PrebootManuscriptCLI

#### Accepted arguments:  
-u \<username>  -p \<password>  -t \<default timeout in ms>  
or  
-s \<"string">  -t \<default timeout in ms>

### Create manuscript using username and password arguments:
python -m run -u username -p password -t 32


### Create manuscript using string argument:
python -m run -s "username\<tab>password\<enter>\<sleep=1000>\<enter>" -t 32


### Create manuscript running CLI:
1. python -m run

2. Enter full string:
e.g. username\<tab>password\<enter>\<sleep=1000>\<enter>

3. Enter default timeout, e.g. 32