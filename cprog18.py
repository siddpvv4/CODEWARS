def pick_peaks(arr):
    pos = []
    peaks = []

    i = 1

    while i < len(arr) - 1:
        if arr[i] > arr[i - 1]:
            peak_pos = i

            # Skip plateau
            while i < len(arr) - 1 and arr[i] == arr[i + 1]:
                i += 1

            # Make sure we're not at the end
            if i < len(arr) - 1 and arr[i] > arr[i + 1]:
                pos.append(peak_pos)
                peaks.append(arr[peak_pos])

        i += 1

    return {"pos": pos, "peaks": peaks}
