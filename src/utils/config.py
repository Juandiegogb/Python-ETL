import os
from dotenv import load_dotenv
import json
from typing import Any, Dict
from utils.entities import DBConfig

load_dotenv()


def getDBInfo(variableName: str) -> DBConfig:
    jsonString = os.getenv(variableName)
    if jsonString:
        try:
            parsedDict: DBConfig = json.loads(jsonString)
            return parsedDict
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON format in environment variable {variableName}: {e}"
            )
    else:
        raise ValueError(f"The variable {variableName} is not defined")
