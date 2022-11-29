#!/usr/bin/python3
<<<<<<< HEAD
"""Module for the entry point of the command interpreter."""

import cmd
from models.base_model import BaseModel
from models import storage
import re
import json


class HBNBCommand(cmd.Cmd):

    """Class for the command interpreter."""

    prompt = "(hbnb) "

    def default(self, line):
        """Catch commands if nothing else matches then."""
        # print("DEF:::", line)
        self._precmd(line)

    def _precmd(self, line):
        """Intercepts commands to test for class.syntax()"""
        # print("PRECMD:::", line)
        match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if not match:
            return line
        classname = match.group(1)
        method = match.group(2)
        args = match.group(3)
        match_uid_and_args = re.search('^"([^"]*)"(?:, (.*))?$', args)
        if match_uid_and_args:
            uid = match_uid_and_args.group(1)
            attr_or_dict = match_uid_and_args.group(2)
        else:
            uid = args
            attr_or_dict = False

        attr_and_value = ""
        if method == "update" and attr_or_dict:
            match_dict = re.search('^({.*})$', attr_or_dict)
            if match_dict:
                self.update_dict(classname, uid, match_dict.group(1))
                return ""
            match_attr_and_value = re.search(
                '^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict)
            if match_attr_and_value:
                attr_and_value = (match_attr_and_value.group(
                    1) or "") + " " + (match_attr_and_value.group(2) or "")
        command = method + " " + classname + " " + uid + " " + attr_and_value
        self.onecmd(command)
        return command

    def update_dict(self, classname, uid, s_dict):
        """Helper method for update() with a dictionary."""
        s = s_dict.replace("'", '"')
        d = json.loads(s)
        if not classname:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** no instance found **")
            else:
                attributes = storage.attributes()[classname]
                for attribute, value in d.items():
                    if attribute in attributes:
                        value = attributes[attribute](value)
                    setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()

    def do_EOF(self, line):
        """Handles End Of File character.
        """
        print()
        return True

    def do_quit(self, line):
        """Exits the program.
        """
        return True

    def emptyline(self):
        """Doesn't do anything on ENTER.
        """
        pass

    def do_create(self, line):
        """Creates an instance.
        """
        if line == "" or line is None:
            print("** class name missing **")
        elif line not in storage.classes():
            print("** class doesn't exist **")
        else:
            b = storage.classes()[line]()
            b.save()
            print(b.id)

    def do_show(self, line):
        """Prints the string representation of an instance.
        """
        if line == "" or line is None:
            print("** class name missing **")
        else:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(words[0], words[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[key])

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id.
        """
        if line == "" or line is None:
            print("** class name missing **")
        else:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(words[0], words[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[key]
                    storage.save()

    def do_all(self, line):
        """Prints all string representation of all instances.
        """
        if line != "":
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            else:
                text = [str(obj) for key, obj in storage.all().items()
                        if type(obj).__name__ == words[0]]
                print(text)
        else:
            text = [str(obj) for key, obj in storage.all().items()]
            print(text)

    def do_count(self, line):
        """Counts the instances of a class.
        """
        words = line.split(' ')
        if not words[0]:
            print("** class name missing **")
        elif words[0] not in storage.classes():
            print("** class doesn't exist **")
        else:
            matches = [
                k for k in storage.all() if k.startswith(
                    words[0] + '.')]
            print(len(matches))

    def do_update(self, line):
        """Updates an instance by adding or updating attribute.
        """
        if line == "" or line is None:
            print("** class name missing **")
            return

        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match = re.search(rex, line)
        classname = match.group(1)
        uid = match.group(2)
        attribute = match.group(3)
        value = match.group(4)
        if not match:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** no instance found **")
            elif not attribute:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:
                cast = None
                if not re.search('^".*"$', value):
                    if '.' in value:
                        cast = float
                    else:
                        cast = int
                else:
                    value = value.replace('"', '')
                attributes = storage.attributes()[classname]
                if attribute in attributes:
                    value = attributes[attribute](value)
                elif cast:
                    try:
                        value = cast(value)
                    except ValueError:
                        pass  # fine, stay a string then
                setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()
=======
""" console  """

import cmd
import models
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.amenity import Amenity
import shlex


classes_dict = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
                "Place": Place, "Review": Review, "State": State, "User": User}


class HBNBCommand(cmd.Cmd):
    """ Entry point of the command interpreter """
    collection_keys = classes_dict.keys()
    prompt = '(hbnb)'

    def do_quit(self, _input):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, _input):
        """Exits command console"""
        return True

    def emptyline(self):
        """An empty line + ENTER should not execute anything"""
        return False

    def do_create(self, _input_class_name):
        """Creates a new instance of BaseModel in JSON"""
        if not _input_class_name:
            print("** class name missing **")
            return
        if _input_class_name not in classes_dict.keys():
            print("** class doesn't exist **")
            return
        newinstance = classes_dict[_input_class_name]()
        newinstance.save()
        print(newinstance.id)

    def do_show(self, _input):
        """Prints the string representation of an instance
                  based on the class name and id"""
        input2 = _input
        if len(input2.split(' ')[0]) is 0:
            print("** class name missing **")
            return
        if input2.split(' ')[0] not in self.collection_keys:
            print("** class doesn't exist **")
            return
        if len(input2.split()) is 1:
            print("** instance id missing **")
            return
        models.storage.reload()
        for key, value in models.storage.all().items():
            if value.__class__.__name__ == input2.split(' ')[0] \
               and value.id == input2.split(' ')[1]:
                print(value.__str__())
                return
        print("** no instance found **")

    def do_destroy(self, _input):
        """Deletes an instance based on the class name and id
        """
        if len(_input.split(' ')[0]) is 0:
            print("** class name missing **")
            return
        if _input.split(' ')[0] not in self.collection_keys:
            print("** class doesn't exist **")
            return
        if len(_input.split(' ')) is 1:
            print("** instance id missing **")
            return
        class_name, class_id = (_input.split(' ')[0], _input.split(' ')[1])
        query_key = class_name + '.' + class_id
        if query_key not in models.storage.all().keys():
            print("** no instance found **")
            return
        del models.storage.all()[query_key]
        models.storage.save()

    def do_all(self, _input_class):
        """Prints all string representation of all instances
            based or not on the class name
        """

        if _input_class:
            if _input_class not in self.collection_keys:
                print("** class doesn't exist **")
                return

        for key_items in models.storage.all().keys():
            key_items = models.storage.all()[key_items]
            print(key_items)
        return

    def do_update(self, _input):
        """Updates an instance based on the class name and id by adding
           or updating attribute (save the change into the JSON file)
        """
        _input = shlex.split(_input)
        query_key = ''

        if len(_input) is 0:
            print("** class name missing **")
            return
        if _input[0] not in self.collection_keys:
            print("** class doesn't exist **")
            return
        if len(_input) is 1:
            print("** instance id missing **")
            return
        if len(_input) > 1:
            query_key = _input[0] + '.' + _input[1]
        if query_key not in models.storage.all().keys():
            print("** no instance found **")
            return
        if len(_input) is 2:
            print('** attribute name missing **')
            return
        if len(_input) is 3:
            print('** value missing **')
            return
        key_name = _input[2]
        input_value = _input[3]
        setattr(models.storage.all()[query_key], key_name, input_value)

        models.storage.all()[query_key].save()

    def default(self, inp):
        """Retrieve all instances class using: <class name>.all()"""
        count = 0
        words = inp.split(".")

        if words[0] in classes_dict and words[1] == "all()":
            self.do_all(words[0])
        elif words[0] in classes_dict and words[1] == "count()":
            if (words[0] not in classes_dict):
                print("** class doesn't exist **")
                return (False)
            else:
                for key in models.storage.all():
                    if key.startswith(words[0]):
                        count += 1
                print(count)
        else:
            print("*** Unknown syntax: {}".format(inp))
>>>>>>> refs/remotes/origin/main


if __name__ == '__main__':
    HBNBCommand().cmdloop()
