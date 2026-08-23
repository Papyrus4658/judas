# This is a simple packet capture tool.
#
# I named it “Judas.”
#
# This name is a recursive acronym for
#
# “Judas: Ubiquitous Data Analyzing System”
#
# or simply means a peephole.
from scapy.all import scapy

import window


def main():
    w = window.Window()
    w.win.mainloop()


if __name__ == "__main__":
    main()
