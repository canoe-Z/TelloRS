"""
把RoLabelImg 生成的xml格式文件转换成coco格式文件
"""

import os
import json
import xml.etree.ElementTree as ET
from BboxToolkit.transforms import obb2hbb

START_BOUNDING_BOX_ID = 1


def get(root, name):
    vars = root.findall(name)
    return vars


def get_and_check(root, name, length):
    vars = root.findall(name)
    if len(vars) == 0:
        return None
        #raise NotImplementedError('Can not find %s in %s.' % (name, root.tag))
    if length > 0 and len(vars) != length:
        raise NotImplementedError(
            'The size of %s is supposed to be %d, but is %d.' % (name, length, len(vars)))
    if length == 1:
        vars = vars[0]
    return vars


def get_filename_as_int(filename):
    try:
        filename = os.path.splitext(filename)[0]
        filename = filename.replace('video_', '')
        filename = filename.replace('-', '')
        return int(filename)
    except:
        raise NotImplementedError(
            'Filename %s is supposed to be an integer.' % (filename))


def convert(xml_list, xml_dir, json_file):
    """

    :param xml_list: 由xml文件名组成的列表['1.xml','2.xml']
    :param xml_dir:  原始存放xml文件夹路径
    :param json_file: 生成json文件的存放路径
    :return:
    """
    json_dict = {"images": [], "type": "instances", "annotations": [],
                 "categories": []}
    #categories = {}
    categories = {'storage-tank': 1, 'mine': 2,
                  'ship': 3, 'field': 4, 'plane': 5}
    bnd_id = START_BOUNDING_BOX_ID
    for line in xml_list:
        line = line.strip()
        print("Processing %s" % (line))
        xml_f = os.path.join(xml_dir, line)
        tree = ET.parse(xml_f)
        root = tree.getroot()
        path = get(root, 'path')
        if len(path) == 1:
            filename = os.path.basename(path[0].text)
        elif len(path) == 0:
            filename = get_and_check(root, 'filename', 1).text
        else:
            raise NotImplementedError(
                '%d paths found in %s' % (len(path), line))
        # The filename must be a number
        image_id = get_filename_as_int(filename)
        size = get_and_check(root, 'size', 1)
        width = int(get_and_check(size, 'width', 1).text)
        height = int(get_and_check(size, 'height', 1).text)
        image = {'file_name': filename, 'height': height, 'width': width,
                 'id': image_id}
        json_dict['images'].append(image)

        for obj in get(root, 'object'):
            category = get_and_check(obj, 'name', 1).text
            if category in ['buliding', 'house', 'building']:
                break
            if category not in categories:
                assert(1 == 2)
                # new_id = len(categories) + 1
                # categories[category] = new_id
            category_id = categories[category]
            robndbox = get_and_check(obj, 'robndbox', 1)
            bndbox = get_and_check(obj, 'bndbox', 1)
            if bndbox:
                xmin = int(float(get_and_check(bndbox, 'xmin', 1).text)) - 1
                ymin = int(float(get_and_check(bndbox, 'ymin', 1).text)) - 1
                xmax = int(float(get_and_check(bndbox, 'xmax', 1).text))
                ymax = int(float(get_and_check(bndbox, 'ymax', 1).text))
                w = xmax-xmin
                h = ymax-ymin
                bbox = [xmin, ymin, w, h]
                ann = {'area': w*h, 'iscrowd': 0, 'image_id':
                       image_id, 'bbox': bbox,
                       'category_id': category_id, 'id': bnd_id, 'ignore': 0,
                       'segmentation': []}
                json_dict['annotations'].append(ann)
                bnd_id = bnd_id + 1
            if robndbox:
                cx = int(float(get_and_check(robndbox, 'cx', 1).text)) - 1
                cy = int(float(get_and_check(robndbox, 'cy', 1).text)) - 1
                w = int(float(get_and_check(robndbox, 'w', 1).text))
                h = int(float(get_and_check(robndbox, 'h', 1).text))
                angle = float(get_and_check(robndbox, 'angle', 1).text)
                hbb = obb2hbb([cx, cy, w, h, angle])
                w_hbb = hbb[2]-hbb[0]
                h_hbb = hbb[3]-hbb[1]
                bbox = [hbb[0], hbb[1], w_hbb, h_hbb]
                ann = {'area': w*h, 'iscrowd': 0, 'image_id':
                       image_id, 'bbox': bbox,
                       'category_id': category_id, 'id': bnd_id, 'ignore': 0,
                       'segmentation': []}
                json_dict['annotations'].append(ann)
                bnd_id = bnd_id + 1

    for cate, cid in categories.items():
        cat = {'supercategory': 'none', 'id': cid, 'name': cate}
        json_dict['categories'].append(cat)
    json_fp = open(json_file, 'w')
    json_str = json.dumps(json_dict, ensure_ascii=False, indent=4)
    json_fp.write(json_str)
    json_fp.close()


if __name__ == '__main__':
    xml_dir = './data/uav/train/xml'
    xml_list = [x for x in os.listdir(xml_dir) if '.xml' in x]
    dist_dir = './data/uav_COCO/annotations'
    json_file = os.path.join(dist_dir, 'train.json')
    convert(xml_list, xml_dir, json_file)
