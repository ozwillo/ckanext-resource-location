#ckanext-location
This extension is meant to add location fields at the end of csv field 
when they are uploaded and contain addresses.

**Requires CKAN Version 2.7.2 or higher.**

##Installation Instructions

- Add the ckanext-location folder in the same folder as your other extensions
- Make sure your virtualenv is activated :
```
. /usr/lib/ckan/default/bin/activate
```
- Change to the extension’s directory :
 ```
cd /usr/lib/ckan/default/src/ckanext-location
```
- Install the extension by running :
 ```
 python setup.py develop
 ```
- And add the following to your ckan.ini:
```
ckan.plugins = ... location
```

##How it works
When uploading a new csv resource to a dataset, fill the fields address, 
city and zipcode fields with the number of the column corresponding 
to these in your file and click ```Add```, the file will be automatically
processed and latitude and longitude columns will be added at the end of your file, 
giving you the coordinates of each address.

##Language management
- To add new translation, make sure you have babel install in your virtual environment,
if not run :
```
pip install --upgrade Babel
```
- Change to the language folder :
```
cd /usr/lib/ckan/default/src/ckanext-location/ckanext/location/i18n
```
- Create the file setup.cfg:
```
nano setup.cfg
```
- Copy and paste it in :
```
[extract_messages]
keywords = translate isPlural
add_comments = TRANSLATORS:
output_file = ckanext/location/i18n/ckanext-location.pot
width = 80

[init_catalog]
domain = ckanext-location
input_file = ckanext/location/i18n/ckanext-location.pot
output_dir = ckanext/location/i18n

[update_catalog]
domain = ckanext-location
input_file = ckanext/location/i18n/ckanext-location.pot
output_dir = ckanext/location/i18n

[compile_catalog]
domain = ckanext-location
directory = ckanext/location/i18n
statistics = true
```
- Change to the folder :
```
/usr/lib/ckan/default/src/ckanext-location/
```
- Generate the translation file :
```
python setup.py extract_messages
```
- Generate the french file :
```
python setup.py init_catalog -l fr
```
- Translate your strings
- Compile your file :
```
python setup.py compile_catalog
```
And you're done !

