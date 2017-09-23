Django JS Translator
====================

Easily translate your front-end code in your Django project !  

This tool outputs an HTML file, using the output body you need, so you can pipe the translation result into a translation helper.

## Command-line

```
usage: django-js-translator [-h] [--dry-run] config_path

Prepare translation files for JS

positional arguments:
  config_path  configuration file path

optional arguments:
  -h, --help   show this help message and exit
  --dry-run    only print output
```

## Configuration

You can configure the translator for your project using a YAML configuration file.  
A sample file is included in the project.  

This sample configuration will:

  - detect **.js** and **.jsx** files,
  - in the `./sample_files` folder,
  - show the position and origin of each translation because the `debug mode` is set,
  - search for the translation directive `tr` *(for example `tr('Hello')`)*,
  - and output a `test.html` file,
  - wrapping the translation in a `django.translate.defineTranslations` function call.  


```yaml
##########################################
# Django JS Translator configuration file

configuration:

  # Paths to watch
  paths:
    - ./sample_files

  # Activate debug mode: show the origin and position of the text to translate
  debug: True

  # Extensions to watch
  extensions:
    - .jsx
    - .js

  # Translation directive to search
  directive: tr

  # Output configuration
  output:

    # Output path
    path: test.html

    # Output body
    body: |
      {{% load i18n %}}

      <script type="text/javascript">
      django.translate.defineTranslations({{
      {0}
      }});
      </script>
```
