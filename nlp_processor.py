def check_information(data):

    required = [
        "name",
        "event",
        "date"
    ]

    missing=[]

    for item in required:

        if data[item]=="":
            missing.append(item)


    return missing