flag = "HCS{3z_3s0l4ng_r3v}"
key = 0x5a

# generate the target array
target = []
for i, c in enumerate(flag):
    val = (ord(c) + (i * 7)) ^ key
    target.append(val)

print("targets:")
print(target)

print("raw correct flag:")
print([ord(c) for c in flag])
print("\n".join([str(ord(c)) for c in flag]))

# quick sanity check lmaoa
recovered = "".join(chr((v ^ key) - (i * 7)) for i, v in enumerate(target))
assert recovered == flag
print("sanity check worked :3")
