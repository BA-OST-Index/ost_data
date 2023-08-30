import json
import os
import logging
import sys
import uuid

filepath = ".."
LOGGER = logging.getLogger()
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
ALL_UUID = []

REPLACE_IF_CONFLICTED = True
DISABLE_WRITING = True


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
                original_content = json.load(file)

            # try to get uuid
            try:
                file_uuid = original_content["uuid"]
            except KeyError:
                # guess this is something special, but whatsoever move on
                LOGGER.warning(f"SKIPPING: {curr_filepath}")
                continue

            # check uuid
            if file_uuid in ALL_UUID:
                LOGGER.warning(f"WARNING:\t\t\t{curr_filepath}\tUUID conflicted!")
                LOGGER.warning(f"\tORIGINAL: {original_content}")

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


traverse_path([filepath])
