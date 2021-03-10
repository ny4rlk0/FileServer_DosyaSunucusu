#5.3.2021 tarihinde yazılmıştır.;
#Erişimi  olan herkes modifiye edebilir ve dağıtabilir.
#Kötü amaçla kullanımından hiçbir şekilde sorumlu değilim.
from flask import Flask,render_template_string, request,send_from_directory
from werkzeug.utils import secure_filename
import socket,os,sys,ctypes,subprocess
from gevent.pywsgi import WSGIServer
from threading import Thread as core
from subprocess import Popen, DEVNULL
import tkinter as ui
from tkinter import messagebox as mb
import subprocess as sp
import socketserver,http.server
nya=0
rlko=0
PAYLASIMLAR_DIR = os.path.join(os.path.dirname(__file__), 'PAYLASIMLAR')
handler = http.server.SimpleHTTPRequestHandler
hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)
CREATE_NO_WINDOW = 0x08000000
fw_in_add=f"""netsh advfirewall firewall add rule name="SS_TCP_80_IN" dir=in action=allow protocol=TCP localport=80"""#olup olmadıgını kontrol et açmadan önce
fw_in_add81=f"""netsh advfirewall firewall add rule name="SS_TCP_81_IN" dir=in action=allow protocol=TCP localport=81"""
fw_out_add81=f"""netsh advfirewall firewall add rule name="SS_TCP_81_OUT" dir=out action=allow protocol=TCP localport=81"""
fw_in_delete81=f"""netsh advfirewall firewall delete rule name="SS_TCP_81_IN" dir=in protocol=TCP localport=81"""
fw_out_delete81=f"""netsh advfirewall firewall delete rule name="SS_TCP_81_OUT" dir=out protocol=TCP localport=81"""
fw_in_delete=f"""netsh advfirewall firewall delete rule name="SS_TCP_80_IN" dir=in protocol=TCP localport=80"""
html_nya='''<!doctype html>
<html>
   <body bgcolor="black" style="color:white">
   <meta charset="UTF-8">
   <title>DOSYA YÜKLE</title>
   <center><h1 style="font-size: 60px;color : gray">Yerel Ağ Dosya Paylaşımı</h1></center>
   <center><h1 style="font-size: 45px;color : blue">Dosya Yükle</h1></center>
   <center>
    </br>
    </br>
    </br>
    </br>
    </br>
      <form action = "http://'''+IP+'''/yuklendi" method = "POST" 
         enctype = "multipart/form-data">
         <input type = "file" name = "file" />
         <input type = "submit"/>
      </form>
    </br>
    </br>
    </br>
    </br>
    </br>
    <a href="http://'''+IP+''':81/"style="font-size: 40px;color : red">Dosya İndir</a>
    </br>
    <center><h6>Software Solutions 2021</h6></center>
    </center>
   </body>
</html>
'''
html_upload='''<!doctype html>
<html>
   <body bgcolor="black" style="color:white">
   <meta charset="UTF-8">
   <title>DOSYA YÜKLENDİ</title>
    <center>
        <h4 style="font-size: 30px;color : white">Dosya başarıyla yüklendi.</h4>
    <a href="http://'''+IP+'''/" style="font-size: 40px;color : red">Geri Dön</a>
    </center>
   </body>
</html>
'''
def chkAdmin():
    try:
        isAdmin = ctypes.windll.shell32.IsUserAnAdmin()
    except AttributeError:
        isAdmin = False
    if not isAdmin:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit(0)
username=os.getlogin()
anlik_directory=os.getcwd()
p='''\PAYLASIMLAR\ '''
p=p.strip()
up_dir=anlik_directory+p
def check_directory_ex():
    PAYLASIMLAR_VARMI=os.path.isdir(up_dir)
    if not PAYLASIMLAR_VARMI:
        os.mkdir(up_dir)
def fw_remove():
    try:
        os.system(fw_in_delete)
    except:
        pass
    try:
        os.system(fw_in_delete81)
    except:
        pass
    try:
        os.system(fw_out_delete81)
    except:
        pass
def fw_add():
    try:
        os.system(fw_in_add)
    except:
        pass
    try:
        os.system(fw_in_add81)
    except:
        pass
    try:
        os.system(fw_out_add81)
    except:
        pass
nya=Flask(__name__)
nya.secret_key = "STEPHANIE_1_2_8_L0RD0FTH3R1NGS"
check_directory_ex()
nya.config['UPLOAD_FOLDER'] = up_dir
nya.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024 #Upload boyut 1 GB ile sınırla.
@nya.route('/')
def main_page():
    return render_template_string(html_nya)
@nya.route('/yuklendi',methods=['GET','POST'])
def upload_file():
    if request.method=='POST':
        check_directory_ex()#check directory exist or not if it wont exist create
        nya=request.files['file']
        nya.save(os.path.join(up_dir, secure_filename(nya.filename)))
        return render_template_string(html_upload)
def flask_server():#Upload Server
    nya_server = WSGIServer((IP, 80), nya)
    nya_server.serve_forever()
def http_server():#Download Server
    check_directory_ex()#check directory exist or not if it wont exist create
    os.chdir(PAYLASIMLAR_DIR)
    socketserver.TCPServer((IP, 81), handler).serve_forever()
if __name__=='__main__':
    chkAdmin() #Admin olarak çalışıp çalışmadığını kontrol et!
    fw_remove()#Güvenlik duvarına ayrıcalık kaldır.
    fw_add() #Güvenlik duvarına ayrıcalık ekle.
    server1 = core(target=flask_server)#, args=(1,)) Flask Server.
    server1.daemon=True #To kill when its needed neccesary
    server1.start() #Flask sunucusunu ayrı bir çekirdekte çalıştır.
    server2 = core(target=http_server)#, args=(1,)) HTTP Server.
    server2.daemon=True #To kill when its needed neccesary
    server2.start() #HTTP sunucusunu ayrı bir çekirdekte çalıştır.
    window=ui.Tk()
    window.title("Dosya Sunucusu")
    window.geometry("465x225")
    window.resizable(0,0)
    window.configure(bg="black")
    #ui.Label(window,text="Dosya Sunucusu",bg="black",fg="white").grid(row=0,column=0)
    ui.Label(window,text="Giriş adresi : "+IP,bg="black",fg="white").grid(row=0,column=0)
    ui.Label(window,text="Dosya yüklemek için adresi tarayıcınıza yazın.",bg="black",fg="gray").grid(row=1,column=0)
    ui.Label(window,text="Bu program açık olduğu sürece PAYLASIMLAR ",bg="black",fg="gray").grid(row=2,column=0)
    ui.Label(window,text="klasöründeki dosyalarınıza erişebilirsiniz.",bg="black",fg="gray").grid(row=3,column=0)
    ui.Label(window,text="Erişimi kesmek için programı kapatmanız yeterlidir.",bg="black",fg="gray").grid(row=4,column=0)
    ui.Label(window,text="İstemci izolasyonu olan ağlarda kullanamazsınız.",bg="black",fg="red").grid(row=5,column=0)
    window.mainloop()
    fw_remove() #Güvenlik için program kapalıyken portlarda kapalı kalsın.
    sys.exit()
