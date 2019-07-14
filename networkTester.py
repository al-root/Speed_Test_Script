import speedtest
import socket
import os
import re
import subprocess

def test():
    s = speedtest.Speedtest()
    s.get_servers()
    s.get_best_server()
    s.download()
    s.upload()
    res = s.results.dict()
    return res["download"], res["upload"], res["ping"]


def main():
    # pretty write to txt file
    with open('file.txt', 'w') as f:
        f.write('Your IPv4 Adress is: ')
        # Here we get IPv4
        f.write(str(socket.gethostbyname(socket.gethostname())))
        f.write('\n')
        f.write('Your Default Gateway is: ')
        # Here we get Default gatewat
        f.write(str(socket.gethostbyname(socket.gethostname()))[:-1])
        f.write('\n')
        #Test through speedtest.net 3x
        for i in range(3):
            print('Making test #{}'.format(i+1))
            d, u, p = test()
            f.write('Test #{}\n'.format(i+1))
            f.write('Download: {:.2f} Kb/s\n'.format(d / 1024))
            f.write('Upload: {:.2f} Kb/s\n'.format(u / 1024))
            f.write('Ping: {}\n'.format(p))

        #assign host and display ping stats for IPv4
        host = str(socket.gethostbyname(socket.gethostname()))
        ping = subprocess.Popen(
            ["ping", "-c", "20", host],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )

        out, error = ping.communicate()

        matcher = re.compile("round-trip min/avg/max/stddev = (\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)")
        f.write('IPv4')
        f.write('\n')
        f.write('   min,      avg,      max,      stdDev')
        f.write('\n')
        f.write(str(matcher.search(out).groups()))
        f.write('\n')

        #assign host and display ping stats for Default Gateway
        host = str(socket.gethostbyname(socket.gethostname()))[:-1]
        ping = subprocess.Popen(
            ["ping", "-c", "20", host],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )

        out, error = ping.communicate()

        matcher = re.compile("round-trip min/avg/max/stddev = (\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)")
        f.write('Default Gateway')
        f.write('\n')
        f.write('   min,      avg,      max,      stdDev')
        f.write('\n')
        f.write(str(matcher.search(out).groups()))
        f.write('\n')

        print('Done!')

main()