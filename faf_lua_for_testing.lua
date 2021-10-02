--****************************************************************************
--**
--**  File     :  /cdimage/units/DRA0202/DRA0202_script.lua
--**  Author(s):  Dru Staltman, Eric Williamson
--**
--**  Summary  :  Cybran Bomber Fighter Script
--**
--**  Copyright © 2005 Gas Powered Games, Inc.  All rights reserved.
--****************************************************************************

local CAirUnit = import('/lua/cybranunits.lua').CAirUnit
local CAAMissileNaniteWeapon = import('/lua/cybranweapons.lua').CAAMissileNaniteWeapon

DRA0202 = Class(CAirUnit) {
    self.unit:SetSpeedMult(1.0),
}
