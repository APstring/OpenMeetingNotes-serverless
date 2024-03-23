import os
from typing import Dict, Optional
import boto3
import traceback

class ConfigException(Exception):
    pass


def get_aws_params():
    # params = {}
    # ssm_verify = True

    client = boto3.client("ssm", region_name="us-east-1")

    try:
        response = client.get_parameter(
            Name='/openmeeting/secret_key',
            WithDecryption=True
        )
        
        return response['Parameter']['Value']
    except Exception as e:
        traceback.print_exc()
        return e

    # next_token: Optional[str] = " "
    # while next_token is not None:
    #     result = client.get_parameters_by_path(Path=prefix,
    #                                            Recursive=True,
    #                                            WithDecryption=True,
    #                                            MaxResults=1,
    #                                            NextToken=next_token)
        
    #     for param in result["Parameters"]:
    #         params[param["Name"]] = param["Value"]
    #     next_token = result.get("NextToken", None)

    # return {k.split("/")[-1]: params[k] for }


# def get_config() -> Dict[str, str]:
#     config = {}
#     secret_name = "openmeeting"
#     verify_bln = True



class Config:
    def __init__(self):
        self.secret = get_aws_params()
