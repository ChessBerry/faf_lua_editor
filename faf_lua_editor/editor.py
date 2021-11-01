import luaparser
from luaparser import ast, astnodes
from luaparser.astnodes import Call, Invoke, LocalAssign, Name, Comment, Index
import os
from typing import Deque, List
import json
import importlib_resources

class FAFLuaEditor():
    def __init__(self) -> None:
        self._up_method_to_moho_method = {}
        self._up_func_to_up_method_call = {}
        self._up_func_to_up_method = {}
        self._func_to_up_func = {}

        self._moho_sim_reference_json_path = 'moho_reference/moho_sim_reference_removed_unsafe.json'
        
        self._duplicate_func_names = set()

        self.setup_moho_functions()

    def setup_moho_functions(self):
        ref = importlib_resources.files("faf_lua_editor").joinpath(self._moho_sim_reference_json_path)
        # pd.read_csv(stream, encoding='latin-1')
        # json.load(stream)

        with ref.open("rb") as file:
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
            print("Found the following duplicate moho functions in %s"%self._moho_sim_reference_json_path)
            print("They are therefore skipped and won't be upvalued/optimized:")
            print(self._duplicate_func_names, "\n")

    def _reformat(self, content: str) -> str:
            chunk = ast.parse(content)
            # print(ast.to_pretty_str(chunk))
            return ast.to_lua_source(chunk)

    def create_new_statement_for_invoke_upvalue(self, statement, up_funcs: List, new_statements:List):
        
        # go through all the method calls that came before the final function call so that we can add them 
        # as the explicit first argument of the function, which is what the colon invoke does implicitly
        explicit_invoke_first_arg = ''
        current_method = statement.source
        if isinstance(current_method, Invoke) and statement.func.id in self._func_to_up_func:
            # Current Method is another invoke
            explicit_invoke_first_arg = self.create_new_statement_for_invoke_upvalue(current_method, up_funcs, new_statements)
        else:
            # this try except stuff is needed because there is no consistent way to get the string 
            # representation from a node. I should add this, it would reduce this entire function 
            # to like 10 lines, with comments.
            # Also the stuff below doesn't generalize to an arbitrary recursion level, even though it should and 
            # implementing that would be trivial with an easy way to get the right string from a node
            while True:
                # if isinstance(current_method, Index): # Doesn't work as most things are somehow called "index"..
                try:
                    is_a_number_index = current_method.idx.display_name == 'Number'
                    if not is_a_number_index: raise AttributeError
                    # Current method is the index part of a table or something, e.g. something like Beams[1]
                    try:
                        explicit_invoke_first_arg = '.'.join(filter(None,[current_method.value.idx.id + '[' + str(current_method.idx.n) + ']', explicit_invoke_first_arg]))
                        # NOTE: This will fail if the index is not a number! Rewriting this is needed anyway though
                        # As the index '[1]' and the table 'Beams' are treated as separate we need to go up two steps .value
                        # calls here
                        current_method = current_method.value.value
                    except AttributeError:
                        # Current method is the main table or otherwise indexed thing
                        explicit_invoke_first_arg = '.'.join(filter(None,[current_method.value.id + '[' + str(current_method.idx.n) + ']', explicit_invoke_first_arg]))
                        # NOTE: This will fail if the index is not a number! Rewriting this is needed anyway though
                        break
                except AttributeError:
                    try:
                        # Current method is an element of another class
                        explicit_invoke_first_arg = '.'.join(filter(None,[current_method.idx.id, explicit_invoke_first_arg]))
                        current_method = current_method.value
                    except AttributeError:
                        try:
                            # Current method is the main class or function being called
                            explicit_invoke_first_arg = '.'.join(filter(None,[current_method.id, explicit_invoke_first_arg]))
                            break
                        except AttributeError:
                            # Current Method is an invoke straight after a function call
                            func_args = []
                            for arg in current_method.args:
                                try:
                                    func_args.append(arg.id) # variable
                                    # break
                                except AttributeError:
                                    try:
                                        func_args.append(str(arg.n)) # number
                                        # break
                                    except AttributeError:
                                        try:
                                            func_args.append(arg.s) # string
                                            # break
                                        except AttributeError:
                                            if arg.notation.name == 'SQUARE': 
                                                index_notation_left = '['
                                                index_notation_right = ']'
                                            else:
                                                index_notation_left = '.'
                                                index_notation_right = ''      
                                            try:
                                                # table being indexed with a variable
                                                # NOTE: Fails for more than one index (if that is possible?)
                                                try:
                                                    func_args.append(arg.value.idx.id + index_notation_left + str(arg.idx.id) + index_notation_right)
                                                    # current_method = current_method.value
                                                except AttributeError:
                                                    func_args.append(arg.value.id + index_notation_left + str(arg.idx.id) + index_notation_right)
                                                    # break
                                            except AttributeError:
                                                # table being indexed with a number
                                                # NOTE: Fails for more than one index (if that is possible?)
                                                try:
                                                    func_args.append(arg.value.idx.id + index_notation_left + str(arg.idx.n) + index_notation_right)
                                                    # current_method = current_method.value
                                                except AttributeError:
                                                    func_args.append(arg.value.id + index_notation_left + str(arg.idx.n) + index_notation_right)
                                                    # break
                            explicit_invoke_first_arg = '.'.join(filter(None,[current_method.func.id + '(' + ', '.join(func_args) + ')', explicit_invoke_first_arg]))
                            break
        func = statement.func.id
        if func in self._func_to_up_func:
            up_func = self._func_to_up_func[func]
            up_funcs.append(up_func)
            new_statements.append(Call(Name(up_func), [Name(explicit_invoke_first_arg)] + statement.args, statement.comments))
        else:
            # If the func can't be upvalued, don't change the statement at all
            new_statements.append(statement)
        
        return explicit_invoke_first_arg

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
                
                up_funcs = []
                # up_methods = []
                new_statements = []

                # Note that functions are cycled through right to left
                if isinstance(statement, Invoke) and statement.func.id in self._func_to_up_func:
                    # Function calls with a colon are invokes in the parser, e.g. thingy:function(args)

                    self.create_new_statement_for_invoke_upvalue(statement, up_funcs, new_statements)
                    
                    if up_funcs:
                        up_funcs_found.update(up_funcs)
                        up_methods = []
                        for func in up_funcs:
                            up_methods.append(self._up_func_to_up_method[func])
                        up_methods_found.update(up_methods)
                        block[i] = new_statements[0]
                        for stat in reversed(new_statements[1:]):
                            block.insert(i+1, stat)
            
                
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

                        up_funcs_found.add(up_func)
                        up_method = self._up_func_to_up_method[up_func]
                        up_methods_found.add(up_method)
                        block[i] = new_statement
            
        # put upvalues at beginning of chunk
        def upvalue_comment_gen():
            # this makes it so the first upvalue method has a comment, while all the other ones are separated 
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

        # Turn the sets into lists and sort them so that order of upvalued functions and hence the AST is always 
        # reproducible
        up_methods_found = list(up_methods_found)
        up_methods_found.sort()
        up_funcs_found = list(up_funcs_found)
        up_funcs_found.sort()
        for up_method in up_methods_found:
            upvalues.append(LocalAssign(
                [Name(up_method)], 
                [Name(self._up_method_to_moho_method[up_method])],
                [Comment(next(upvalue_comment))]))
            for up_func in up_funcs_found:
                if up_method in self._up_func_to_up_method[up_func]:
                    upvalues.append(LocalAssign(
                        [Name(up_func)], 
                        [Name(self._up_func_to_up_method_call[up_func])],
                        ))   
        if upvalues:
            first_block = chunk.body.body
            first_block[0].comments[0:0] = [Comment('-- End of automatically upvalued moho functions'), 
                                            Comment('')]
            first_block[0:0] = upvalues
        
        return ast.to_lua_source(chunk)

    def reformat_file(self, filepath: str):
        """ Transform the file into an AST and then generate lua code from it"""
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
