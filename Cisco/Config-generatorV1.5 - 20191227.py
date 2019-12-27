import pandas as pd
import os
import re
import sys

if os.path.exists("output"):
        pass
else:
   os.mkdir("output")

def excel_writer(file, df):
    w = pd.ExcelWriter(file)
    df.to_excel(w, 'Sheet1', index=False, header=False)
    w.save()

def string_duplicate(li):
    new_s = []
    for x in li:
        if x not in new_s:
            new_s.append(x)
    return(new_s)

def template_argus(template_file, output_file):
    if os.path.isfile(data_file):
        print('ERROR! File '+ data_file +' is exist!')
        return
    else:
        pass
    with open(template_file, 'rt') as f:
        template = f.read()
        f.close()

    argus = []

    for line in template.splitlines():
        if re.search(r'\<*\>', line):
            for argu in re.findall('\<(.*?)\>', line):
                argus.append(argu)
    li = string_duplicate(argus)
    li = [li]
    df = pd.DataFrame(li)
    excel_writer(output_file, df)
    print('data file {} is generated!'.format(output_file))

def generateor(template_file, data_file, config_director):
    df = pd.read_excel(data_file)
    with open(template_file, 'rt') as f:
        template = f.read()
        f.close()

    for i in range(df.shape[0]):
        print(0)
        try:
            with open(config_director + str(df.at[i, 'hostname']) + '.txt', 'wt') as f:
                print(config_director + str(df.at[i, 'hostname']))
                print(str(df.at[i, 'hostname']) + ' is generating! \n')
                for line in template.splitlines():
                    if re.search(r'\<*\>', line):
                        for argu in re.findall(r'\<(.*?)\>', line):
                            line = line.replace('<{0}>'.format(argu), str(df.at[i, argu]))
                        f.write(line + '\n')
                    else:
                        f.write(line + '\n')
                f.close()
        except Exception as e:
            print(e)
        print(str(df.at[i, 'hostname']) +'.txt generated! \n')

if __name__ == '__main__':
    while 1:
        try:
            choice = input('''
            press f to input project directory:
            press 0 to input txt template name:
            press 1 to generate arugs excel
            press 2 to generate cofiguratione
            press h to get tips of this scripts
            press e to exit script
            :''')

            if choice is '0':
                template_name = input('Please identify the template name:')
                template_file = os.path.join(template_directory , template_name + '.txt')
                data_file = os.path.join(template_directory, template_name + '.xlsx')
                config_director = os.path.join(template_directory, 'output\\')
                print('config files will be generated in {}'.format(config_director))
            elif choice is 'f':
                template_directory = input('Please input the project directory:')
            elif choice is '1':
                template_argus(template_file, data_file)
            elif choice is '2':
                generateor(template_file, data_file, config_director)
            elif choice is 'h':
                print('''
            ****************************************************************
                txt 文件模板，设备名称尖角号内，必须使用<hostname>
                脚本需要提前安装pandas 和xlrd 两个模块，请百度pip install
                f option 下填写目录是模板所在目录
                f option 下填写目录末尾不需要带\\
            ****************************************************************    
                ''')
            elif choice is 'e':
                break
            else:
                print('Wrong choice, please choose the right one!')
        except Exception as e:
            print(e)
