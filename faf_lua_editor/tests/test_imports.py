import unittest

class ImportsTestCase(unittest.TestCase):
    def test_luaparser_imports(self):
        import luaparser
    
    def test_faf_lua_editor_relative_class_import(self):
        import faf_lua_editor
        from faf_lua_editor import FAFLuaEditor
