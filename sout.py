import os

# Request directory from user
# Returns type string
def req_dir():
    print("Please input a directory to scan: ", end='')
    dir_to_scan = input()
    return dir_to_scan

# Scan directory via OS library
# Returns iterator
def scan_dir(dir_string):
    total_size = 0
    scanned = os.scandir(dir_string)
    # TODO: Add verbose flag for prints
    #print("Operating on directories:\n")
    #for dir in scanned:
    #    print(dir)
    return scanned

# Take the size of the directory given & all subdirectories in it
# WILL ERROR OUT ON EXCESSIVE SYMLINKS
# WILL ERROR OUT ON OS RESTRICTED FILES REGARDLESS OF PERMISSIONS
def sizer(iterable):
    total = 0
    try:
        for f in iterable:
            if not (hasattr(f, 'is_file') and hasattr(f, 'is_dir')):
                print(f, "is of wrong type: IGNORING!")
            elif f.is_file():
                total += f.stat().st_size
            elif f.is_dir():
                total += sizer(os.scandir(f))
    except PermissionError:
        print("Received permissions error:", PermissionError)
    except OSError:
        print("Received OS error:", OSError)
    return total

# Make things easy for the user
def human_readable(int):
    if int < 1000:
        return "%i" % int + " Bytes"
    elif 1000 <= int <= 1000000:
        return "%.1f" % float(int/1000) + " Kilobytes"
    elif 1000000 <= int <= 1000000000:
        return "%.1f" % float(int/1000000) + " Megabytes"
    elif 1000000000 <= int:
        return "%.1f" % float(int/1000000000) + " Gigabytes"

# Request & save directory to size from user
dir_str = req_dir()
# Scan saved directory path & save returned iterator
dir_iter = scan_dir(dir_str)
# Pass saved iterator to sizer & save returned size count
b_size = sizer(dir_iter)
# Convert saved byte size count to easily parsed unit & print
print(human_readable(b_size))
