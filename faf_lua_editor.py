import luaparser
from luaparser import ast, astnodes
from luaparser.astnodes import Call, Invoke, LocalAssign, Name, Comment, Index
import os
from typing import Deque, List
import json

class FAFLuaEditor():
    def __init__(self, moho_sim_reference_json_path: str) -> None:
        self._up_method_to_moho_method = {}
        self._up_func_to_up_method_call = {}
        self._up_func_to_up_method = {}
        self._func_to_up_func = {}
        
        self._duplicate_func_names = set()

        self.setup_moho_functions(moho_sim_reference_json_path)

    def setup_moho_functions(self, moho_sim_reference_json_path: str):
        with open(moho_sim_reference_json_path, "r") as file:
            moho_references = json.load(file)
            for moho_file, moho_funcs in moho_references.items():

                moho_funcs = list(moho_funcs)

                method = moho_file[4:] + "Methods"
                if "<global>" in method:
                    method = method.replace("<global>", "Global")
                    moho_function = "_G"
                    # moho_function = "_G." + moho_funcs[-1]
                else:
                    moho_function = "_G." + moho_funcs[-1]

                self._up_method_to_moho_method[method] = moho_function
                # print(method, self._up_method_to_moho_method[method])

                for func in moho_funcs[:-1]:
                    up_func = method + func
                    # Some moho functions have the same name but belong to different sim classes. We can't differentiate
                    # between them automatically (yet), so we can't upvalue them (yet)
                    if func in self._func_to_up_func:
                        # If we find a duplicate function, we gotta remove it or else we might upvalue the wrong 
                        # function. Doing it like this, we can't remove the entries in the up_func_to_method[_call] 
                        # dicts, but that shouldn't cause any problems as they should never be accessed 
                        self._duplicate_func_names.add(func)
                        ## self._up_func_to_up_method.pop(up_func)
                        ## self._up_func_to_up_method_call.pop(up_func)
                        self._func_to_up_func.pop(func)
                        # print("found the duplicate function: ", func)
                    elif func in self._duplicate_func_names:
                        # print("Again found the duplicate function: ", func)
                        pass
                    else:
                        self._up_func_to_up_method[up_func] = method
                        self._up_func_to_up_method_call[up_func] = method + '.' + func
                        self._func_to_up_func[func] = up_func

                    # print(' ' * len(method), up_func, self._up_func_to_up_method[up_func])
                    # print(' ' * len(method), func, self._func_to_up_func[func])
            print("Found the following duplicate moho functions in %s"%moho_sim_reference_json_path)
            print("They are therefore skipped and won't be upvalued/optimized:")
            print(self._duplicate_func_names, "\n")

    def _reformat(self, content: str) -> str:
            chunk = ast.parse(content)
            # print(ast.to_pretty_str(chunk))
            return ast.to_lua_source(chunk)

    def _upvalue_moho_functions(self, content: str) -> str:
        chunk = ast.parse(content)
        # print(ast.to_pretty_str(chunk))
        up_methods_found = set()
        up_funcs_found = set()

        node_gen = ast.walk(chunk)
        blocks = []
        for node in node_gen:
            if node.display_name == 'Block': 
                # print("block found")
                blocks.append(node.body)

        for j in range(len(blocks)):
            block = blocks[j]
            for i in range(len(block)):
                statement = block[i]
                
                up_func = None
                if isinstance(statement, Invoke) and \
                        statement.func.id in self._func_to_up_func:
                    # Function calls with a colon are invokes in the parser, e.g. thingy:function(args)
                    up_func = self._func_to_up_func[statement.func.id]

                    # go through all the method calls that came before the final function call so that we can add them 
                    # as the explicit first argument of the function, which is what the colon invoke does implicitly
                    explicit_invoke_arg = ''
                    current_method = statement.source
                    while True:
                        try: 
                            explicit_invoke_arg = '.'.join(filter(None,[current_method.idx.id, explicit_invoke_arg]))
                            current_method = current_method.value
                        except AttributeError:
                            explicit_invoke_arg = '.'.join(filter(None,[current_method.id, explicit_invoke_arg]))
                            # current_method = statement_value.value
                            break
                    # The "[Name('self')]" part in the next line is a HAAAACK
                    new_statement = Call(Name(up_func), [Name(explicit_invoke_arg)] + statement.args, statement.comments)
                
                elif isinstance(statement, Call):
                    try: 
                        # Call of a function as a method, e.g. thingy.function(args)
                        func = statement.func.idx.id
                    except AttributeError: 
                        # Call of a function as variable(?) e.g. function(args)
                        func = statement.func.id
                    if func in self._func_to_up_func:
                        up_func = self._func_to_up_func[func]
                        new_statement = Call(Name(up_func), statement.args, statement.comments)

                if up_func is not None:
                    up_funcs_found.add(up_func)
                    up_method = self._up_func_to_up_method[up_func]
                    up_methods_found.add(up_method)
                    block[i] = new_statement
            
        # put upvalues at beginning of chunk
        def upvalue_comment_gen():
            # this is makes it so the first upvalue method has a comment, while all the other ones are separated 
            # by whitespace. A generator is overkill for that, but more fun than if statements :P
            n = 0 
            while True:
                if n == 0:
                    yield '-- Automatically upvalued moho functions for performance'
                else:
                    yield ''
                n += 1
        upvalue_comment = upvalue_comment_gen()
        upvalues = []
        for up_method in list(up_methods_found):
            upvalues.append(LocalAssign(
                [Name(up_method)], 
                [Name(self._up_method_to_moho_method[up_method])],
                [Comment(next(upvalue_comment))]))
            for up_func in list(up_funcs_found):
                if up_method in self._up_func_to_up_method[up_func]:
                    upvalues.append(LocalAssign(
                        [Name(up_func)], 
                        [Name(self._up_func_to_up_method_call[up_func])],
                        ))   
        if upvalues:
            first_block = chunk.body.body
            first_block[0].comments[0:0] = [Comment('-- End of automatically upvalued moho functions --'), 
                                            Comment('')]
            first_block[0:0] = upvalues
        
        return ast.to_lua_source(chunk)

    def reformat_file(self, filepath: str):
        # print("Opening %s"%filepath)
        with open(filepath, 'r+') as file:
            content = file.read()
            
            new_content = self._reformat(content)
            if new_content == content:
                print("Nothing to reformat in %s"%filepath)
            else:
                print("Reformating %s"%filepath)
                file.seek(0)
                file.write(new_content)
                file.truncate()
        return filepath

    def upvalue_moho_functions_in_file(self, filepath: str):
        # print("Opening %s"%filepath)
        with open(filepath, 'r+') as file:
            content = file.read()
            
            new_content = self._upvalue_moho_functions(content)
            if new_content == content:
                print("Nothing to upvalue in %s"%filepath)
            else:
                print("Upvalue %s"%filepath)
                file.seek(0)
                file.write(new_content)
                file.truncate()
        return filepath

if __name__ == "__main__":
    # # rootdirs = ["../FAForever_GitHub/units"]
    # # rootdirs = ["../FAForever_GitHub/projectiles"]
    # rootdirs = ["../FAForever_GitHub/units", "../FAForever_GitHub/projectiles"]
    # filepaths = []
    # for rootdir in rootdirs:
    #     for subdir, dirs, files in os.walk(rootdir):
    #         # print(files)
    #         for file in files:
    #             if file.endswith(".lua"):
    #                 file_path = os.path.join(subdir, file)
    #                 filepaths.append(file_path)
    #                 # print(file_path)

    # filepaths = ["../FAForever_GitHub/units/DRA0202/DRA0202_Script.lua"]
    # filepaths = ["../FAForever_GitHub/units/UAB1104/UAB1104_Script.lua"]
    # filepaths = ["faf_lua_for_testing.lua"]
    filepaths = ["lua_for_testing.lua"]

    editor = FAFLuaEditor(moho_sim_reference_json_path = "moho_sim_reference_removed_unsafe.json")

    failed_files = []
    for file_path in filepaths:
        try:
            print("\nOpening ", file_path)
            editor.reformat_file(file_path)
            # editor.upvalue_moho_functions_in_file(file_path)
            # print(file_path)
        except:
            failed_files.append(file_path)
            print("FAILED editing/upvaluing ", file_path)

    if failed_files:
        print("\nfailed and hence skipped files:\n", failed_files)
    else:
        print("Editing/Optimizing worked for ALL files!")
    # print("it worked!")

# ---------
# Notes for the moho_sim_reference changes:
# 
# Removed all the User and Core functions as we probably don't want to touch them anyway
# 
# Removed all the "base" functions and all the functions with "_c_" in the name (only "_c_CreateEntity" 
# and "_c_CreateShield") as touching either of them can hard crash the game for some reason
# 