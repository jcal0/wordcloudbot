import json




def compare(auth_lookup,gpt_response,member_dict):

    for key, value in gpt_response.items():
        if value['evaluation']:
            print(f"{value['content']} is good morning, with key {key}")
            # print(f'Key {key} is from {auth_lookup[key]}')
            # print(f'Updating member dict\n')
            try:
                author = auth_lookup[int(key)]
                member_dict[author] = True
            except Exception as e:
                print(e)
    print(json.dumps(member_dict, indent=4))

    return member_dict


# with open("auth_lookup.json") as file:
#     auth_lookup = json.load(file)

# with open("output.json") as file:
#     gpt_response = json.load(file)
        
# with open("mem_list.json") as file:
#     member_dict = json.load(file)

# compare(auth_lookup,gpt_response,member_dict)

