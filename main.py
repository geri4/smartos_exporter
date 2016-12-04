from prometheus_client import start_http_server, Summary, Counter, Gauge
import random
import time
import psutil

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
RAM_TOTAL = Gauge('smartos_memory_total', 'Total memory size')
RAM_AVAIL = Gauge('smartos_memory_available', 'Avaliable memory')
RAM_USED = Gauge('smartos_memory_used', 'Used memory')
RAM_FREE = Gauge('smartos_memory_free', 'Free memory')
SWAP_TOTAL = Gauge('smartos_swap_total', 'Total swap size')
SWAP_USED = Gauge('smartos_swap_used', 'Used swap')
SWAP_FREE = Gauge('smartos_swap_free', 'Free swap')
CPUTIME_USER = Gauge('smartos_cputime_user', 'CPU user time')
CPUTIME_SYSTEM = Gauge('smartos_cputime_system', 'CPU system time')
CPUTIME_IDLE = Gauge('smartos_cputime_idle', 'CPU idle time')
CPUTIME_IOWAIT = Gauge('smartos_cputime_iowait', 'CPU iowait time')
CPU_CTXSW = Gauge('smartos_cpu_ctxsw', 'CPU context switches')
CPU_INTR = Gauge('smartos_cpu_interrupts', 'CPU interrupts')
CPU_SOFT_INTR = Gauge('smartos_cpu_soft_interrupts', 'CPU soft interrupts')
CPU_SYSCALLS = Gauge('smartos_cpu_syscalls', 'CPU system calls')
DISKSIZE_TOTAL = Gauge('smartos_disksize_total', 'Total disk size', ['device', 'mountpoint', 'fstype'])
DISKSIZE_USED = Gauge('smartos_disksize_used', 'Used disk size', ['device', 'mountpoint', 'fstype'])
DISKSIZE_FREE = Gauge('smartos_disksize_free', 'Free disk size', ['device', 'mountpoint', 'fstype'])
DISK_READCOUNT = Gauge('smartos_disk_readcount', 'Disk read count', ['disk'])
DISK_WRITECOUNT = Gauge('smartos_disk_writecount', 'Disk write count', ['disk'])
NET_BYTES_SEND = Gauge('smartos_net_bytes_send', 'Bytes sended', ['nic'])
NET_BYTES_RECV = Gauge('smartos_net_bytes_recv', 'Bytes recieved', ['nic'])
NET_PKT_SEND = Gauge('smartos_net_pkt_send', 'Packets sended', ['nic'])
NET_PKT_RECV = Gauge('smartos_net_pkt_recv', 'Packets recieved', ['nic'])
NET_ERRIN = Gauge('smartos_net_errin', 'Input errors', ['nic'])
NET_ERROUT = Gauge('smartos_net_errout', 'Output errors', ['nic'])
NET_DROPIN = Gauge('smartos_net_dropin', 'Input dropped packets', ['nic'])
NET_DROPOUT = Gauge('smartos_net_dropout', 'Output dropped packets', ['nic'])

# Decorate function with metric.
@REQUEST_TIME.time()
def process_request():
    """A dummy function that takes some time."""

def memory_stat():
    memstat = psutil.virtual_memory()
    RAM_TOTAL.set(memstat.total)
    RAM_AVAIL.set(memstat.available)
    RAM_USED.set(memstat.used)
    RAM_FREE.set(memstat.free)

def swap_stat():
    swapstat = psutil.virtual_memory()
    SWAP_TOTAL.set(swapstat.total)
    SWAP_USED.set(swapstat.used)
    SWAP_FREE.set(swapstat.free)

def cputime_stat():
    cputime = psutil.cpu_times(percpu=False)
    CPUTIME_USER.set(cputime.user)
    CPUTIME_SYSTEM.set(cputime.system)
    CPUTIME_IDLE.set(cputime.idle)
    CPUTIME_IOWAIT.set(cputime.iowait)

def cpu_stat():
    cpustat = psutil.cpu_stats()
    CPU_CTXSW.set(cpustat.ctx_switches)
    CPU_INTR.set(cpustat.interrupts)
    CPU_SOFT_INTR.set(cpustat.soft_interrupts)
    CPU_SYSCALLS.set(cpustat.syscalls)

def disksize_usage():
    for part in psutil.disk_partitions():
        diskstat = psutil.disk_usage(part.mountpoint)
        DISKSIZE_TOTAL.labels(device = part.device, mountpoint = part.mountpoint, fstype = part.fstype).set(diskstat.total)
        DISKSIZE_USED.labels(device = part.device, mountpoint = part.mountpoint, fstype = part.fstype).set(diskstat.used)
        DISKSIZE_FREE.labels(device = part.device, mountpoint = part.mountpoint, fstype = part.fstype).set(diskstat.free)

def disk_stat():
    for disk, diskstat in psutil.disk_io_counters(perdisk=True).iteritems():
        DISK_READCOUNT.labels(disk = disk).set(diskstat.read_count)
        DISK_WRITECOUNT.labels(disk = disk).set(diskstat.write_count)

def net_stat():
    for nic, nicstat in psutil.net_io_counters(pernic=True).iteritems():
        NET_BYTES_SEND.labels(nic = nic).set(nicstat.bytes_sent)
        NET_BYTES_RECV.labels(nic = nic).set(nicstat.bytes_recv)
        NET_PKT_SEND.labels(nic = nic).set(nicstat.packets_sent)
        NET_PKT_RECV.labels(nic = nic).set(nicstat.packets_recv)
        NET_ERRIN.labels(nic = nic).set(nicstat.errin)
        NET_ERROUT.labels(nic = nic).set(nicstat.errout)
        NET_DROPIN.labels(nic = nic).set(nicstat.dropin)
        NET_DROPOUT.labels(nic = nic).set(nicstat.dropout)


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(9100)
    # Generate some requests.
    while True:
        process_request()
        memory_stat()
        swap_stat()
        cputime_stat()
        cpu_stat()
        disksize_usage()
        disk_stat()
        net_stat()
        time.sleep(1)
