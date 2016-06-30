#!/usr/bin/env python3
#-*- coding:utf-8 -*-

LD = {
    "Debian":0,
    "Ubuntu":0,
    "LinuxMint":0,
    "CentOS":0,
    "Fedora":0,
    "OpenSuSE":0,
    "Arch":0,
    "Gentoo":0,
    "Slackware":0
}

def plus(step,*list):
    for x in list:
        x += step

print("你是否为有一定Linux经验的老手？\nY.是\tN.否")
a = input(">>> ")
if a == "Y":
    plus(2,LD["Debian"],LD["CentOS"],LD["Fedora"])# += 2
    plus(1,LD["Arch"],LD["Gentoo"],LD["Slackware"])# += 1
elif a == "N":
    plus(1,LD["Ubuntu"],LD["LinuxMint"],LD["OpenSuSE"])# += 1

print("你是否需要一个追求最快更新的发行版而不是一个稳定的发行版？\nY.最新的\tN.稳定的")
a = input(">>> ")
if a == "Y":
    plus(1,LD["Fedora"],LD["Arch"])# += 1
elif a == "N":
    plus(2,LD["Debian"],LD["CentOS"],LD["OpenSuSE"],LD["Gentoo"],LD["Slackware"])# += 2
    plus(1,LD["Ubuntu"],LD["LinuxMint"])# += 1

print("你是否极度渴望图形界面？\nY.是\tN.否")
a = input(">>> ")
if a == "Y":
    plus(2,LD["OpenSuSE"])# += 2
    plus(1,LD["Ubuntu"],LD["LinuxMint"])# += 1
elif a == "N":
    plus(1,LD["Debian"],LD["CentOS"],LD["Fedora"],LD["Arch"],LD["Gentoo"],LD["Slackware"])# += 1

print("你是否更需要滚动更新的发行版？\nY.滚动的\tN.版本的")
a = input(">>> ")
if a == "Y":
    plus(1,LD["Arch"],LD["Gentoo"])# += 1
elif a == "N":
    plus(1,LD["Debian"],LD["Ubuntu"],LD["LinuxMint"],LD["CentOS"],LD["Fedora"],LD["OpenSuSE"],LD["Slackware"])# += 1

print("你的电脑是否性低下？\nY.是\tN.否")
a = input(">>> ")
if a == "Y":
    plus(2,LD["Arch"])# += 2
    plus(1,LD["Debian"],LD["LinuxMint"],LD["CentOS"],LD["Fedora"],LD["Slackware"])# += 1
elif a == "N":
    plus(1,LD["Gentoo"],LD["OpenSuSE"],LD["Ubuntu"])# += 1

print("你是否需要较高的灵活性和可定制性？\nY.是\tN.否")
a = input(">>> ")
if a == "Y":
    plus(2,LD["Gentoo"])# += 2
    plus(1,LD["Arch"])# += 1
elif a == "N":
    plus(1,LD["Debian"],LD["Ubuntu"],LD["LinuxMint"],LD["CentOS"],LD["Fedora"],LD["OpenSuSE"],LD["Slackware"])# += 1

n = 0
for x in LD:
    print(x,LD[x])
    if LD[x] > n:
        n = LD[x]

print("适合您的Linux发行版有：")

for x in LD:
    if LD[x] == n:
        print(x)
