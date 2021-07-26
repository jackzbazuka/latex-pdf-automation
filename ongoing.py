text = "Jun 2021 - Oct 2021"
arr = text.split()

if arr[4] == "2021":
    if arr[3] == "Aug" or arr[3] == "Sep" or arr[3] == "Nov" or arr[3] == "Dec":
        arr[3] = ""
        arr[4] = "Ongoing"
elif arr[4] == "2022":
    if (
        arr[3] == "Jan"
        or arr[3] == "Feb"
        or arr[3] == "Mar"
        or arr[3] == "Apr"
        or arr[3] == "May"
        or arr[3] == "Jun"
        or arr[3] == "Jul"
    ):
        arr[3] = ""
        arr[4] = "Ongoing"
print(arr)
