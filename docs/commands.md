# General Input
Every input should have those parameters :
- 'user'
- 'timestamp'
- 'payload'
- 'md5_payload'
- 'md5'

## user
Type : string
The username for accessing the API

## timestemp
Type : int
The epoch time of the request

## payload 
Type : string / json
Could be empty '{}' or extra command depending of the endpoint

## md5_payload
Type : string
The md5 (base64) of the payload

## md5
Type : string
The md5 (base64) of user + timestamp  + md5p + key
Note : key is shared between the api and the user and is not send


# General output

The output is a JSON string with 
- md5_payload
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
    "md5_payload": "9e537c263b5aa2ad3f271fc0f7c7b2de",
    "payload": "{\"name\": \"antoine\", \"type\": \"directory\", \"children\": [{\"name\": \"essai\", \"type\": \"directory\", \"children\": []}, {\"name\": \"important\", \"type\": \"directory\", \"children\": [{\"name\": \"bidule\", \"type\": \"directory\", \"children\": []}]}, {\"name\": \"truc\", \"type\": \"directory\", \"children\": [{\"name\": \"test0\", \"type\": \"directory\", \"children\": [{\"name\": \"test0.1\", \"type\": \"directory\", \"children\": []}]}]}]}",
    "return": {
        "code": 0,
        "status": "OK"
    }
```

# Commands

## __/lod__ : List of directories
Method : GET
Description : This command list the directories inside a user folder. The desired user is given in the command payload
Input :
- user (string)
 
Output : A table of :
- name (string) : directory name
- type (string) : "directory"
- children (json table) : contains the other directories inside this folder 

### Example :
- Input : 
```
{ user: "antoine" }
```

- Output :
 ```
{
    "md5_payload": "9e537c263b5aa2ad3f271fc0f7c7b2de",
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

- Input : ```{ user: "antoine", folder: "truc" }```
- Output :
```
{\"origin\": \"antoine/truc\", 
\"blob\": \"..\",
 \"method\": \"base64\",
 \"mime\": \"application/zip\"}
```

## __/uzu__ Upload a zip and extract it in a given directory

Method : POST (now GET only)
Description : This command upload a zip (blob) and extract it in a given directory
Input :
- user (string)
- folder (string) : the path of the folder where the zip will be extracted
- blob (string) : blob of the zip in base64
- method (string): "base64"
- mime (string) : "application/zip" 

Output :
- extractpath (string) : directory of extraction
_Note_ : if the destination already exist in the folder then the API will add a -V<number> at the end of the path until it find a non-existing version.
- method (string) : "base64"
- mime  (string) : "application/zip"

### Example

- Input :
```
{ user: "machin", destination: "assign", blob: blob, method: "base64", mime: "application/zip" };
```

- Output :
```
{
    "md5_payload": "e88cc1a2b9b79dee6bcd304c81ed116b",
    "payload": "{\"extractpath\": \"/assign-V6\"}",
    "return": {
        "code": 0,
        "status": "OK"
    }
}
```

