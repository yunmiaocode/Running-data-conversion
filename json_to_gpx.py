# 导入python标准库，模块及类
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import json
import time
from datetime import datetime
import pytz
import os

import gpxpy.gpx
import xml.etree.ElementTree as ET

# 编写数据清理，文件操作函数实现特定的功能
# 文本转换为列表函数
def text_to_list(text_str):
    run_data_list = []
    text_str_clear = text_str[22:]
    lines = text_str_clear.split('\n')
    del lines[-1]
    for line in lines:
        parts = line.split(';')
        item = {}
        for part in parts:
            try:
                key, value = part.split('=')
                item[key] = value
            except:
                pass
        run_data_list.append(item)
    return run_data_list
# 读取路径内容并转换为python对像


def path_to_pyobj(file_path):
    """将指定路径的文件里的内容读取为python对像,并返回python对像

    Args:
        file_path (str): 要读取文件的路径

    Returns:
        py_obj(python_obj): 要返回的python对像
    """
    path = Path(file_path)          # 使用Path类将指定路径创建为path实体
    contents = path.read_text()     # 使用Path类read_text()方法将文件内读取容为'str'
    # 使用json模块中loads()函数将格式为'str'的文件内容转换为文件形式上的python对像（列表/字典等）
    py_obj = json.loads(contents)
    return py_obj
# 根据路径将python对象写入文件


def creat_new_readable_file(new_file_path, py_obj):
    """将已有的python对像转换为字符串写入新文件

    Args:
        new_file_path (str): 新文件的路径
        py_obj (python对像列表/字典等): 需要写入文件的python对像
    """
    path = Path(new_file_path)      # 使用Path类将指定路径创建为path实体
    # 使用json模块中dumps()函数将python对像转换为格式为'str'的可读内容
    readable_data = json.dumps(py_obj, indent=4)
    path.write_text(readable_data)   # 使用Path类write_text()方法将文件写入路径所指文件

# 提取列表内相同键的值组成新列表，并返回列表
def dirclist_extract_lists(dirclist, data_type, data_value, data_time):
    """提取一个元素为字典的列表中字典某三项键的值存入三个列表，返回三个列表的函数

    Args:
        dirclist (list): 要提取对应字典键的值的列表
        data_type (str): 字典键的名称（一般为该字典存储实际数据的类型）
        data_value (str): 字典键的名称（一般为该字典存储实际数据的值）
        data_time (_type_):字典键的名称（一般为该字典存储实际数据的时间）

    Returns:
        ls_1(list): 对应字典键的值的集合列表,一般为实际中的数据类型
        ls_2(list): 对应字典键的值的集合列表,一般为实际中数据的值
        ls_3(list): 对应字典键的值的集合列表,一般为实际中数据值记录的时间
    """
    ls_1, ls_2, ls_3 = [], [], []
    for dirc in dirclist:
        ls1 = dirc[data_type]
        ls2 = int(float(dirc[data_value]))
        ls3 = datetime.fromtimestamp(int(dirc[data_time])/1000)

        ls_1.append(ls1)
        ls_2.append(ls2)
        ls_3.append(ls3)

    return ls_1, ls_2, ls_3

# 专用与提取坐标点字典列表的函数
def dirclist_extract_location(dirclist, lon, lat, data_time):
    """提取一个元素为字典的列表中字典某三项键的值存入三个列表，返回三个列表的函数

    Args:
        dirclist (list): 要提取对应字典键的值的列表
        data_type (str): 字典键的名称（一般为该字典存储实际数据的类型）
        data_value (str): 字典键的名称（一般为该字典存储实际数据的值）
        data_time (_type_):字典键的名称（一般为该字典存储实际数据的时间）

    Returns:
        ls_1(list): 对应字典键的值的集合列表,一般为实际中的数据类型
        ls_2(list): 对应字典键的值的集合列表,一般为实际中数据的值
        ls_3(list): 对应字典键的值的集合列表,一般为实际中数据值记录的时间
    """
    ls_1, ls_2, ls_3 = [], [], []
    for dirc in dirclist:
        ls1 = float(dirc[lon])
        ls2 = float(dirc[lat])
        ls3 = datetime.fromtimestamp(float(dirc[data_time][:-2])*1000000000)

        ls_1.append(ls1)
        ls_2.append(ls2)
        ls_3.append(ls3)

    return ls_1, ls_2, ls_3

# 提取跑步python对象有用信息
def extract_simp_data(pyobj_data):
    """提取pyobj_data有用的跑步数据

    Args:
        pyobj_data (list): 一个包含每次运动数据字典的列表，通过读取原始json文件获得

    Returns:
        simp_list(list): 返回简化后的字典列表

    Dictionary key name meaning:
        "totalSteps": 总步数
        "startTime": 开始时间
        "attribute" : 详细属性
        "totalDistance" : 总距离
        "endTime": 结束时间
        "totalTime": 总用时
        "timeZone": 时区
        "totalCalories": 总卡路里
        "partTimeMap": 分段用时
        "paceMap": 分段平均配速
    """
    simp_list = []
    for run_data in pyobj_data:
        if run_data["sportType"] == 4:
            simp_run_dict = {}
            simp_run_dict["totalSteps"] = run_data["totalSteps"]
            simp_run_dict["startTime"] = run_data["startTime"]
            simp_run_dict["attribute"] = text_to_list(run_data["attribute"])
            simp_run_dict["totalDistance"] = run_data["totalDistance"]
            simp_run_dict["endTime"] = run_data["endTime"]
            simp_run_dict["totalTime"] = run_data["totalTime"]
            simp_run_dict["timeZone"] = run_data["timeZone"]
            simp_run_dict["totalCalories"] = run_data["totalCalories"]
            simp_run_dict["partTimeMap"] = run_data["partTimeMap"]
            simp_run_dict["paceMap"] = run_data["paceMap"]

            simp_list.append(simp_run_dict)

    return simp_list
# 归类列表元素创建多个列表


def create_lists(simp_datas):
    """根据列表元素内容创建多个列表，将跑步数据归类

    Args:
        simp_datas (list): 简化后的跑步数据集合

    Returns:
        _list_: 将simp_datas列表归类存放在多个列表
    """
    lbs_data,  hr_data, sr_data, alti_data, rs_data, rp_data = [], [], [], [], [], []

    for r_data in simp_datas["attribute"]:
        try:
            if r_data['tp'] == 'lbs':
                lbs_data.append(r_data)
        except:
            pass
        try:
            if r_data['tp'] == 'h-r':
                hr_data.append(r_data)
        except:
            pass
        try:
            if r_data['tp'] == 's-r':
                sr_data.append(r_data)
        except:
            pass
        try:
            if r_data['tp'] == 'alti':
                alti_data.append(r_data)
        except:
            pass
        try:
            if r_data['tp'] == 'rs':
                rs_data.append(r_data)
        except:
            pass
        try:
            if r_data['tp'] == 'rp':
                rp_data.append(r_data)
        except:
            pass

    return lbs_data,  hr_data, sr_data, alti_data, rs_data, rp_data
# 将整理好的列表转换为gpx_xml格式


def list_to_gpx(run_fit_list):
    gpx = gpxpy.gpx.GPX()

    track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(track)

    segment = gpxpy.gpx.GPXTrackSegment()
    track.segments.append(segment)

    ns3 = "ns3"

    # 遍历跑步数据，将每个点添加到轨迹段
    for data in run_fit_list:
        # 将字符串时间转换为 datetime 对象
        list_time = data['timestamp']

        # 创建一个轨迹点
        point = gpxpy.gpx.GPXTrackPoint(
            data['latitude'], data['longitude'], elevation=data['elevation'], time=list_time)

        # 创建心率和踏频扩展字段
        track_point_extension = ET.Element("{%s}TrackPointExtension" % ns3)

        hr_element = ET.SubElement(track_point_extension, "{%s}hr" % ns3)
        hr_element.text = str(data['heart_rate'])

        cad_element = ET.SubElement(track_point_extension, "{%s}cad" % ns3)
        cad_element.text = str(data['cadence'])

        # 直接将扩展内容添加到轨迹点的 extensions 中
        point.extensions.append(track_point_extension)

        # 添加轨迹点到轨迹段
        segment.points.append(point)

    # 手动添加命名空间，修改输出为带有命名空间的 XML 格式
    gpx_xml = gpx.to_xml()

    # 添加命名空间
    gpx_xml = gpx_xml.replace('<gpx ', '<gpx xmlns:' + ns3 +
                              '="http://www.garmin.com/xmlschemas/TrackPointExtension/v1" ')

    return gpx_xml


def jsonfile_to_gpxfile(jsonfile_path):
    # 使用文件操作模块里path_to_pyobj()函数将指定路径文件里的内容读取转换为python对像
    all_run_data = path_to_pyobj(jsonfile_path)
    # 筛选有用的跑步数据
    simp_run_list = extract_simp_data(all_run_data)

    gpx_files, run_times = [], []

    for single_run_data in simp_run_list:
        # 提取筛选后跑步数据中"attribute"，并分类创建多个新列表
        lbs, h_r, s_r, alti, rs, rp = create_lists(single_run_data)

        # 提取lbs字典列表，经纬度/采样时间信息
        lons, lats, l_times = dirclist_extract_location(lbs, 'lon', 'lat', 't')
        # 提取s_r字典列表，类型/步频/采样时间信息
        s_colors, steps, s_times = dirclist_extract_lists(s_r, 'tp', 'v', 'k')
        # 提取h_r字典列表，类型/心率/采样时间信息
        h_colors, hearts, h_times,  = dirclist_extract_lists(
            h_r, 'tp', 'v', 'k')
        # 提取alti字典列表，类型/海拔/采样时间信息
        a_colors, altis, a_times,  = dirclist_extract_lists(
            alti, 'tp', 'v', 'k')
        # 提取rs字典列表，类型/海拔/采样时间信息
        r_colors, rss, r_times,  = dirclist_extract_lists(rs, 'tp', 'v', 'k')

        del l_times[-3:], lons[-3:], lats[-3:]
        del l_times[:4], lons[:4], lats[:4]

        single_run_list = []
        for i in range(len(lats)):
            hearts_index = i // 5
            if hearts_index < len(hearts):
                heart_data = hearts[hearts_index]
                try:
                    step_data = steps[hearts_index]
                    alti_data = altis[hearts_index]
                except:
                    pass
            run_fit_dric = {
                "timestamp": l_times[i].astimezone(pytz.utc),
                "latitude": lats[i],
                "longitude": lons[i],
                "elevation": alti_data,
                "heart_rate": heart_data,
                "cadence": step_data
            }

            single_run_list.append(run_fit_dric)

        gpx_file = list_to_gpx(single_run_list)
        gpx_files.append(gpx_file)
        gpx_file_path = time.strftime(
            "%Y-%m-%d", time.localtime(int(int(single_run_data["startTime"])/1000)))
        run_times.append(gpx_file_path)
    return gpx_files, run_times
    # with open(f'gpx_file/{gpx_file_path}-run-data.gpx', 'w', encoding='utf-8') as f:
    #     f.write(gpx_file)

# 用于保存 GPX 文件到指定目录，确保文件名唯一


def save_gpx_files(gpx_files, run_times, output_dir):
    for i, gpx_file in enumerate(gpx_files):
        # 为每个文件生成唯一的文件名
        gpx_file_path = os.path.join(
            output_dir, f"{run_times[i]}-run-data-{i+1}.gpx")

        # 确保文件名唯一
        counter = 1
        while os.path.exists(gpx_file_path):
            gpx_file_path = os.path.join(
                output_dir, f"{run_times[i]}-run-data-{i+1}-{counter}.gpx")
            counter += 1

        # 保存文件
        with open(gpx_file_path, 'w', encoding='utf-8') as f:
            f.write(gpx_file)

# 处理上传 JSON 文件和选择输出目录的函数


def upload_json():
    # 打开文件选择对话框，允许用户选择 JSON 文件
    file_path = filedialog.askopenfilename(
        filetypes=[("JSON Files", "*.json")])

    if file_path:
        try:
            # 调用转换函数，将 JSON 文件转换为 GPX 文件
            gpx_files, run_times = jsonfile_to_gpxfile(file_path)

            # 打开目录选择对话框，允许用户选择输出目录
            output_dir = filedialog.askdirectory(
                title="Select Output Directory")

            if output_dir:
                # 保存 GPX 文件到用户选择的目录
                save_gpx_files(gpx_files, run_times, output_dir)

                # 提示用户转换成功
                messagebox.showinfo(
                    "success", "GPX file generated successfully!")
            else:
                messagebox.showwarning("warn", "No output directory selected")

        except Exception as e:
            messagebox.showerror("warn", f"Parsing failed: {str(e)}")


# 设置 Tkinter 窗口
root = tk.Tk()
root.title("Convert json file to gpx file")
root.geometry("400x200")  # 设置窗口大小

# 创建上传按钮
upload_button = tk.Button(root, text="Upload json file", command=upload_json)
upload_button.pack(pady=50)

# 运行应用
root.mainloop()
