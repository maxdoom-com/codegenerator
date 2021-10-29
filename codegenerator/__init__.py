import yaml, jinja2, pathlib

"""
======================================================================
Example template file ("example.j2"):
======================================================================

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

======================================================================
Example yaml file ("example.yaml"):
======================================================================

!Greetings
me: World

======================================================================
Example python code:
======================================================================
from codegenerator import TAG, compile_template, load_yaml

class Greetings(TAG):
    yaml_tag = '!Greetings'

    @property
    def greetings(self):
        return "Hello " + self.me

compile_template("example.j2", root=load_yaml("example.yaml"))
======================================================================
"""

TAG = yaml.YAMLObject




def load_yaml(yaml_file):
    """
    just loads a yaml file and accepts YamlTags like this:
    
    class Foo(cg.YAMLObject):
        yaml_tag = u'!Foo'
    """

    with open(yaml_file) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def split(text):
    """
    splits a text by lines starting with "--- .../filename" and
    returns a dictionary mapping the ".../filename" => the content
    following this mark
    """

    results = {}
    key, lines = None, []

    # iterate over the lines
    for line in text.split("\n"):
        if line.startswith("---"):
            if key: # of the previous file
                results[key] = "\n".join(lines)
            try:
                key = line.split(" ")[1]
            except IndexError:
                key = None # so the result gets eaten up
            lines = []
        else:
            lines.append(line)

    # last file
    if key:
        results[key] = "\n".join(lines)
        key = None
        lines = []

    return results


def directories(mapping):
    """
    gets a list of directories, unique and sorted from
    a dictionary { dir/subdir/.../filename => content, ... }
    """

    dirs = []
    for key in mapping:
        dir = "/".join( key.split('/')[0:-1] )
        if dir and not dir in dirs:
            dirs.append( dir )
    return sorted(dirs)


def mkdirs(dirs):
    """
    makes a list of directories
    """
    
    for dir in dirs:
        path = pathlib.Path(dir)
        path.mkdir(mode=511, parents=True, exist_ok=True)


def mkfiles(files):
    """
    (over)writes a list of files given as dictionary (filename => content)
    """

    for file, text in files.items():
        with pathlib.Path(file).open('w') as file:
            file.write(text)


def compile_template(template, **data):
    """compile a template (jinja2) and generate files and directories for it"""

    # get a jinja2 loader
    env   = jinja2.Environment( loader = jinja2.FileSystemLoader(["."]) )
    env.trim_blocks = True
    # env.lstrip_blocks = True

    # load the template
    tpl   = env.get_template(template)

    # expand the template
    text  = tpl.render(**data)

    # get a mapping of files to their content
    files = split(text)

    # get a sorted list of directories
    dirs  = directories(files)

    # make the directories
    mkdirs(dirs)

    # make the files
    mkfiles(files)

