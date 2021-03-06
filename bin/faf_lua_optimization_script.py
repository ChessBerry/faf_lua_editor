from faf_lua_editor import FAFLuaEditor
import os

if __name__ == "__main__":
    # rootdirs = ["../FAForever_GitHub/units"]
    # rootdirs = ["../FAForever_GitHub/projectiles"]
    rootdirs = ["../FAForever_GitHub/units", "../FAForever_GitHub/projectiles"]
    filepaths = []
    for rootdir in rootdirs:
        for subdir, dirs, files in os.walk(rootdir):
            # print(files)
            for file in files:
                if file.endswith(".lua"):
                    file_path = os.path.join(subdir, file)
                    filepaths.append(file_path)
                    # print(file_path)

    # filepaths = ["../FAForever_GitHub/units/DRA0202/DRA0202_Script.lua"]
    # filepaths = ["../FAForever_GitHub/units/UAB1104/UAB1104_Script.lua"]
    # filepaths = ["../FAForever_GitHub/projectiles\AIFMiasmaShell01\AIFMiasmaShell01_script.lua"]
    # filepaths = ["bin/files_for_quick_testing/faf_lua_for_testing.lua"]
    # filepaths = ["bin/files_for_quick_testing/lua_for_testing.lua"]

    # the last stubborn ones
    # filepaths = ['../FAForever_GitHub/projectiles\\SANHeavyCavitationTorpedo01\\SANHeavyCavitationTorpedo01_script.lua', '../FAForever_GitHub/projectiles\\SANHeavyCavitationTorpedo02\\SANHeavyCavitationTorpedo02_script.lua']
    
    editor = FAFLuaEditor()

    # filepaths = filepaths[142:143] # megalith

    # filepaths = filepaths[0:150]
    # filepaths = filepaths[150:225]
    # filepaths = filepaths[225:267]
    # filepaths = filepaths[225:246]
    # filepaths = filepaths[246:255]
    # filepaths = filepaths[246:250]
    # filepaths = filepaths[250:253]
    # filepaths = filepaths[252:253] #  Ohwalli-Strategic Bomb script SBOOhwalliStategicBomb01_script.lua

    # filepaths = filepaths[250:260]
    # filepaths = filepaths[250:255]
    # filepaths = filepaths[255:258]
    # filepaths = filepaths[255:257]
    # filepaths = filepaths[255:256] # Zhanasee Bomb script SBOZhanaseeBomb01_script.lua

    # remove SBOZhanaseeBomb01_script.lua from the filpaths, as I don't understand the tripple colon syntax
    for i in range(len(filepaths)):
        path = filepaths[i]
        if 'SBOZhanaseeBomb01_script.lua' in path: 
            filepaths.pop(i)
            break

    nr_files_to_edit = len(filepaths)
    print(nr_files_to_edit)

    failed_files = []
    for file_path in filepaths:
        try:
            print("\nOpening ", file_path)
            # editor.reformat_file(file_path)
            editor.upvalue_moho_functions_in_file(file_path)
            # print(file_path)
        except:
            failed_files.append(file_path)
            print("FAILED editing/upvaluing ", file_path)

    if failed_files:
        print("\nfailed and hence skipped files:\n", failed_files)
    else:
        print("\nEditing/Optimizing worked for ALL %d files!"%nr_files_to_edit)
    # print("it worked!")

# ---------
# Notes for the moho_sim_reference changes:
# 
# Removed all the User and Core functions as we probably don't want to touch them anyway
# 
# Removed all the "base" functions and all the functions with "_c_" in the name (only "_c_CreateEntity" 
# and "_c_CreateShield") as touching either of them can hard crash the game for some reason
# 