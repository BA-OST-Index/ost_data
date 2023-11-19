import json
import os
import logging
import sys
import uuid
import pprint

LOGGER = logging.getLogger()
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
ALL_UUID = []

REPLACE_IF_CONFLICTED = True
DISABLE_WRITING = True

ERROR_JSON = []
CONFLICTED_JSON = []


def traverse_path(namespace: list):
    global ALL_UUID, LOGGER, REPLACE_IF_CONFLICTED
    current_path = "/".join(namespace)

    all_path = list(os.listdir(current_path))
    all_file = list(filter(lambda i: os.path.isfile(os.path.join(*namespace, i)) and not i.startswith("."), all_path))
    all_folder = list(filter(lambda i: os.path.isdir(os.path.join(*namespace, i))
                                       and not i.startswith(".") and not i.startswith("_"),
                             all_path))

    for i in all_file:
        if i.endswith(".json"):
            curr_filepath = os.path.join(current_path, i)
            LOGGER.debug(f"CHECKING: {curr_filepath}")

            with open(curr_filepath, mode="r", encoding="UTF-8") as file:
                try:
                    original_content = json.load(file)
                except json.JSONDecodeError:
                    LOGGER.error(f"JSON ERROR: {curr_filepath}")
                    ERROR_JSON.append(curr_filepath)

            # try to get uuid
            try:
                file_uuid = original_content["uuid"]
            except KeyError:
                # guess this is something special, but whatsoever move on
                LOGGER.info(f"SKIPPING: {curr_filepath}")
                continue

            # check uuid
            if file_uuid in ALL_UUID:
                LOGGER.warning(f"WARNING:\t\t\t{curr_filepath}\tUUID conflicted!")
                LOGGER.warning(f"\tORIGINAL: {original_content}")

                CONFLICTED_JSON.append(curr_filepath)

                # replace uuid
                if REPLACE_IF_CONFLICTED:
                    while True:
                        replace_uuid = str(uuid.uuid4())
                        if replace_uuid not in ALL_UUID:
                            break

                    original_content["uuid"] = replace_uuid
                    LOGGER.warning(f"\tNEW UUID: {replace_uuid}")

            if not DISABLE_WRITING:
                with open(curr_filepath, mode="w", encoding="UTF-8") as file:
                    json.dump(original_content, file)

    for folder in all_folder:
        traverse_path(namespace + [folder])


def run(filepath):
    traverse_path([filepath])

    if len(ERROR_JSON) != 0:
        print("ERROR JSON:")
        pprint.pprint(ERROR_JSON)
    if len(CONFLICTED_JSON) != 0:
        print("CONFLICTED JSON:")
        pprint.pprint(CONFLICTED_JSON)
    if len(ERROR_JSON) != 0 or len(CONFLICTED_JSON) != 0:
        raise AssertionError


if __name__ == "__main__":
    run("..")
