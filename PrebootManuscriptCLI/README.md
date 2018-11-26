cd /PrebootManuscriptCLI

Accepted arguments:  
-u \<username>  
-p \<password>  
-t \<default timeout in ms>  
-s \<"string">  

#### Create manuscript using username and password:
python -m run -u username -p password -t 32


#### Create manuscript using string:
python -m run -s "username\<tab>password\<enter>" -t 32


#### Create manuscript running CLI:
1. python -m run

2. Enter full string:
e.g. username\<tab>password\<enter>

3. Enter default timeout, e.g. 32