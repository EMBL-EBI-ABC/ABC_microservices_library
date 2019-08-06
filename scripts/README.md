# Script to work with Fire API

## Documentation
This script will allow you to upload your file to Fire database, get public link, delete file and list all objects that were uploaded to Fire.

Before using script you need to get access (username and password) and your archive name from Fire team. To get access please write email to [fire@ebi.ac.uk](mailto:fire@ebi.ac.uk)

Getting Started Documentation: http://docs.fire.ebi.ac.uk/getting-started.html#getting-started

Complete Documentation: http://docs.fire.ebi.ac.uk/fire-documentation.html

Swagger Documentation: https://hh.fire-test.sdo.ebi.ac.uk/swagger-ui.html

## Script documentation
Try to run script with -h parameter to get help about usage
```markdown
 python scripts/fire_api.py -h
 
 usage: fire_api.py [-h] [-a ACTION] [-f FILENAME] [-p PATH] [-id ID]

optional arguments:
  -h, --help            show this help message and exit
  -a ACTION, --action ACTION
                        Which function to use, could be 'upload_object',
                        'get_public_link', 'list_objects' and 'delete_object'
  -f FILENAME, --filename FILENAME
                        Path to the file you want to upload to Fire API
  -p PATH, --path PATH  Path that will be used for public access inside Fire
                        API
  -id ID, --fireOId ID  Fire API id of object (optional, will be used only to
                        delete object)

```

To use script you need to provide .env file inside script directory with these fields:
1. USERNAME={username from fire team}
2. PASSWORD={password from fire team}
3. ARCHIVE_NAME={archive name to public access}
4. API_ENDPOINT={api poin you want to use: http://docs.fire.ebi.ac.uk/public-access.html#endpoints}

#### How to upload file to Fire:
```markdown
 python scripts/fire_api.py -a upload_object -f <path_to_your_file> -p <path_inside_fire_for_public_access>
```

#### How to list all objects that were uploaded:
```markdown
python scripts/fire_api.py -a list_objects
```

#### How to get public access link:
```markdown
python scripts/fire_api.py -a get_public_link -f <path_to_your_file> -p <path_inside_fire_for_public_access>
```

#### How to delete object:
For this you need to know fireOId (you can get it using list_objects action)
```markdown
python scripts/fire_api.py -a delete_object -id <fireOId>
```