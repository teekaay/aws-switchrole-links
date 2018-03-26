def parse_arn(arn):
    """
    Parses an ARN (Amazon Resource Identififier).

    :param arn: The arn as a string
    :returns: A dictionary with all as entries
    """
    parts = arn.split(':')
    sections = {
        'owner': parts[1],
        'service': parts[2],
        'region': parts[3],
        'account_id': parts[4],
        'resource': parts[5]
    }
    return sections
