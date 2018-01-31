#!/usr/bin/env python
""" msend.py
    
    A simple multicast chat program.
    This is a simple implementation that only send or listens.
    To use, open two console windows - one for transmit and one
    for listening.
    
    Multicast socket usage inspired by:
     https://pymotw.com/3/socket/multicast.html
    
    Paul A. Lambert  January 31, 2018
"""
import socket
import struct
import sys
import click
import time

def multicastSocket():
    """ Setup a UDP multicast socket """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(30) # timeout to not block on recieve
    ttl = struct.pack('b', 1)  # time-to-live of 1 hop to stay on local net
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    return sock

def send(sock, message, mcast_address, port):
    """ Send message to multicast socket """
    multicast_group = (mcast_address, port)
    try:
        sent = sock.sendto(message, multicast_group)
    except:
        click.echo("Send Error")

def recieve(sock):
    """ Recieve message from multicast socket and echo
    """
    try:
        data, server = sock.recvfrom(16)
    except socket.timeout:
        return None
    else:
        return (server, data)




# -- Command line code, executed when file is run as 'main'
@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--port', '-p', 'port', default=10000,
              help="Specify UDP port (default=10000)")
@click.option('--mcast', '-m', 'mcast_address', default='224.3.29.71',
              help="Specify multicast address (default='224.3.29.71')")
@click.option('--send', '-s', 's_or_l', flag_value='send',
              default=True, help="Send messages")
@click.option('--listen', '-l','s_or_l', flag_value='listen',
              help="Listen for messages")
def cli(port, mcast_address, s_or_l):
    """ Multicast UDP Chat
    """
    # setup a socket for multicast using the provided address and port
    sock = multicastSocket()
    
    if s_or_l == 'send':
        while True:
            #message = click.prompt('> ')
            message = "THIS IS A TEST"
            send(sock, message, mcast_address, port)
            time.sleep(1)
            click.echo(message)
    elif s_or_l == 'listen':
        send(sock, ' ', mcast_address, port)
        while True:
            response = recieve(sock)
            if response:
                server, data = response
                click.echo('{} -> {!r}'.format(server, data))
    else:
        click.echo('Error - bad option')

if __name__ == '__main__':
    cli()
