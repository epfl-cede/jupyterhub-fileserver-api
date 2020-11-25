# General Input
Every input should have those parameters :
- 'user'
- 'timestamp'
- 'payload'
- 'md5_payload'
- 'key'

## user
Type : json table
Fields :
- id (string) : moodle user id 
- primary_email (string) : Email of moodle user
- auth_method (string) : authentication method from moodle

### Test user 
In order to try the API an users tests can be used:
 ``` user: {id:'test', primary_email:'test@epfl.ch',auth_method:"test"} ```
 ``` user: {id:'test2', primary_email:'test2@epfl.ch',auth_method:"test"} ```
 ``` user: {id:'test3', primary_email:'test3@epfl.ch',auth_method:"test"} ```

**Be careful the ```test```  auth_method is reserved and only those login will work**

### Example 
```
user: {id:'253705', primary_email:'pierre-olivier.valles@epfl.ch',auth_method:"noto"}
```

## timestemp
Type : int
The epoch time of the request

## payload 
Type : string / json
Could be empty '{}' or extra command depending of the endpoint

## md5_payload
Type : string
The md5 (base64) of the payload

## key
Type : string
The hmac-sha256 (base64) of user(utf8) + timestamp(utf8)  + md5_payload(base64) using the shared key for encryption
Note : key is shared between the api and the user and it is not send


# General output

The output is a JSON string with 
- md5_payload(base64)
- payload
- return
    - code
    - status
    
## md5_payload
Type : string
The md5 (base64) of the payload

## payload 
Type : string / json
Could be empty '{}' or output of the command depending of the endpoint

## Return
Status of the request in a JSON table with ```code``` and ```status```

### Code
Type : Int
If different than 0 the request has an error

### Status
Type : String
If Code = 0 then Status is "OK" 
Otherwise the status give an explanation about the error

## Example 
```
{
    "md5_payload": "mZFLkyvTelC5g8XnyQrpOw==",
    "payload": "{}",
    "return": {
        "code": 0,
        "status": "OK"
    }
}
```

# Commands

## __/ls__ : List the contents of a path for a given user
Method : GET
Description : This command list the directories and file for a given path inside an user folder. 
The desired user and path is given in the command payload

Input :
- user (string)
- path (string)

Output : A table of :
- name (string) : name of the object
- type (string) : "directory" or "file"
- last-modification (formated string ```%Y-%m-%d %H:%M:%S```) : last modification (for file only) 
### Example :
- Input : 
```
{ user: {id:'test', primary_email:'test@epfl.ch',auth_method:"test"}, path:"truc/test0"}
```

- Output :
 ```
{
    "md5_payload": "y63WGT+xQaB0EFdrIPEMUg==",
    "payload": "[{\"name\": \"Documentation\", \"type\": \"directory\"}, {\"name\": \"my_venvs\", \"type\": \"directory\"}, {\"name\": \"my_notebooks\", \"type\": \"directory\"}, {\"name\": \"git\", \"type\": \"directory\"}, {\"name\": \"switchdrive\", \"type\": \"directory\"}, {\"name\": \"Untitled.ipynb\", \"type\": \"file\", \"last-modification\": \"2020-03-30 16:52:11\"}, {\"name\": \"fill.sh\", \"type\": \"file\", \"last-modification\": \"2019-08-14 16:20:53\"}, {\"name\": \"JuliaTest.ipynb\", \"type\": \"file\", \"last-modification\": \"2020-03-26 09:03:28\"}, {\"name\": \"Neuron.ipynb\", \"type\": \"file\", \"last-modification\": \"2020-03-25 15:40:25\"}, {\"name\": \"Java.ipynb\", \"type\": \"file\", \"last-modification\": \"2020-03-26 09:04:23\"}, {\"name\": \"SQL.ipynb\", \"type\": \"file\", \"last-modification\": \"2020-04-27 23:37:49\"}, {\"name\": \"cities.sqlite\", \"type\": \"file\", \"last-modification\": \"2020-04-27 23:36:03\"}, {\"name\": \"Untitled1.ipynb\", \"type\": \"file\", \"last-modification\": \"2020-05-04 17:31:51\"}, {\"name\": \"spawn.rules\", \"type\": \"file\", \"last-modification\": \"2020-03-30 17:08:15\"}, {\"name\": \"jnb.conf\", \"type\": \"file\", \"last-modification\": \"2020-05-04 14:23:35\"}, {\"name\": \"nest.ipynb\", \"type\": \"file\", \"last-modification\": \"2020-05-19 15:04:52\"}, {\"name\": \"Slides.ipynb\", \"type\": \"file\", \"last-modification\": \"2020-06-18 17:23:30\"}, {\"name\": \"testslides.py\", \"type\": \"file\", \"last-modification\": \"2020-06-18 17:04:14\"}, {\"name\": \"Octave\", \"type\": \"directory\"}, {\"name\": \"Untitled2.ipynb\", \"type\": \"file\", \"last-modification\": \"2020-09-21 23:25:04\"}, {\"name\": \"Untitled3.ipynb\", \"type\": \"file\", \"last-modification\": \"2020-07-08 15:43:34\"}, {\"name\": \"toto\", \"type\": \"directory\"}, {\"name\": \"assign\", \"type\": \"directory\"}, {\"name\": \"assign-V2\", \"type\": \"directory\"}, {\"name\": \"assign-V3\", \"type\": \"directory\"}, {\"name\": \"assign-V4\", \"type\": \"directory\"}, {\"name\": \"assign-V5\", \"type\": \"directory\"}]",
    "return": {
        "code": 0,
        "status": "OK"
    }
}
```

## __/lof__ : List recursively the contents of a path for a given user
Method : GET
Description : This command list the directories and file for a given path inside an user folder. Directories are scanned recursively
The desired user and path is given in the command payload

Input :
- user (string)
- path (string)

Output : A table of :
- name (string) : name of the object
- type (string) : "directory" or "file"
- last-modification (formated string ```%Y-%m-%d %H:%M:%S```) : last modification (for file only) 
- children (json table)  (for directory only) : contents inside this folder 

### Example :
- Input : 
```
{ user: {id:'test2', primary_email:'test2@epfl.ch',auth_method:"test"}, path:"./"}
```

- Output :
```
{
    "md5_payload": "97aq2BAYEwyOEU3fLUzZtg==",
    "payload": "[{\"name\": \"one.txt\", \"type\": \"file\", \"last-modification\": \"2020-11-25 13:22:30\"}, {\"name\": \"dir1\", \"type\": \"directory\", \"children\": [{\"name\": \"two.txt\", \"type\": \"file\", \"last-modification\": \"2020-11-25 13:22:41\"}, {\"name\": \"three.txt\", \"type\": \"file\", \"last-modification\": \"2020-11-25 13:22:46\"}]}]",
    "return": {
        "code": 0,
        "status": "OK"
    }
}
```


## __/lod__ : List of directories
Method : GET
Description : This command list the directories inside an user folder. The desired user is given in the command payload
Input :
- user (string)
 
Output : A table of :
- name (string) : directory name
- type (string) : "directory"
- children (json table) : contains the other directories inside this folder 

### Example :
- Input : 
```
{ user: {id:'test', primary_email:'test@epfl.ch',auth_method:"test"} ,path:"./"} }
```

- Output :
```
{
    "md5_payload": "...",
    "payload": "{\"name\": \"antoine\", \"type\": \"directory\", 
\"children\": [{\"name\": \"essai\", \"type\": \"directory\", \"children\": []}, {\"name\": \"important\", \"type\": \"directory\", \"children\": [{\"name\": \"bidule\", \"type\": \"directory\", \"children\": []}]}, {\"name\": \"truc\", \"type\": \"directory\", \"children\": [{\"name\": \"test0\", \"type\": \"directory\", \"children\": [{\"name\": \"test0.1\", \"type\": \"directory\", \"children\": []}]}]}]}",
    "return": {
        "code": 0,
        "status": "OK"
    }
}
```

## __/zfs__ Send a directory as zip

Method : GET

Description : This command return a zip (blob) from a given directory

Input : 
- user (string)
- folder (string) : the path of the folder where the zip will be started

Output :
- origin (string) : directory path
- blob (string) : blob of zip in base64
- method (string) : "base64"
- mime  (string) : "application/zip"

### Example

- Input : ```{ user:{id:'test', primary_email:'test@epfl.ch',auth_method:"test"}, folder: "truc" }```
- Output :
```
{
    "md5_payload": "KmNIY9E57uw9PkADx4eMhg==",
    "payload": "{\"origin\": \"povalles/toto\", \"blob\": \"UEsDBBQAAAAIADVgY1EADxSrCgAAAAgAAAALAAAAaGVsbG9fd29ybGTLSM3JyVdQ5AIAUEsBAhQDFAAAAAgANWBjUQAPFKsKAAAACAAAAAsAAAAAAAAAAAAAAKSBAAAAAGhlbGxvX3dvcmxkUEsFBgAAAAABAAEAOQAAADMAAAAAAA==\", \"method\": \"base64\", \"mime\": \"application/zip\"}",
    "return": {
        "code": 0,
        "status": "OK"
    }
}
```

## __/uzu__ Upload a zip and extract it in a given directory

Method : POST
Description : This command upload a zip (blob) and extract it in a given directory
Input :
- user (string)
- folder (string) : the path of the folder where the zip will be extracted

The file is send through _form_data_ inside the ```file``` key

Output :
- extractpath (string) : directory of extraction
_Note_ : if the destination already exist in the folder then the API will add a -V<number> at the end of the path until it find a non-existing version.


### Example

- Input :
```
{ user: {id:'test', primary_email:'test@epfl.ch',auth_method:"test"}, destination: "assign"}```

+

```file``` in  _form_data_

```

- Output :
```
{
    "md5_payload": "PNorwNys7O56G/Ljexix1A==",
    "payload": "{\"extractpath\": \"/povalles/assign-V5\"}",
    "return": {
        "code": 0,
        "status": "OK"
    }
}
```

## __/endpoints_stats__ Statics on endpoints

Return the usage and timings on each endpoints on the api

Note: This is accessible without keys

### Example

- Input : 
 _None_

- Output :`
```
{
    "duration": [
        {
            "endpoint \"/\" ": {
                "avg": 0.005962371826171875,
                "count": 1,
                "max": 0.005962371826171875,
                "min": 0.005962371826171875,
                "percentile_25": 0.005962371826171875,
                "percentile_50": 0.005962371826171875,
                "percentile_75": 0.005962371826171875,
                "percentile_90": 0.005962371826171875
            }
        },
        {
            "endpoint \"/endpoints_stats\" ": {
                "avg": 0.06605410575866699,
                "count": 1,
                "max": 0.06605410575866699,
                "min": 0.06605410575866699,
                "percentile_25": 0.06605410575866699,
                "percentile_50": 0.06605410575866699,
                "percentile_75": 0.06605410575866699,
                "percentile_90": 0.06605410575866699
            }
        },
        {
            "endpoint \"/lod\" ": {
                "avg": 0.011118471622467041,
                "count": 4,
                "max": 0.012638092041015625,
                "min": 0.009519815444946289,
                "percentile_25": 0.009519815444946289,
                "percentile_50": 0.01044607162475586,
                "percentile_75": 0.01186990737915039,
                "percentile_90": 0.01186990737915039
            }
        }
    ]
}
```

