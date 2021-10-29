from codegenerator import TAG, compile_template, load_yaml

class Greetings(TAG):
    yaml_tag = '!Greetings'

compile_template("example.j2", root=load_yaml("example.yaml"))
