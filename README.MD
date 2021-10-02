## README - FAF Lua Editor

This repository contains the python 3 code for the faf lua editor, a set of scripts to reformat and optimize the lua code of [FAForever](https://github.com/FAForever/fa).

To do this, we generate and then manipulate an abstract syntax tree from the lua code via the py-lua-parser package. As FAF Lua uses a slightly [different syntax](https://github.com/FAForever/lua-lang/blob/lua-5.0/HISTORY) than base Lua5.0, we modified the luaparser to work with this changed syntax.  
Having the [FAF_lua_support](https://github.com/ChessBerry/py-lua-parser/tree/faf_lua_support) branch of the py-lua-parser installed is therefore required for the code in this repository to work.

For questions or contribution ideas [write me](cheeseberry@protonmail.com) or message me in discord at Cheeseberry#1965.
