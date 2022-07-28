#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2022 Christopher J. Kucera
# <cj@apocalyptech.com>
# <http://apocalyptech.com/contact.php>
#
# This Wonderlands Hotfix Mod is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# This Wonderlands Hotfix Mod is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this Wonderlands Hotfix Mod.  If not, see
# <https://www.gnu.org/licenses/>.

import sys
sys.path.append('../../../python_mod_helpers')
from wldata.wldata import WLData
from wlhotfixmod.wlhotfixmod import Mod, BVCF, Balance

data = WLData()

mod = Mod('no_wasted_equipment.wlhotfix',
        'No Wasted Equipment',
        'Apocalyptech',
        [
            "Adjust the character-specific weighting so that you won't get",
            "class-specific gear for classes that you're not currently",
            "playing.  Theoretically this should work just fine in multiplayer,",
            "though I haven't tested it at all in that mode.",
            "",
            "Note that this does *not* affect specific gear drops from named",
            "enemies, should that matter at all.",
            # TODO: ^ figure that out.
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='0.9.0',
        cats='loot-system, gameplay',
        )

# Default values here are 0.25
mod.header('Update base character weighting')
for row, val in [
        ('CharacterWeights_Base', 0),
        # Don't want to go *all* the way to zero for the secondary
        # char, otherwise advanced-level gear won't have a secondary
        # class prior to speccing into a second class.  This should
        # make the secondary class be a near-guaranteed lock for
        # the secondary part, though, once it's enabled, and will
        # give an even chance for all other classes before then.
        ('CharacterWeights_Secondary', 0.0001),
        ]:
    mod.table_hotfix(Mod.PATCH, '',
            '/Game/GameData/Economy/Economy_Miscellaneous',
            row,
            'Value',
            BVCF(bvc=val))
mod.newline()

# Armor secondary-class unlocking -- the default behavior ends up unlocking
# in pairs (based on an unlocked Secondary Body part), which isn't really
# what we want with this mod.
mod.header('Unlocking Armor Second Class')
for part in [
        'Part_P_Class_Secondary_Barbarian',
        'Part_P_Class_Secondary_GunMage',
        'Part_P_Class_Secondary_Knight',
        'Part_P_Class_Secondary_Necromancer',
        'Part_P_Class_Secondary_Ranger',
        'Part_P_Class_Secondary_Rogue',
        ]:
    mod.reg_hotfix(Mod.PATCH, '',
            f'/Game/Gear/Pauldrons/_Shared/_Design/Parts/Class/Secondary/{part}',
            'Dependencies',
            '()')
mod.newline()

# Amulets -- by default these don't take the currently-used classes into
# account at all!
amulet_part_mapping = {
        'Part_Amulet_ClassStat_Barbarian': '/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Barb',
        'Part_Amulet_ClassStat_GunMage': '/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_GunMage',
        'Part_Amulet_ClassStat_KotC': '/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Knight',
        'Part_Amulet_ClassStat_Necromancer': '/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Necro',
        'Part_Amulet_ClassStat_Ranger': '/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Ranger',
        'Part_Amulet_ClassStat_Rogue': '/Game/GameData/Loot/CharacterWeighting/Att_CharacterWeight_ArmorUsers_Rogue',
        }
mod.header('Amulet Class-locking')
for obj_name in [
        '/Game/Gear/Amulets/_Shared/_Design/Balance/Balance_Amulets_01_Common',
        '/Game/Gear/Amulets/_Shared/_Design/Balance/Balance_Amulets_02_Uncommon',
        '/Game/Gear/Amulets/_Shared/_Design/Balance/Balance_Amulets_03_Rare',
        '/Game/Gear/Amulets/_Shared/_Design/Balance/Balance_Amulets_04_VeryRare',
        '/Game/Gear/Amulets/_Shared/_Unique/BlazeOfGlory/Balance/Balance_Amulet_Unique_BlazeOfGlory',
        '/Game/Gear/Amulets/_Shared/_Unique/Bradluck/Balance/Balance_Amulet_Unique_Bradluck',
        '/Game/Gear/Amulets/_Shared/_Unique/Frenzied/Balance/Balance_Amulet_Unique_Frenzied',
        '/Game/Gear/Amulets/_Shared/_Unique/Harbinger/Balance/Balance_Amulet_Unique_Harbinger',
        '/Game/Gear/Amulets/_Shared/_Unique/JointTraining/Balance/Balance_Amulet_Unique_JointTraining',
        '/Game/Gear/Amulets/_Shared/_Unique/OverflowBloodbag/Balance_Amulets_OverflowBloodbag',
        '/Game/Gear/Amulets/_Shared/_Unique/SacSkeep/Balance_Amulets_SacSkeep',
        '/Game/Gear/Amulets/_Shared/_Unique/Theruge/Balance/Balance_Amulet_Unique_Theruge',
        '/Game/Gear/Amulets/_Shared/_Unique/UniversalSoldier/Balance/Balance_Amulet_Unique_UniversalSoldier',
        '/Game/PatchDLC/Indigo1/Gear/Amulets/_Shared/_Unique/SlipnStun/Balance/Balance_Amulet_Unique_SlipnStun',
        '/Game/PatchDLC/Indigo2/Gear/Amulets/_Shared/_Unique/Barboload/Balance/Balance_Amulet_Unique_Barboload',
        '/Game/PatchDLC/Indigo3/Gear/Amulets/_Shared/_Unique/PracticalFocus/Balance/Balance_Amulet_Unique_PracticalFocus',

        # This one is apparently hard-locked to Clawbringers (handled below)
        #'/Game/Gear/Amulets/_Shared/_Unique/GTFO/Balance/Balance_Amulet_Unique_GTFO',

        # This one is apparently hard-locked to Spore Wardens (handled below)
        #'/Game/Gear/Amulets/_Shared/_Unique/RonRivote/Balance/Balance_Amulet_Unique_RonRivote',

        # These are already locked by char
        #'/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Barb',
        #'/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_KotC',
        #'/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Necro',
        #'/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_GunMage',
        #'/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Ranger',
        #'/Game/Gear/Amulets/_Shared/_Unique/HarmoniousDingleDangle/Balance/Balance_Amulet_Unique_Plot05_HDD_Rogue',
        ]:

    # We could make use of the Balance class, but that's a bit too high-level
    # for us, and I'm content to not bother with processing categories here.
    # Just looking to update the weights, is all.
    short_name = obj_name.rsplit('/', 1)[-1]
    obj_data = data.get_data(obj_name)[0]
    seen_header = False
    for idx, part in enumerate(obj_data['RuntimePartList']['AllParts']):
        if 'export' not in part['PartData'] and part['PartData'][0] in amulet_part_mapping:
            if not seen_header:
                mod.comment(short_name)
                seen_header = True
            mod.reg_hotfix(Mod.PATCH, '',
                    obj_name,
                    f'RuntimePartList.AllParts.AllParts[{idx}].Weight',
                    BVCF(bva=amulet_part_mapping[part['PartData'][0]]))
    if seen_header:
        mod.newline()

# A couple of amulets are straight-up class-locked.  They do make *sense* that way, in terms
# of their effects, but there's no reason why other classes couldn't make use of them too.
# So: unlocks!  We *will* be making use of the Balance class to do this one.
mod.header('Amulet Class Expansions')
for label, obj_path in [
        ("Rivolte's Amulet", '/Game/Gear/Amulets/_Shared/_Unique/RonRivote/Balance/Balance_Amulet_Unique_RonRivote'),
        ("Vorcanar's Cog", '/Game/Gear/Amulets/_Shared/_Unique/GTFO/Balance/Balance_Amulet_Unique_GTFO'),
        ]:
    mod.comment(label)
    bal = Balance.from_data(data, obj_path)
    found_class_parts = False
    for cat in bal.categories:
        if 'Part_Amulet_ClassStat' in cat.partlist[0].part_name:
            found_class_parts = True
            cat.clear()
            for part, att in amulet_part_mapping.items():
                cat.add_part_name(f'/Game/Gear/Amulets/_Shared/_Design/Parts/ClassStat/{part}', BVCF(bva=att))
            break
    if found_class_parts:
        bal.hotfix_full(mod)
    mod.newline()

# Aborted attempt at seeing how we can deal with Enchantments below.  There's various annoyances
# if we want to do this -- many Balances include a hardcoded list of enchantments, and those
# would be easy to edit: just alter the weights.  It'd be annoying 'cause there's so many of
# them, but doable, especially with code.
#
# The wrinkle is that some balances *don't* explicitly specify Enchantments, and they just get
# put on the Balance automatically by the engine.  For instance:
#
#   /Game/Gear/Melee/_Shared/_Design/Balance/Balance_M_Sword_03_Rare
#
# If you dump at runtime, you'll see that its RuntimeGenericPartList is populated, so it's
# getting them from somewhere; I assume probably:
#
#   /Game/Gear/Melee/_Shared/_Design/EndGameParts/Balance/InvGenericPartExpansion_Melee
#
# By the time we hotfix, modifications to that object don't impact anything on the balance.
# For instance, this *works* (the object is updated) but no changes show up on the Balance:
#
#    mod.reg_hotfix(Mod.PATCH, '',
#            '/Game/Gear/Melee/_Shared/_Design/EndGameParts/Balance/InvGenericPartExpansion_Melee',
#            'GenericParts.Parts.Parts[0].Weight.BaseValueScale',
#            200000)
#
# We *can*, at least, hit that value directly on RuntimeGenericPartList.  This works:
#
#    mod.reg_hotfix(Mod.PATCH, '',
#            '/Game/Gear/Melee/_Shared/_Design/Balance/Balance_M_Sword_03_Rare',
#            'RuntimeGenericPartList.PartList.PartList[0].Weight.BaseValueScale',
#            200000)
#
# The annoying thing is that we'd have to figure out every single Balance that can be
# enchanted, check to see if the list is hardcoded -- if so, we know for sure what
# the list is, so we can alter weights.  If not, we need to figure out what object
# provides the balance with enchantments and use that to figure out what indexes we
# need to alter on the Balance.  Alternatively, could pull that info out with the SDK,
# of course.  I'm not going to bother with that for the time being, though.  Class-
# specific Enchantments are rare enough that I don't want to deal with it yet.

mod.close()
