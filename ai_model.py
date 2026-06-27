def generate_certificate(
    name,
    event,
    extra_message,
    date,
    certificate_type,
    organization
):


    message=f"""

{certificate_type}


This certificate is proudly presented to


{name}


for successfully completing


{event}


Organized by:

{organization}


Date:

{date}


{extra_message}


"""


    return message