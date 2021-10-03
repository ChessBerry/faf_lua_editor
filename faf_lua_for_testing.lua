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
}