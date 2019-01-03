# README #

## Frondtend

### Folders
 * Templates : geonome-vis\django\heatmap\templates
 * Module sources: geonome-vis\django\static\src
 * Module css : geonome-vis\django\static\css\modules

### Modules
 * userManager : geonome-vis\django\static\src\userManager
 * unitManager : geonome-vis\django\static\src\unitManager
 * historyManager : geonome-vis\django\static\src\historyManager
 * visualizer : geonome-vis\django\static\src\visualizer

### Dependency

* jQuery
* jQueryUI
* D3JS
* bootstrap
* lodash


### Django installation
* install python3
bash install.sh
* install django==1.8
* * pip (or pip3) install django==1.8
* dependencies:
* * import-export
  https://github.com/django-import-export/django-import-export/issues/200
* * pymysql
* * numpy
* * scipy
* * pandas
* * django-sendfile
* * scikit-learn
* * bs4

* Database : geonome-vis\django\genovis\settings.py

```
#!python

 DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'genovis',
    'USER': 'genomevis',
    'PASSWORD': 'iVADER404-2',
    'HOST': 'ivaderlab.unist.ac.kr',
    'PORT': '8983'
    }
}
```