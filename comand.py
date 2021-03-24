import xmltodict
import argparse
import json
import sys
from xml.etree import ElementTree


description = (
    "This command convert from json data type to xml and vice versa. path_to_data is"
    " required argument it indicate path of file that should be converted.path_to_convert "
    "indicates path of file where should be saved converted data if mode is path"
)

mode = (
    "if mode is path then path_to_convert is required,"
    " converted data should be saved in path_to_convert file,"
    "if mode is print converted data should be printed in console."
)

parser = argparse.ArgumentParser(
    prog="xml-json-converter",
    description=description,
    usage="%(prog)s [-h] [-m {output,path}]" " \n\t\t\tpath_to-data [path_to_convert]",
)
parser.add_argument("path_to_data", type=str, help="path to file to be converted")
parser.add_argument(
    "path_to_convert", type=str, help="path to file to be saved converted data"
)

parser.add_argument("-m", "--mode", help=mode, dest="{output, path}")

args = parser.parse_args()


def create_xml_tree(root, data: dict):
    for k, v in data.items():
        if not isinstance(v, dict):
            ElementTree.SubElement(root, k).text = str(v)
        else:
            create_xml_tree(ElementTree.SubElement(root, k), v)
    return root


file_type = args.path_to_data.split(".")[-1]

if file_type == "json":
    with open(args.path_to_data, "r") as jf:
        data = json.loads(jf.read())
        root = ElementTree.Element("data")
        create_xml_tree(root, data)
        tree = ElementTree.ElementTree(root)
        if (
            args.__dict__["{output, path}"] == "path"
            or args.__dict__["{output, path}"] is None
        ):
            tree.write(args.path_to_convert)
        elif args.__dict__["{output, path}"] == "output":
            sys.stdout.write(ElementTree.tostring(root).decode("utf-8"))
        else:
            raise Exception("invalid command for -m/--mode")


elif file_type == "xml":
    with open(args.path_to_data, "r") as xml_f:
        o = xmltodict.parse(xml_f.read())
    if (
        args.__dict__["{output, path}"] == "path"
        or args.__dict__["{output, path}"] is None
    ):
        with open(args.path_to_convert, "w") as jf:
            jf.write(json.dumps(o["data"]))
    elif args.__dict__["{output, path}"] == "output":
        sys.stdout.write(json.dumps(o["data"]))
    else:
        raise Exception("invalid command for -m/--mode")
