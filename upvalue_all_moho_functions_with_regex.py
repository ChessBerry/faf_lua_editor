
# Iterate over files with regex searches to remove colon functions
# Actually, why not do that in here too? Then it's all in one place, much better documented an reproducible

files_to_upvalue = os.smth
all_moho_files = os.smth

moho_fct_dict = {}
for file in all_moho_files:
    moho_global_names_found = []
    for moho_global_name in find_global_name_regex: # this shouldn't be a for loop, it can only find one..
        moho_global_names_found.append(moho_global_name)
    
    if len(moho_global_names_found) > 1:
        raise Exception("More than one global moho name was found for the file " + os.getname(file))
    
    moho_global_table_name = "_G." + moho_global_names_found[0]
    moho_fct_dict[moho_global_table_name] = []
        
    for moho_fct in find_moho_fct_regex:
        moho_fct_dict[moho_global_table_name].append(moho_fct)


for file in files_to_upvalue:
    found_moho_fct_dict = {}
    for fct_name in find_fct_name_regex:
        for moho_global_table_name, moho_fcts in moho_fct_dict.items():
            if fct_name in moho_fcts:
                if moho_global_table_name not in found_moho_fct_dict:
                    found_moho_fct_dict[moho_global_table_name] = set()
                found_moho_fct_dict[moho_global_table_name].add(fct_name)
                # replace the fct with the direct call to the moho fct in file, care about fct arguments thoug

    # go back to beginning of file here
    for moho_global_table_name, moho_fcts in found_moho_fct_dict.items():
        # just before the first nonempty, noncomment, nonlocal import line add the following
        # empty line
        # comment about automatically upvaluing functions
        # local MohoFileMethods = moho_global_table_name  (create mohofilename programmatically from the table name)
        for moho_fct in moho_fcts:
            # local MohoFct = MohoFileMethods.moho_fct
            # empty line
            pass
