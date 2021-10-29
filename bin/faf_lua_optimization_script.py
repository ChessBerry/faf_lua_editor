from faf_lua_editor import FAFLuaEditor

if __name__ == "__main__":
    # # rootdirs = ["../FAForever_GitHub/units"]
    # # rootdirs = ["../FAForever_GitHub/projectiles"]
    # rootdirs = ["../FAForever_GitHub/units", "../FAForever_GitHub/projectiles"]
    # filepaths = []
    # for rootdir in rootdirs:
    #     for subdir, dirs, files in os.walk(rootdir):
    #         # print(files)
    #         for file in files:
    #             if file.endswith(".lua"):
    #                 file_path = os.path.join(subdir, file)
    #                 filepaths.append(file_path)
    #                 # print(file_path)

    # filepaths = ["../FAForever_GitHub/units/DRA0202/DRA0202_Script.lua"]
    # filepaths = ["../FAForever_GitHub/units/UAB1104/UAB1104_Script.lua"]
    # filepaths = ["../FAForever_GitHub/projectiles\AIFMiasmaShell01\AIFMiasmaShell01_script.lua"]
    filepaths = ["faf_lua_for_testing.lua"]
    # filepaths = ["lua_for_testing.lua"]

    editor = FAFLuaEditor()

    failed_files = []
    for file_path in filepaths:
        try:
            print("\nOpening ", file_path)
            editor.reformat_file(file_path)
            # editor.upvalue_moho_functions_in_file(file_path)
            # print(file_path)
        except:
            failed_files.append(file_path)
            print("FAILED editing/upvaluing ", file_path)

    if failed_files:
        print("\nfailed and hence skipped files:\n", failed_files)
    else:
        print("Editing/Optimizing worked for ALL files!")
    # print("it worked!")

# ---------
# Notes for the moho_sim_reference changes:
# 
# Removed all the User and Core functions as we probably don't want to touch them anyway
# 
# Removed all the "base" functions and all the functions with "_c_" in the name (only "_c_CreateEntity" 
# and "_c_CreateShield") as touching either of them can hard crash the game for some reason
# 