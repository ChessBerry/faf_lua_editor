import unittest
import textwrap
from faf_lua_editor import FAFLuaEditor

class FAFLuaEditorTestCase(unittest.TestCase):
    def setUp(self):
        self.editor = FAFLuaEditor()

    def tearDown(self):
        del self.editor

    def test_reformat_lots_of_stuff_at_once(self):
        source = textwrap.dedent('''\
            DRA0202 = Class(CAirUnit) {
                Weapons = {
                    AntiAirMissiles = Class(CAAMissileNaniteWeapon) {},
                    GroundMissile = Class(CIFMissileCorsairWeapon) {
                    
                IdleState = State (CIFMissileCorsairWeapon.IdleState) {
                Main = function(self)
                    CIFMissileCorsairWeapon.IdleState.Main(self)
                end,
                            
                OnGotTarget = function(self)
                    if self.unit:IsUnitState('Moving') then
                    self.unit:SetSpeedMult(1.0)
                    else
                    self.unit:SetBreakOffTriggerMult(2.0)
                    self.unit:SetBreakOffDistanceMult(8.0)
                    self.unit:SetSpeedMult(0.67)
                    CIFMissileCorsairWeapon.IdleState.OnGotTarget(self)
                    end
                end,            
                },
                    
                OnGotTarget = function(self)
                    if self.unit:IsUnitState('Moving') then
                    self.unit:SetSpeedMult(1.0)
                    else
                    self.unit:SetBreakOffTriggerMult(2.0)
                    self.unit:SetBreakOffDistanceMult(8.0)
                    self.unit:SetSpeedMult(0.67)
                    CIFMissileCorsairWeapon.OnGotTarget(self)
                    end
                end,
                    
                OnLostTarget = function(self)
                    self.unit:SetBreakOffTriggerMult(1.0)
                    self.unit:SetBreakOffDistanceMult(1.0)
                    self.unit:SetSpeedMult(1.0)
                    CIFMissileCorsairWeapon.OnLostTarget(self)
                end,
                    },
                },
            }''')
        exp = textwrap.dedent('''\
            DRA0202 = Class(CAirUnit)({
                Weapons = {
                        AntiAirMissiles = Class(CAAMissileNaniteWeapon)({
                        }),
                        GroundMissile = Class(CIFMissileCorsairWeapon)({

                                    IdleState = State(CIFMissileCorsairWeapon.IdleState)({
                                                    Main = function(self)
                                                        CIFMissileCorsairWeapon.IdleState.Main(self)
                                                    end,

                                                    OnGotTarget = function(self)
                                                        if self.unit:IsUnitState('Moving') then
                                                            self.unit:SetSpeedMult(1.0)
                                                        else
                                                            self.unit:SetBreakOffTriggerMult(2.0)
                                                            self.unit:SetBreakOffDistanceMult(8.0)
                                                            self.unit:SetSpeedMult(0.67)
                                                            CIFMissileCorsairWeapon.IdleState.OnGotTarget(self)
                                                        end
                                                    end,
                                    }),

                                    OnGotTarget = function(self)
                                        if self.unit:IsUnitState('Moving') then
                                            self.unit:SetSpeedMult(1.0)
                                        else
                                            self.unit:SetBreakOffTriggerMult(2.0)
                                            self.unit:SetBreakOffDistanceMult(8.0)
                                            self.unit:SetSpeedMult(0.67)
                                            CIFMissileCorsairWeapon.OnGotTarget(self)
                                        end
                                    end,

                                    OnLostTarget = function(self)
                                        self.unit:SetBreakOffTriggerMult(1.0)
                                        self.unit:SetBreakOffDistanceMult(1.0)
                                        self.unit:SetSpeedMult(1.0)
                                        CIFMissileCorsairWeapon.OnLostTarget(self)
                                    end,
                        }),
                },
            })''')
        self.assertEqual(exp, self.editor._reformat(source))

    def test_upvalue_lots_of_stuff_at_once(self):
        source = textwrap.dedent('''\
            DRA0202 = Class(CAirUnit)({
                Weapons = {
                        AntiAirMissiles = Class(CAAMissileNaniteWeapon)({
                        }),
                        GroundMissile = Class(CIFMissileCorsairWeapon)({

                                    IdleState = State(CIFMissileCorsairWeapon.IdleState)({
                                                    Main = function(self)
                                                        CIFMissileCorsairWeapon.IdleState.Main(self)
                                                    end,

                                                    OnGotTarget = function(self)
                                                        if self.unit:IsUnitState('Moving') then
                                                            self.unit:SetSpeedMult(1.0)
                                                        else
                                                            self.unit:SetBreakOffTriggerMult(2.0)
                                                            self.unit:SetBreakOffDistanceMult(8.0)
                                                            self.unit:SetSpeedMult(0.67)
                                                            CIFMissileCorsairWeapon.IdleState.OnGotTarget(self)
                                                        end
                                                    end,
                                    }),

                                    OnGotTarget = function(self)
                                        if self.unit:IsUnitState('Moving') then
                                            self.unit:SetSpeedMult(1.0)
                                        else
                                            self.unit:SetBreakOffTriggerMult(2.0)
                                            self.unit:SetBreakOffDistanceMult(8.0)
                                            self.unit:SetSpeedMult(0.67)
                                            CIFMissileCorsairWeapon.OnGotTarget(self)
                                        end
                                    end,

                                    OnLostTarget = function(self)
                                        self.unit:SetBreakOffTriggerMult(1.0)
                                        self.unit:SetBreakOffDistanceMult(1.0)
                                        self.unit:SetSpeedMult(1.0)
                                        CIFMissileCorsairWeapon.OnLostTarget(self)
                                    end,
                        }),
                },
            })''')
        expect = textwrap.dedent('''\
            -- Automatically upvalued moho functions for performance
            local UnitMethods = _G.moho.unit_methods
            local UnitMethodsSetBreakOffDistanceMult = UnitMethods.SetBreakOffDistanceMult
            local UnitMethodsSetBreakOffTriggerMult = UnitMethods.SetBreakOffTriggerMult
            local UnitMethodsSetSpeedMult = UnitMethods.SetSpeedMult
            -- End of automatically upvalued moho functions

            DRA0202 = Class(CAirUnit)({
                Weapons = {
                        AntiAirMissiles = Class(CAAMissileNaniteWeapon)({
                        }),
                        GroundMissile = Class(CIFMissileCorsairWeapon)({

                                    IdleState = State(CIFMissileCorsairWeapon.IdleState)({
                                                    Main = function(self)
                                                        CIFMissileCorsairWeapon.IdleState.Main(self)
                                                    end,

                                                    OnGotTarget = function(self)
                                                        if self.unit:IsUnitState('Moving') then
                                                            UnitMethodsSetSpeedMult(self.unit, 1.0)
                                                        else
                                                            UnitMethodsSetBreakOffTriggerMult(self.unit, 2.0)
                                                            UnitMethodsSetBreakOffDistanceMult(self.unit, 8.0)
                                                            UnitMethodsSetSpeedMult(self.unit, 0.67)
                                                            CIFMissileCorsairWeapon.IdleState.OnGotTarget(self)
                                                        end
                                                    end,
                                    }),

                                    OnGotTarget = function(self)
                                        if self.unit:IsUnitState('Moving') then
                                            UnitMethodsSetSpeedMult(self.unit, 1.0)
                                        else
                                            UnitMethodsSetBreakOffTriggerMult(self.unit, 2.0)
                                            UnitMethodsSetBreakOffDistanceMult(self.unit, 8.0)
                                            UnitMethodsSetSpeedMult(self.unit, 0.67)
                                            CIFMissileCorsairWeapon.OnGotTarget(self)
                                        end
                                    end,

                                    OnLostTarget = function(self)
                                        UnitMethodsSetBreakOffTriggerMult(self.unit, 1.0)
                                        UnitMethodsSetBreakOffDistanceMult(self.unit, 1.0)
                                        UnitMethodsSetSpeedMult(self.unit, 1.0)
                                        CIFMissileCorsairWeapon.OnLostTarget(self)
                                    end,
                        }),
                },
            })''')
        result = self.editor._upvalue_moho_functions(source)
        self.assertEqual(expect, result)
