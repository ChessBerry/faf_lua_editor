import luaparser
from luaparser import ast, astnodes
import json

file_test_input_path = "lua_for_testing.lua"
# file_test_input_path = "faf_lua_for_testing.lua"
# file_test_input_path = "../FAForever_GitHub/engine/Sim/Unit.lua"
# file_test_input_path = "../FAForever_GitHub/lua/sim/defaultweapons.lua"

# for filename in os.listdir(directory):

file_test_output_path = "new_file_test.lua"

up_methods_found = set()
up_funcs_found = set()
with open(file_test_input_path, 'r') as file:
    content = file.read()
    chunk = ast.parse(content)
    # print(ast.to_pretty_str(chunk))

    node_gen = ast.walk(chunk)
    # print(node_gen.__next__)
    blocks = []
    for node in node_gen:
        # if node.display_name == 'Invoke': 
        #     funcs.append(node)
        if node.display_name == 'Block': 
            blocks.append(node.body)
        
        # print(node is chunk.body.body[1])
        # # print(node.display_name)
        # try:
        #     print(node.id)
        # except AttributeError:
        #     pass

    block = blocks[0]
    # print(chunk.body.body is block)
    # block[0], block[1] = block[1], block[0]
    # block[2].func.id = 'Oh_shit_I_changed_this_from_the_walker'
    # print(chunk.body.body is block)

    # visitor =  ast.WalkVisitor()
    # visitor.visit(chunk)
    # chunk2 = visitor.nodes[0]
    # print(ast.to_pretty_str(chunk2)) 
    # chunk2.body.body[0], chunk2.body.body[1] = chunk2.body.body[1], chunk2.body.body[0]
    # print(ast.to_pretty_str(chunk2))

    # chunk.body.body[0], chunk.body.body[1] = chunk.body.body[1], chunk.body.body[0]
    # print(ast.to_pretty_str(chunk))

    new_file = ast.to_lua_source(chunk)

with open(file_test_output_path, 'w') as file:
    file.write(new_file)

print("it worked!")
