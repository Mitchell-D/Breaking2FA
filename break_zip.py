#!/usr/bin/python

import os
import subprocess
from time import perf_counter
import shlex

# To re-run already-cracked passwords, remove john/run/john.pot

hashcommand = "john/run/zip2john {zipname}"
crackcommand = "john/run/john --format=pkzip {hashfile}"
zipcommand = "zip --password {pass} -j {zipname} {filename}"
workdir = "/home/krttd/uah/22.s/cs465/project1/test"
logfile = "cracked.log"
log_output = True

def make_zip(password:str, filename:str, filetext:str):
    """
    @:param password -- the password to use for the zip archive
    @:param filename -- name of a non-existent file to encrypt, don't include
                        any file extensions here.
    @:param filetext -- text to write to the new file before encrypting
    @:return path -- qualified path to the generated zip file

    Make an encrypted zipped archive with the provided password and file info.
    """
    #  Format the paths for the new zip file and the included text file
    fname = os.path.join(workdir, filename+".txt")
    zname = os.path.join(workdir, filename+".zip")
    print(f"Zipping {fname} to {zname} with password {password}\n")

    #  Make sure the text file doesn't already exist
    if os.path.isfile(fname):
        raise IOError(f"Provided file already exists! {filename}\n")

    #  Create the text file to write to
    with open(fname, "w") as txtfp:
        print(f"Writing to {fname}\n")
        txtfp.write(filetext)

    #  Format the zipping command and run it
    command = zipcommand.replace("{pass}", password).replace(
        "{filename}", fname).replace("{zipname}", zname)
    print(f"Using command: {command}\n")
    zipproc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    out, err = zipproc.communicate()

    #  Remove the text file and return the path to the new zip file
    if os.path.isfile(fname):
        print(f"removing {fname}\n")
        os.unlink(fname)
    return zname

def crack_zip(zipfile):
    """
    @:param zipfile The file to attempt to crack

    Use John the ripper (installed in the local directory) to crack the
    password for a provided zip file
    """
    #  Make sure this method was provided a valid zip file
    if not os.path.isfile(zipfile):
        raise IOError(f"{zipfile} is not a valid file!")

    #  Write a file with the zip file's hash
    hashcom = hashcommand.replace("{zipname}", zipfile)
    hashproc = subprocess.Popen(shlex.split(hashcom), stdout=subprocess.PIPE)
    out, err = hashproc.communicate()
    with open("tmp.hash", "wb") as hashfp:
        hashfp.write(out)

    #  Run the cracking command and record the time elapsed.
    t0 = perf_counter()
    crackcom = crackcommand.replace("{hashfile}", "tmp.hash")
    crackproc = subprocess.Popen(shlex.split(crackcom), stdout=subprocess.PIPE)
    out, err = crackproc.communicate()
    tf = perf_counter()
    print(f"file={zipfile}, time={tf-t0} sec")

    #  Write the output to the log file
    if log_output:
        with open(logfile, "wb") as lffp:
            lffp.write(out)

    #  Remove the temporary hash file
    os.unlink("tmp.hash")

if __name__ == "__main__":
    passwords = [
            "iloveyou",
            "happy2002",
            "sambarock",
            #"happy 2002",
            #  Elapsed time: 8:31:34
            # '"Password 465"',
            #  Elapsed time: 13:33:03
            #"Ball2022Game",
            #  Elapsed time: 13:50:28
            #"Ball2022Game",
            #"SuperBowl!Horray", 13:50:28
            #  Elapsed time: 13:21:35
            # "E$%!&dret5@!#@#@#",
            "!123#UAH$Go"
            ]

    txtfile = "mysecret"
    filetext = "Hello World!"

    for pw in passwords:
        zipfile = make_zip(pw, txtfile, filetext)
        print(f"made zip file: {zipfile}\n")
        crack_zip(zipfile)
