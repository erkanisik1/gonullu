#!/usr/bin/env python3
import argparse
import os
import signal
import sys
import traceback

from gonullu import Log, Farm, Volunteer

def parse_arguments():
    parser = argparse.ArgumentParser(description='Gonullu Paket Derleme Sistemi')
    parser.add_argument('-j', '--jobs', type=int, help='Docker içindeki /etc/pisi/pisi.conf içindeki -j parametresi')
    parser.add_argument('--cpu', type=int, default=50, help='Docker için kullanılacak CPU yüzdesi (default: 50)')
    parser.add_argument('--memory', type=int, default=25, help='Docker için kullanılacak hafıza yüzdesi (default: 25)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Detaylı çıktı')
    return parser.parse_args()

def usage():
    print("""
Kullanim - Usage
Asagidaki satir, docker icindeki /etc/pisi/pisi.conf icinde bulunan
-j parametresini verecegimiz rakam ile degistirir.
\tsudo gonullu -j 24
Asagidaki satir, docker icin islemcinin %70'ini, fiziksel hafizanin
%25'ini  ayirir.
\tsudo gonullu --cpu=70 --memory=25
""")
    sys.exit()

def main():
    args = parse_arguments()
    
    log_main = Log()
    farm_main = Farm()
    volunteer_main = Volunteer()

    if args.verbose:
        log_main.set_verbose(True)

    while 1:
        response = farm_main.get_package()
        if (response == -1) or (response ==  -2):
            if response == -1:
                farm_main.wait(message='dir yeni paket bekleniyor.')
        else:
            volunteer_main.get_package_farm(response)
            while 1:
                if volunteer_main.check():
                    # container bulunamadı. İşlem bitti.
                    if farm_main.send_file(response['package'], response['binary_repo_dir']):
                        success = int(open('/tmp/gonullu/%s/%s.bitti' % (response['package'],
                                                                         response['package']), 'r').read())
                        farm_main.get('updaterunning?id=%s&state=%s' % (response['queue_id'], success), json=False)
                        volunteer_main.remove()
                        log_main.success(
                            message='derleme işlemi %s paketi için %s saniyede bitti.' % (response['package'],
                                                                                          farm_main.get_total_time())
                        )
                        log_main.blank_line()
                        farm_main.wait(reset=True)
                    break
                else:
                    # container bulundu. İşlem sürüyor.
                    farm_main.wait(message='den beri derleme işlemi %s paketi için devam ediyor.' % response['package'])

if __name__ == '__main__':
    main()