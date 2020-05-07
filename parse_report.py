# coding=utf-8


import sys
import MySQLdb
import getopt

class ParseReport:

    def __init__(self,path,force = False):
        self.path = path
        self.force = force


    def get_connection(self):
        host = "vnamenode01.edaijia-inc.cn"
        port = 3306
        #host = "172.16.170.151"
        #port = 2002
        #host = "localhost"
        #port = 3306
        #user = "root"
        #passwd = "root"
        user = "data"
        passwd = "sudEio998s8daAD0af!"
        db = "qlikview"
        mysql_conn = MySQLdb.connect(host, user, passwd, db,port, use_unicode=True,charset="utf8")
        return mysql_conn

    def parse(self):
        reports = self.read_file()
        self.save_or_update_reports(reports)



    '''
     根据报表名称判断报表是否存在
    '''
    def check_report_exists(self,connection,report_name):
        sql = "select id,report_name,report_creater,report_principal from report_info where report_name = %s "
        cursor = connection.cursor()
        cursor.execute(sql, (report_name,))
        row = cursor.fetchone()
        cursor.close()
        if row and row[1] is not None:
            return True
        else:
            return False

    '''
     根据邮箱判断用户是否存在
    '''
    def check_report_receiver(self,connection,report_receiver):
        sql = "select id,receiver_email,receiver_name from report_receiver where receiver_email = %s "
        cursor = connection.cursor()
        cursor.execute(sql, (report_receiver,))
        row = cursor.fetchone()
        cursor.close()
        if row and row[1] is not None:
            return True
        else:
            return False

    '''
     根据报表名称获取报表
    '''
    def get_report(self,connection,report_name):
        sql = "select id,report_name,report_creater,report_principal from report_info where report_name = %s "
        cursor = connection.cursor()
        cursor.execute(sql, (report_name,))
        row = cursor.fetchone()
        cursor.close()
        return row

    '''
     根据邮箱获取收件人
    '''
    def get_receiver(self,connection,receiver_email):
        sql = "select id,receiver_email,receiver_name from report_receiver where receiver_email = %s "
        cursor = connection.cursor()
        cursor.execute(sql, (receiver_email,))
        row = cursor.fetchone()
        cursor.close()
        return row

    '''
    保存报表信息
    '''
    def save_report(self,connection,report_name,service_user,data_user):
        sql = "insert into  report_info(report_name,report_principal,report_creater) values(%s,%s,%s)"
        cursor = connection.cursor()
        cursor.execute(sql,(report_name,service_user,data_user,))
        cursor.close()
        connection.commit()

    '''
     删除报表
    '''
    def delete_report(self,connection,report_id):
        sql = "delete from report_info where id = %s"
        cursor = connection.cursor()
        cursor.execute(sql,(report_id,))
        cursor.close()
        connection.commit()

    '''
      删除报表对应收件人信息
    '''
    def delete_report_receiver(self,connection,report_id):
        sql = "delete from report_info_receivers where reportinfo_id = %s"
        cursor = connection.cursor()
        cursor.execute(sql,(report_id,))
        cursor.close()
        connection.commit()

    '''
     删除报表对应抄送信息
    '''
    def delete_report_copy(self,connection,report_id):
        sql = "delete from report_info_copys where reportinfo_id = %s"
        cursor = connection.cursor()
        cursor.execute(sql,(report_id,))
        cursor.close()
        connection.commit()

    '''
    保存收件人信息
    '''
    def save_receiver(self,connection,receiver_email,receiver_name):
        sql = "insert into  report_receiver(receiver_email,receiver_name) values(%s,%s)"
        cursor = connection.cursor()
        cursor.execute(sql,(receiver_email,receiver_name,))
        cursor.close()
        connection.commit()

    '''
    保存报表收件人信息
    '''
    def save_report_receiver(self,connection,report_id,receiver_id):
        sql = "insert into  report_info_receivers(reportinfo_id,reportreceiver_id) values(%s,%s)"
        cursor = connection.cursor()
        cursor.execute(sql,(report_id,receiver_id,))
        cursor.close()
        connection.commit()

    '''
     保存报表抄送信息
    '''
    def save_report_copy(self,connection,report_id,copy_id):
        sql = "insert into  report_info_copys(reportinfo_id,reportcopy_id) values(%s,%s)"
        cursor = connection.cursor()
        cursor.execute(sql,(report_id,copy_id,))
        cursor.close()
        connection.commit()
    '''
     读取要配置的收件人信息列表格式如下:
     报表名称,业务负责人,数据负责人,收件人(多个使用空格分隔),抄送(多个使用空格分隔)
    '''
    def read_file(self):
        reports = {}
        file_handler = open(self.path,'r')
        lines = file_handler.readlines()
        if lines :
            for line in lines:
                if line and len(line) > 0:
                    report_array = line.strip().split(",")
                    if report_array and len(report_array) == 5:
                        report_name = report_array[0].strip()
                        service_user = report_array[1].strip()
                        data_user = report_array[2].strip()
                        report_user = report_array[3].strip()
                        report_copy = report_array[4].strip()

                        report_info = {}
                        report_info["report_name"] = report_name
                        report_info["service_user"] = service_user
                        report_info["data_user"] = data_user

                        report_user_array = report_user.split(" ")
                        if report_user_array is None  or len(report_user_array) == 0:
                            print("报表:" + report_name + " 收件人为空,无法解析")
                            return {}
                        report_info["report_user"] = report_user_array

                        report_copy_array = report_copy.split(" ")
                        if report_copy_array is None or len(report_copy_array) == 0:
                            print("报表:" + report_name + " 抄送人为空,无法解析")
                            return {}
                        report_info["report_copy"] = report_copy_array

                        reports[report_name] = report_info

                    else:
                        print("文件内容:" + line + "不符合格式")
                        print("配置格式为: 报表名称,业务负责人,数据负责人,收件人(多个使用空格分隔),抄送(多个使用空格分隔)")
                        return {}
            return reports
        else:
            print(self.path + " 文件内容为空")
            return reports


    '''
     用来判断报表是否存在
    '''
    def save_or_update_reports(self,reports):
        if reports is None or len(reports) == 0:
            print("读取配置文件信息为空,无法解析")
            sys.exit(1)
        else:
            print("输出文件中配置报表信息")
            connection = self.get_connection()
            exist_reports = set()
            exist_receiver = set()
            for report_name,report_info in reports.items():
                report_name = report_info["report_name"]
                service_user = report_info["service_user"]
                data_user = report_info["data_user"]
                report_user = report_info["report_user"]
                report_copy = report_info["report_copy"]
                print(report_name + "  " + service_user + "  " + data_user + "  " + str(report_user) + "  "
                      + str(report_copy))
                is_report_exists = self.check_report_exists(connection,report_name)
                if is_report_exists:
                    exist_reports.add(report_name)
                for receiver in report_user:
                    is_receiver_exits = self.check_report_receiver(connection,receiver)
                    if not is_receiver_exits:
                        exist_receiver.add(receiver)
                for receiver in report_copy:
                    is_receiver_exits = self.check_report_receiver(connection,receiver)
                    if not is_receiver_exits:
                        exist_receiver.add(receiver)


            if exist_reports is not None and len(exist_reports) > 0:
                report_str = ""
                for report in exist_reports:
                    report_str += report + ","
                print("已经存在的报表数:" + str(len(exist_reports))  + "  " + report_str)

            if exist_receiver is not None and len(exist_receiver) > 0:
                receiver_str = ""
                for receiver in exist_receiver:
                    receiver_str += receiver + ","
                print("需要确定邮箱是否存在:" + str(len(exist_receiver)) + "  " + receiver_str)
		sys.exit(1)

            if self.force:
                print("强制执行操作,对已有的报表执行更新操作,对不存在的收件人执行插入操作,收件人姓名为邮箱,需手动更改姓名")
                for report in exist_reports:
                    print("更新报表:" + report)
                    report_id = self.get_report(connection,report)[0]
                    self.delete_report_receiver(connection,report_id)
                    self.delete_report_copy(connection,report_id)
                    self.delete_report(connection,report_id)
                    service_user = reports[report]["service_user"]
                    data_user = reports[report]["data_user"]
                    self.save_report(connection,report,service_user,data_user)

                for receiver in exist_receiver:
                    print("保存收件人:" + receiver)
                    self.save_receiver(connection,receiver,receiver)

            else:
                if len(exist_reports) > 0:
                    print("配置的报表中有已经存在的报表,无法执行插入操作")
                    sys.exit(1)

                if len(exist_receiver) > 0 :
                    print("需要添加收件人邮箱,无法执行插入操作")
                    sys.exit(1)

            # 保存报表信息
            for report in reports:
                if report not in exist_reports:
                    print("保存报表:" + report)
                    service_user = reports[report]["service_user"]
                    data_user = reports[report]["data_user"]
                    self.save_report(connection,report,service_user,data_user)

            # 保存报表,收件人配置信息
            for report in reports:
                report_id = self.get_report(connection,report)[0]
                receivers = reports[report]["report_user"]
                for receiver in receivers:
                    receiver_id = self.get_receiver(connection,receiver)[0]
                    self.save_report_receiver(connection,report_id,receiver_id)

                copys = reports[report]["report_copy"]
                for copy in copys:
                    copy_id = self.get_receiver(connection,copy)[0]
                    self.save_report_copy(connection,report_id,copy_id)





'''

  参数:
    p:  需要解析的文件路径 配置格式为: 报表名称,业务负责人,数据负责人,收件人(多个使用空格分隔),抄送(多个使用空格分隔)
    f:  是否执行强制更新, (Y|y) 如果要保存的报表已经存在则更新,收件人不存在会直接保存,姓名使用邮箱

  eg:  python parse_report.py -p xxx -f y

'''
if __name__ == '__main__':

    # 设置 字符编码
    reload(sys)
    sys.setdefaultencoding('utf-8')

    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:f:", ["help","path=","force="])
    except getopt.GetoptError:
        print 'args error getopt.GetoptError'
        exit(-1)

    path = None
    arg_force = None
    force = False
    for k, v in opts:
        if k == '-p':
            path = v.strip()
        if k == '-f':
            arg_force = v.strip()

    if arg_force is not None and len(arg_force) > 0:
        if arg_force == 'Y' or arg_force == 'y':
            force = True

    if path is None:
        print("输入的参数错误 path 是 必须参数")
        sys.exit(1)

    parse = ParseReport(path,force)

    parse.parse()

