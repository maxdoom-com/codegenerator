# Codegenerator

A simple codegenerator connecting yaml files (data) and jinja2 templates.

Imagine you have to create many files conforming to template or you find
yourself often building up the same structures of directories and files.

Imagine further, the key informations are changing always but the general
layout is always the same.

So you could want to put your changing data into a yaml file and write a
jinj2 template to output.

You might want to put the generated code into multiple files by just
saying where it should be stored.

A special case has been added: `[[` and `]]` become `{{` and `}}` as
well as `[%` and `%]` become `{%` and `%}` *after* code generation.

This is what this tiny python module makes.

**Attention: This module overwrites existing files!**


## Example template file ("example.j2"):

```jinja2
{#
    THIS IS AN EXAMPLE FOR codegenerator.py!

    INITIAL LINES BEFORE A FILE MARK ("--- {directory/.../}{filename}")
    WILL BE IGNORED!
#}

--- output/subdir/something.txt
Yeah, it works!

---

{#
    IT IS POSSIBLE TO PUT IN CONTENT HERE, THAT WILL BE EATEN UP!
    THEREFORE JUST INSERT A FILE MARK ("---") WITHOUT A FILE NAME.
#}

--- output/hello.txt

{# printing a variable... #}
Hello {{ root.me }}!

{# printing a property from the Greetings class... #}
{{ root.greetings }}!

--- output/hello-to-{{ root.me }}.txt

Hello!

```

## Example yaml file ("example.yaml"):

```yaml

!Greetings
me: World

```

## Example python code:

```py
from codegenerator import TAG, compile_template, load_yaml

class Greetings(TAG):
    yaml_tag = '!Greetings'

    @property
    def greetings(self):
        return "Hello " + self.me

compile_template("example.j2", root=load_yaml("example.yaml"))
```

## Installation

```sh
pip install git+https://github.com/maxdoom-com/codegenerator
```
