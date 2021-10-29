from codegenerator import TAG, compile_template, load_yaml

class Greetings(TAG):
    yaml_tag = '!Greetings'

    @property
    def greetings(self):
        return "Hello " + self.me
    

compile_template("example.j2", root=load_yaml("example.yaml"))
