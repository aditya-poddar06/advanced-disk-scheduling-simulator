"""Disk scheduling algorithms package."""
from algorithms.fcfs import fcfs
from algorithms.sstf import sstf
from algorithms.scan import scan
from algorithms.cscan import cscan

__all__ = ['fcfs', 'sstf', 'scan', 'cscan']
