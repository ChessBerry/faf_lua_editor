import unittest
import textwrap
from faf_lua_editor import FAFLuaEditor

class FAFLuaEditorTestCase(unittest.TestCase):
    def setUp(self):
        self.editor = FAFLuaEditor()

    def test_upvalue_call(self):
        source = textwrap.dedent('''\
            self.SetBreakOffTriggerMult(1)''')
        expect = textwrap.dedent('''\
            -- Automatically upvalued moho functions for performance
            local UnitMethods = _G.moho.unit_methods
            local UnitMethodsSetBreakOffTriggerMult = UnitMethods.SetBreakOffTriggerMult
            -- End of automatically upvalued moho functions

            UnitMethodsSetBreakOffTriggerMult(1)''')
        result = self.editor._upvalue_moho_functions(source)
        self.assertEqual(expect, result)

    def test_upvalue_chained_calls(self):
        source = textwrap.dedent('''\
            self.meh.foo.bar.SetBreakOffTriggerMult(1)''')
        expect = textwrap.dedent('''\
            -- Automatically upvalued moho functions for performance
            local UnitMethods = _G.moho.unit_methods
            local UnitMethodsSetBreakOffTriggerMult = UnitMethods.SetBreakOffTriggerMult
            -- End of automatically upvalued moho functions

            UnitMethodsSetBreakOffTriggerMult(1)''')
        result = self.editor._upvalue_moho_functions(source)
        self.assertEqual(expect, result)

    def test_upvalue_invoke(self):
        source = textwrap.dedent('''\
            self:SetBreakOffTriggerMult(1)''')
        expect = textwrap.dedent('''\
            -- Automatically upvalued moho functions for performance
            local UnitMethods = _G.moho.unit_methods
            local UnitMethodsSetBreakOffTriggerMult = UnitMethods.SetBreakOffTriggerMult
            -- End of automatically upvalued moho functions

            UnitMethodsSetBreakOffTriggerMult(self, 1)''')
        result = self.editor._upvalue_moho_functions(source)
        self.assertEqual(expect, result)

    def test_upvalue_chained_invokes(self):
        source = textwrap.dedent('''\
            self.unit:SetBreakOffTriggerMult(3):SetBreakOffDistanceMult(4)''')
        expect = textwrap.dedent('''\
            -- Automatically upvalued moho functions for performance
            local UnitMethods = _G.moho.unit_methods
            local UnitMethodsSetBreakOffDistanceMult = UnitMethods.SetBreakOffDistanceMult
            local UnitMethodsSetBreakOffTriggerMult = UnitMethods.SetBreakOffTriggerMult
            -- End of automatically upvalued moho functions

            UnitMethodsSetBreakOffTriggerMult(self.unit, 3)
            UnitMethodsSetBreakOffDistanceMult(self.unit, 4)''')
        result = self.editor._upvalue_moho_functions(source)
        self.assertEqual(expect, result)

    def test_upvalue_chained_invokes_2(self):
        source = textwrap.dedent('''\
            self.unit:SetBreakOffTriggerMult(3):SetBreakOffDistanceMult(4):SetBreakOffTriggerMult(5)''')
        expect = textwrap.dedent('''\
            -- Automatically upvalued moho functions for performance
            local UnitMethods = _G.moho.unit_methods
            local UnitMethodsSetBreakOffDistanceMult = UnitMethods.SetBreakOffDistanceMult
            local UnitMethodsSetBreakOffTriggerMult = UnitMethods.SetBreakOffTriggerMult
            -- End of automatically upvalued moho functions

            UnitMethodsSetBreakOffTriggerMult(self.unit, 3)
            UnitMethodsSetBreakOffDistanceMult(self.unit, 4)
            UnitMethodsSetBreakOffTriggerMult(self.unit, 5)''')
        result = self.editor._upvalue_moho_functions(source)
        self.assertEqual(expect, result)

    def test_upvalue_calls_and_invokes(self):
        source = textwrap.dedent('''\
            self.SetBreakOffTriggerMult(1)
            self:SetBreakOffDistanceMult(2)
            self.unit:SetSpeedMult(3)''')
        expect = textwrap.dedent('''\
            -- Automatically upvalued moho functions for performance
            local UnitMethods = _G.moho.unit_methods
            local UnitMethodsSetBreakOffDistanceMult = UnitMethods.SetBreakOffDistanceMult
            local UnitMethodsSetBreakOffTriggerMult = UnitMethods.SetBreakOffTriggerMult
            local UnitMethodsSetSpeedMult = UnitMethods.SetSpeedMult
            -- End of automatically upvalued moho functions

            UnitMethodsSetBreakOffTriggerMult(1)
            UnitMethodsSetBreakOffDistanceMult(self, 2)
            UnitMethodsSetSpeedMult(self.unit, 3)''')
        result = self.editor._upvalue_moho_functions(source)
        self.assertEqual(expect, result)

    def test_upvalue_some_calls_and_chained_invokes(self):
        source = textwrap.dedent('''\
            self.unit:SetBreakOffTriggerMult(1)
            self.unit:SetBreakOffDistanceMult(2)
            self.unit:SetBreakOffTriggerMult(3):SetBreakOffDistanceMult(4)''')
        expect = textwrap.dedent('''\
            -- Automatically upvalued moho functions for performance
            local UnitMethods = _G.moho.unit_methods
            local UnitMethodsSetBreakOffDistanceMult = UnitMethods.SetBreakOffDistanceMult
            local UnitMethodsSetBreakOffTriggerMult = UnitMethods.SetBreakOffTriggerMult
            -- End of automatically upvalued moho functions

            UnitMethodsSetBreakOffTriggerMult(self.unit, 1)
            UnitMethodsSetBreakOffDistanceMult(self.unit, 2)
            UnitMethodsSetBreakOffTriggerMult(self.unit, 3)
            UnitMethodsSetBreakOffDistanceMult(self.unit, 4)''')
        result = self.editor._upvalue_moho_functions(source)
        self.assertEqual(expect, result)

    def test_upvalue_indexed_thing_invoking_1(self):
        source = textwrap.dedent('''\
            Beams[1]:SetAmbientSound()''')
        expect = textwrap.dedent('''\
            -- Automatically upvalued moho functions for performance
            local EntityMethods = _G.moho.entity_methods
            local EntityMethodsSetAmbientSound = EntityMethods.SetAmbientSound
            -- End of automatically upvalued moho functions

            EntityMethodsSetAmbientSound(Beams[1])''')
        result = self.editor._upvalue_moho_functions(source)
        self.assertEqual(expect, result)

    def test_upvalue_indexed_thing_invoking_2(self):
        source = textwrap.dedent('''\
            self.Beams[1]:SetAmbientSound()''')
        expect = textwrap.dedent('''\
            -- Automatically upvalued moho functions for performance
            local EntityMethods = _G.moho.entity_methods
            local EntityMethodsSetAmbientSound = EntityMethods.SetAmbientSound
            -- End of automatically upvalued moho functions

            EntityMethodsSetAmbientSound(self.Beams[1])''')
        result = self.editor._upvalue_moho_functions(source)
        self.assertEqual(expect, result)

    def test_upvalue_indexed_thing_invoking_3(self):
        source = textwrap.dedent('''\
            thingy[23].meh.Beams[1].lights[1123]:SetAmbientSound()''')
        expect = textwrap.dedent('''\
            -- Automatically upvalued moho functions for performance
            local EntityMethods = _G.moho.entity_methods
            local EntityMethodsSetAmbientSound = EntityMethods.SetAmbientSound
            -- End of automatically upvalued moho functions

            EntityMethodsSetAmbientSound(thingy[23].meh.Beams[1].lights[1123])''')
        result = self.editor._upvalue_moho_functions(source)
        self.assertEqual(expect, result)